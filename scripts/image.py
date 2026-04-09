#!/usr/bin/env python3
"""
Image module — AI image creation (OpenAPI v1).

Subcommands:
  run       Submit image creation and wait for result
  submit    Submit only, print workspace IDs
  query     Poll an existing workspace ID
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_run(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    print("Submitting image creation task...", file=sys.stderr)
    result = client.post("/openapi/v1/img/create", body)
    images = result.get("images", [])
    ws_ids = result.get("workspace_ids", [])
    if images:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif ws_ids:
        print(f"Task submitted. Workspace IDs: {ws_ids}", file=sys.stderr)
        for ws_id in ws_ids:
            detail = client.poll_work_status(str(ws_id), timeout=args.timeout, interval=args.interval)
            print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    result = client.post("/openapi/v1/img/create", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    detail = client.poll_work_status(args.workspace_id, timeout=args.timeout, interval=args.interval)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    for key in ("prompt", "model", "ratio", "resolution"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    if args.image_urls:
        body["image_urls"] = [u.strip() for u in args.image_urls.split(",") if u.strip()]
    if args.concurrency is not None:
        body["concurrency"] = args.concurrency
    if args.sync_mod:
        body["sync_mod"] = True
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Image Creation (OpenAPI v1)")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name in ("run", "submit"):
        p = sub.add_parser(name, help=f"{name.capitalize()} image creation task")
        p.add_argument("--prompt", help="Image prompt")
        p.add_argument("--image-urls", dest="image_urls", help="Comma-separated reference image URLs")
        p.add_argument("--model", help="Model name (default: nanobanana_pro)")
        p.add_argument("--ratio", help="Aspect ratio")
        p.add_argument("--resolution", help="Resolution")
        p.add_argument("--concurrency", type=int, help="Parallel output count")
        p.add_argument("--sync-mod", dest="sync_mod", action="store_true", help="Synchronous mode")
        p.add_argument("--timeout", type=float, default=300)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing workspace ID")
    p.add_argument("--workspace-id", dest="workspace_id", required=True)
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
