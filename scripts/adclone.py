#!/usr/bin/env python3
"""
AdClone module — video clone analysis and generation (OpenAPI v1).

Subcommands:
  analyze     Analyze a video segment for cloning
  run         Submit clone generation and poll until done
  submit      Submit clone generation only
  query       Poll an existing workspace ID
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_analyze(args, _parser):
    client = AdsTurboClient()
    body = {"video_url": args.video_url}
    if args.clip_start is not None:
        body["clip_start"] = args.clip_start
    if args.clip_end is not None:
        body["clip_end"] = args.clip_end
    result = client.post("/openapi/v1/adclone/analyze", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_run(args, _parser):
    client = AdsTurboClient()
    body = _build_generate_body(args)
    print("Submitting adclone generation task...", file=sys.stderr)
    result = client.post("/openapi/v1/adclone/generate", body)
    ws_id = result.get("workspace_id", "")
    print(f"Task submitted. Workspace ID: {ws_id}", file=sys.stderr)
    if ws_id:
        detail = client.poll_work_status(str(ws_id), timeout=args.timeout, interval=args.interval)
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    body = _build_generate_body(args)
    result = client.post("/openapi/v1/adclone/generate", body)
    ws_id = result.get("workspace_id", "")
    print(ws_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    detail = client.poll_work_status(args.workspace_id, timeout=args.timeout, interval=args.interval)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _build_generate_body(args) -> dict:
    body = {}
    for key in ("prompt", "video_url", "callback_id"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    if args.concurrent is not None:
        body["concurrent"] = args.concurrent
    if args.duration is not None:
        body["duration"] = args.duration
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo AdClone — video clone (OpenAPI v1)")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # analyze
    p = sub.add_parser("analyze", help="Analyze a video segment for cloning")
    p.add_argument("--video-url", dest="video_url", required=True, help="Source video URL")
    p.add_argument("--clip-start", dest="clip_start", type=int, help="Start time in seconds")
    p.add_argument("--clip-end", dest="clip_end", type=int, help="End time in seconds (clip_end - clip_start <= 12)")

    # run (generate + poll)
    p = sub.add_parser("run", help="Submit clone generation and poll until done")
    p.add_argument("--prompt", help="Text-to-video prompt (can be modified from analyze output)")
    p.add_argument("--video-url", dest="video_url", help="Source video segment URL (from analyze)")
    p.add_argument("--concurrent", type=int, help="Parallel generation count")
    p.add_argument("--duration", type=int, help="Duration: 4, 8, or 12 seconds")
    p.add_argument("--callback-id", dest="callback_id", help="Custom callback tracking ID")
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    # submit
    p = sub.add_parser("submit", help="Submit clone generation only")
    p.add_argument("--prompt", help="Text-to-video prompt")
    p.add_argument("--video-url", dest="video_url", help="Source video segment URL")
    p.add_argument("--concurrent", type=int, help="Parallel generation count")
    p.add_argument("--duration", type=int, help="Duration: 4, 8, or 12 seconds")
    p.add_argument("--callback-id", dest="callback_id", help="Custom callback tracking ID")

    # query
    p = sub.add_parser("query", help="Poll existing workspace ID")
    p.add_argument("--workspace-id", dest="workspace_id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"analyze": cmd_analyze, "run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
