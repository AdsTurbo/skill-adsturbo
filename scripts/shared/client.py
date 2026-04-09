#!/usr/bin/env python3
"""
AdsTurbo API client with Bearer token auth and work-status polling.
"""

from __future__ import annotations

import json
import os
import sys
import time

import requests

DEFAULT_BASE_URL = "https://adsturbo.ai/klian/novartapi"
DEFAULT_POLL_INTERVAL = 5
DEFAULT_POLL_TIMEOUT = 600

WORK_STATUS_PATH = "/openapi/v1/work/status"


class AdsTurboError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class AdsTurboClient:
    """HTTP client for the AdsTurbo Open API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.environ.get("ADSTURBO_API_KEY", "")
        self.base_url = (base_url or os.environ.get("ADSTURBO_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        if not self.api_key:
            print("Error: ADSTURBO_API_KEY environment variable is not set.", file=sys.stderr)
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post(self, path: str, json_body: dict | None = None) -> dict:
        """POST JSON request, return parsed response data."""
        resp = self.session.post(self._url(path), json=json_body or {})
        resp.raise_for_status()
        body = resp.json()
        ret = body.get("ret", 0)
        if ret != 1:
            raise AdsTurboError(ret, body.get("msg", "unknown error"))
        data = body.get("data", {})
        return data.get("ent", data) if isinstance(data, dict) else data

    def poll_work_status(
        self,
        workspace_id: str,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        interval: float = DEFAULT_POLL_INTERVAL,
        verbose: bool = True,
    ) -> dict:
        """
        Poll /openapi/v1/work/status until the task reaches a terminal status.
        Returns the OpenWorkData dict when done.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Polling timed out after {timeout}s for workspace {workspace_id}")
            if verbose:
                print(f"  Polling work status (elapsed {elapsed:.0f}s)...", file=sys.stderr)
            result = self.post(WORK_STATUS_PATH, {"workspace_id": workspace_id})
            status = result.get("status", "")
            if status == "completed":
                if verbose:
                    print(f"  Task completed.", file=sys.stderr)
                return result
            if status == "failed":
                raise AdsTurboError(-1, f"Task failed: {result.get('message', '')}")
            time.sleep(interval)
