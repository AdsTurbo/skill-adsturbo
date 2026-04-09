#!/usr/bin/env python3
"""
AI Actor module — list, TTS, and video generation with AI digital humans (OpenAPI v1).

Subcommands:
  list     List available AI actors (with filters)
  say      Generate TTS audio with an actor's voice
  perform  Generate a talking-head video with an AI actor (async)
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient, AdsTurboError


def cmd_list(args, _parser):
    client = AdsTurboClient()
    body = {}
    for key in ("gender", "age", "situation", "sort_by", "offset", "limit", "pose", "shot_type"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    result = client.post("/openapi/v1/aiactor/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_say(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id, "script": args.script}
    if args.auto_emotion:
        body["auto_emotion"] = True
    for key in ("speed", "stability", "similarity"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    result = client.post("/openapi/v1/aiactor/say", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_perform(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id, "script": args.script}
    if args.auto_emotion:
        body["auto_emotion"] = True
    for key in ("speed", "stability", "similarity", "style", "callback_id"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    if args.speaker_boost:
        body["speaker_boost"] = True
    result = client.post("/openapi/v1/aiactor/perform", body)
    ws_id = result.get("workspace_id", "")
    print(f"Task submitted. Workspace ID: {ws_id}", file=sys.stderr)
    if ws_id and not args.submit_only:
        detail = client.poll_work_status(str(ws_id), timeout=args.timeout, interval=args.interval)
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    detail = client.poll_work_status(args.workspace_id, timeout=args.timeout, interval=args.interval)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _csv(val):
    """Parse comma-separated string into list."""
    return [v.strip() for v in val.split(",") if v.strip()]


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo AI Actor (OpenAPI v1)")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # list
    p = sub.add_parser("list", help="List available AI actors")
    p.add_argument("--gender", type=_csv, help="Filter: female,male")
    p.add_argument("--age", type=_csv, help="Filter: senior,adult,young-adult,kid")
    p.add_argument("--situation", type=_csv, help="Filter: balcony,beach,bedroom,...")
    p.add_argument("--pose", type=_csv, help="Filter: arms-crossed,sitting,standing,...")
    p.add_argument("--shot-type", dest="shot_type", type=_csv, help="Filter: close-up,full-shot,medium-shot,...")
    p.add_argument("--sort-by", dest="sort_by", help="Sort field")
    p.add_argument("--offset", type=int, help="Pagination offset")
    p.add_argument("--limit", type=int, help="Page size")

    # say
    p = sub.add_parser("say", help="Generate TTS audio")
    p.add_argument("--actor-id", required=True, dest="actor_id", help="Actor ID")
    p.add_argument("--script", required=True, help="Text to speak")
    p.add_argument("--auto-emotion", dest="auto_emotion", action="store_true", help="Enable auto emotion")
    p.add_argument("--speed", type=float, help="Speech speed")
    p.add_argument("--stability", type=float, help="Voice stability")
    p.add_argument("--similarity", type=float, help="Voice similarity")

    # perform
    p = sub.add_parser("perform", help="Generate talking-head video with AI actor")
    p.add_argument("--actor-id", required=True, dest="actor_id", help="Actor ID")
    p.add_argument("--script", required=True, help="Text for the actor to speak")
    p.add_argument("--auto-emotion", dest="auto_emotion", action="store_true", help="Enable auto emotion")
    p.add_argument("--speed", type=float, help="Speech speed")
    p.add_argument("--stability", type=float, help="Voice stability")
    p.add_argument("--similarity", type=float, help="Voice similarity")
    p.add_argument("--style", type=float, help="Voice style")
    p.add_argument("--speaker-boost", dest="speaker_boost", action="store_true", help="Speaker boost")
    p.add_argument("--callback-id", dest="callback_id", help="Custom callback tracking ID")
    p.add_argument("--submit-only", action="store_true", help="Submit only, don't poll")
    p.add_argument("--timeout", type=float, default=600, help="Polling timeout (default: 600)")
    p.add_argument("--interval", type=float, default=5, help="Polling interval (default: 5)")

    # query
    p = sub.add_parser("query", help="Poll existing workspace ID")
    p.add_argument("--workspace-id", dest="workspace_id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"list": cmd_list, "say": cmd_say, "perform": cmd_perform, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
