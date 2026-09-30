#!/usr/bin/env python3
"""HTTP client for the AdsTurbo Open API.

Covers the three response shapes the server can return:
  1. envelope success  {"ret": 1, "data": {"ent": {...}}}
  2. envelope failure  {"ret": <non-1>, "msg": "..."}  -- still HTTP 200
  3. auth failure      HTTP 401 with a plain-text body, no envelope at all
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests

DEFAULT_BASE_URL = "https://adsturbo.ai/klian/novartapi"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 900
REQUEST_TIMEOUT = 60
UPLOAD_TIMEOUT = 300

WORK_STATUS_PATH = "/openapi/v1/work/status"
WORK_BATCH_STATUS_PATH = "/openapi/v1/work/batch-status"

TERMINAL_OK = "completed"
TERMINAL_FAIL = "failed"


class AdsTurboError(Exception):
    """A business-level failure reported by the API."""

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class AdsTurboAuthError(AdsTurboError):
    """The API key is missing, invalid or expired."""

    def __init__(self, msg: str = "API key is invalid or expired"):
        super().__init__(401, msg)


class AdsTurboClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.environ.get("ADSTURBO_API_KEY", "")
        raw_base = base_url or os.environ.get("ADSTURBO_BASE_URL", DEFAULT_BASE_URL)
        self.base_url = raw_base.rstrip("/")
        if not self.api_key:
            raise AdsTurboAuthError(
                "ADSTURBO_API_KEY is not set. Get a key at https://adsturbo.ai?channel=github "
                "and export it: export ADSTURBO_API_KEY=..."
            )
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    # ---------- transport ----------

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    @staticmethod
    def _unwrap(resp: requests.Response) -> dict:
        """Turn a raw response into the `ent` payload, or raise a typed error."""
        if resp.status_code == 401:
            raise AdsTurboAuthError(
                "API key is invalid or expired. Check ADSTURBO_API_KEY."
            )
        if 300 <= resp.status_code < 400:
            # Following a redirect would downgrade POST to GET and surface as a
            # confusing 405. Point at the base URL instead, which is the real cause.
            raise AdsTurboError(
                resp.status_code,
                f"Base URL redirects to {resp.headers.get('Location', 'elsewhere')!r}. "
                f"Set ADSTURBO_BASE_URL to the final address (default: {DEFAULT_BASE_URL}).",
            )
        if resp.status_code >= 400:
            raise AdsTurboError(
                resp.status_code,
                f"HTTP {resp.status_code}: {resp.text[:200] or 'no response body'}",
            )
        try:
            body = resp.json()
        except json.JSONDecodeError:
            raise AdsTurboError(-1, f"Malformed response: {resp.text[:200]}") from None

        ret = body.get("ret", 0)
        if ret != 1:
            raise AdsTurboError(ret, body.get("msg") or "unknown error")

        data = body.get("data") or {}
        if isinstance(data, dict):
            return data.get("ent", data)
        return data

    def post(self, path: str, payload: dict | None = None) -> dict:
        """POST a JSON body and return the unwrapped `ent` payload."""
        try:
            resp = self.session.post(
                self._url(path),
                json=_drop_empty(payload or {}),
                headers={"Content-Type": "application/json"},
                timeout=REQUEST_TIMEOUT,
                allow_redirects=False,
            )
        except requests.RequestException as exc:
            raise AdsTurboError(-1, f"Network error calling {path}: {exc}") from exc
        return self._unwrap(resp)

    def upload(self, path: str, file_path: str | Path) -> dict:
        """POST a multipart file upload and return the unwrapped payload."""
        target = Path(file_path).expanduser()
        if not target.is_file():
            raise AdsTurboError(-1, f"File not found: {target}")
        # The part needs its own Content-Type: storage rejects an empty one
        # outright ("content type len 0").
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        try:
            with target.open("rb") as handle:
                resp = self.session.post(
                    self._url(path),
                    files={"data": (target.name, handle, content_type)},
                    timeout=UPLOAD_TIMEOUT,
                    allow_redirects=False,
                )
        except requests.RequestException as exc:
            raise AdsTurboError(-1, f"Network error uploading {target.name}: {exc}") from exc
        return self._unwrap(resp)

    # ---------- async task helpers ----------

    def work_status(self, workspace_id: str) -> dict:
        return self.post(WORK_STATUS_PATH, {"workspace_id": workspace_id})

    def batch_work_status(self, workspace_ids: list[str]) -> dict:
        return self.post(WORK_BATCH_STATUS_PATH, {"workspace_ids": workspace_ids})

    def poll(
        self,
        workspace_id: str,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        interval: float = DEFAULT_POLL_INTERVAL,
        verbose: bool = True,
    ) -> dict:
        """Poll work status until the task reaches a terminal state.

        Raises TimeoutError (task may still be running -- resume with `query`)
        or AdsTurboError when the task itself failed.
        """
        started = time.time()
        while True:
            elapsed = time.time() - started
            if elapsed > timeout:
                raise TimeoutError(
                    f"Still running after {timeout:.0f}s. The task is not lost -- "
                    f"resume with: query --workspace-id {workspace_id}"
                )
            result = self.work_status(workspace_id)
            status = result.get("status", "")
            if status == TERMINAL_OK:
                return result
            if status == TERMINAL_FAIL:
                raise AdsTurboError(-1, result.get("message") or "task failed")
            if verbose:
                print(
                    f"  {status or 'pending'} ... {elapsed:.0f}s elapsed",
                    file=sys.stderr,
                )
            time.sleep(interval)


def _drop_empty(payload: dict) -> dict:
    """Strip keys the caller left unset so the server applies its own defaults."""
    return {
        key: value
        for key, value in payload.items()
        if value is not None and value != [] and value != ""
    }


def emit(result: dict | list) -> None:
    """Print a result as indented JSON on stdout."""
    print(json.dumps(result, ensure_ascii=False, indent=2))


def run_cli(parser, handlers: dict) -> None:
    """Shared entrypoint: dispatch argparse results and render errors readably."""
    args = parser.parse_args()
    command = getattr(args, "command", None)
    if not command:
        parser.print_help()
        sys.exit(1)
    try:
        result = handlers[command](AdsTurboClient(), args)
    except AdsTurboAuthError as exc:
        print(f"Auth failed: {exc.msg}", file=sys.stderr)
        sys.exit(2)
    except AdsTurboError as exc:
        print(f"Request failed: {exc.msg}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError as exc:
        print(f"Timed out: {exc}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)
    if result is not None:
        emit(result)


def add_async_flags(sub) -> None:
    """Attach the polling flags every async submit command shares."""
    sub.add_argument("--callback-id", default="", help="your own tracking id, echoed back")
    sub.add_argument("--no-wait", action="store_true", help="submit only, do not poll")
    sub.add_argument("--timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    sub.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL)


def submit_and_maybe_poll(client: AdsTurboClient, path: str, payload: dict, args) -> dict:
    """Submit an async task, then either return the receipt or poll to completion."""
    receipt = client.post(path, payload)
    workspace_id = receipt.get("workspace_id", "")
    if getattr(args, "no_wait", False) or not workspace_id:
        return receipt
    print(f"  submitted, workspace_id={workspace_id}", file=sys.stderr)
    return client.poll(workspace_id, timeout=args.timeout, interval=args.interval)
