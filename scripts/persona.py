#!/usr/bin/env python3
"""
Persona module — custom AI persona management (OpenAPI v1).

Subcommands:
  create    Create a custom persona from photo + optional voice
  delete    Delete a custom persona
  list      List your custom personas
  status    Check persona creation status
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_create(args, _parser):
    client = AdsTurboClient()
    body = {}
    for key in ("photo_url", "voice_audio_url", "name", "callback_id"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    result = client.post("/openapi/v1/persona/create", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_delete(args, _parser):
    client = AdsTurboClient()
    result = client.post("/openapi/v1/persona/delete", {"actor_id": args.actor_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_list(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.offset is not None:
        body["offset"] = args.offset
    if args.limit is not None:
        body["limit"] = args.limit
    result = client.post("/openapi/v1/persona/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_status(args, _parser):
    client = AdsTurboClient()
    result = client.post("/openapi/v1/persona/status", {"actor_id": args.actor_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Persona Management (OpenAPI v1)")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # create
    p = sub.add_parser("create", help="Create a custom persona")
    p.add_argument("--photo-url", dest="photo_url", required=True, help="Photo URL for persona")
    p.add_argument("--voice-audio-url", dest="voice_audio_url", help="Voice audio URL for voice cloning (optional)")
    p.add_argument("--name", help="Persona name")
    p.add_argument("--callback-id", dest="callback_id", help="Custom callback tracking ID")

    # delete
    p = sub.add_parser("delete", help="Delete a custom persona")
    p.add_argument("--actor-id", dest="actor_id", required=True, help="Actor ID to delete")

    # list
    p = sub.add_parser("list", help="List your custom personas")
    p.add_argument("--offset", type=int, help="Pagination offset")
    p.add_argument("--limit", type=int, help="Page size")

    # status
    p = sub.add_parser("status", help="Check persona creation status")
    p.add_argument("--actor-id", dest="actor_id", required=True, help="Actor ID to check")

    args = parser.parse_args()
    {"create": cmd_create, "delete": cmd_delete, "list": cmd_list, "status": cmd_status}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
