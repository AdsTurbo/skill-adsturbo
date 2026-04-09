#!/usr/bin/env python3
"""
Video Tools module — video processing utilities (OpenAPI v1).

Subcommands:
  analyze          Submit video analysis task
  lipsync          Submit lip-sync task
  inpaint          Submit watermark removal task
  translate        Submit video translation task
  upscale          Submit video super-resolution task
  character-swap   Submit character swap task
  motion-control   Submit motion control task
  subtitle         Submit video subtitle task

All subcommands support: run (submit + poll), submit (fire-and-forget), query (resume polling).
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient, AdsTurboError

TOOLS = {
    "analyze":        "/openapi/v1/video/analyze",
    "lipsync":        "/openapi/v1/video/lipsync",
    "inpaint":        "/openapi/v1/video/inpaint",
    "translate":      "/openapi/v1/video/translate",
    "upscale":        "/openapi/v1/video/upscale",
    "character-swap": "/openapi/v1/video/character-swap",
    "motion-control": "/openapi/v1/video/motion-control",
    "subtitle":       "/openapi/v1/video/subtitle",
}


WORK_STATUS_PATH = "/openapi/v1/work/status"


def _poll_work_status(client, workspace_id: str, timeout: float = 600, interval: float = 5) -> dict:
    """Poll /openapi/v1/work/status until terminal status."""
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"Polling timed out after {timeout}s for workspace {workspace_id}")
        print(f"  Polling work status (elapsed {elapsed:.0f}s)...", file=sys.stderr)
        result = client.post(WORK_STATUS_PATH, {"workspace_id": workspace_id})
        status = result.get("status", "")
        if status == "completed":
            print(f"  Task completed.", file=sys.stderr)
            return result
        if status == "failed":
            raise AdsTurboError(-1, f"Task failed: {result.get('message', '')}")
        time.sleep(interval)


def cmd_run(args, _parser):
    client = AdsTurboClient()
    endpoint = TOOLS[args.tool]
    body = _collect_params(args)
    print(f"Submitting {args.tool} task...", file=sys.stderr)
    result = client.post(endpoint, body)
    ws_id = result.get("workspace_id", "")
    print(f"Task submitted. Workspace ID: {ws_id}", file=sys.stderr)
    if ws_id:
        detail = _poll_work_status(client, str(ws_id), timeout=args.timeout, interval=args.interval)
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    endpoint = TOOLS[args.tool]
    body = _collect_params(args)
    result = client.post(endpoint, body)
    ws_id = result.get("workspace_id", "")
    print(ws_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    detail = _poll_work_status(client, args.workspace_id, timeout=args.timeout, interval=args.interval)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _collect_params(args) -> dict:
    body = {}
    for key in (
        "video_url", "audio_url", "avatar_url", "image_url", "prompt",
        "workspace_id", "callback_id", "target_lang", "source_language",
        "translate_language", "subtitle_format", "style_type",
        "character_orientation", "negative_prompt", "mode",
    ):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    if getattr(args, "keep_original_sound", None) is not None:
        body["keep_original_sound"] = args.keep_original_sound
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Video Tools (OpenAPI v1)")
    sub = parser.add_subparsers(dest="action")
    sub.required = True

    for action in ("run", "submit"):
        p = sub.add_parser(action, help=f"{action.capitalize()} a video tool task")
        p.add_argument("tool", choices=list(TOOLS.keys()), help="Which tool to use")
        p.add_argument("--video-url", dest="video_url", help="Video URL")
        p.add_argument("--audio-url", dest="audio_url", help="Audio URL (for lipsync)")
        p.add_argument("--avatar-url", dest="avatar_url", help="Avatar URL (for lipsync)")
        p.add_argument("--image-url", dest="image_url", help="Image URL (for character-swap, motion-control)")
        p.add_argument("--prompt", help="Prompt text")
        p.add_argument("--workspace-id", dest="workspace_id", type=int, help="Associated workspace ID")
        p.add_argument("--callback-id", dest="callback_id", help="Custom callback tracking ID")
        p.add_argument("--target-lang", dest="target_lang", help="Target language (for translate)")
        p.add_argument("--source-language", dest="source_language", help="Source language (for subtitle)")
        p.add_argument("--translate-language", dest="translate_language", help="Translate language (for subtitle)")
        p.add_argument("--subtitle-format", dest="subtitle_format", help="Subtitle format")
        p.add_argument("--style-type", dest="style_type", help="Subtitle style type")
        p.add_argument("--character-orientation", dest="character_orientation", help="Character orientation (for motion-control)")
        p.add_argument("--keep-original-sound", dest="keep_original_sound", action="store_true", default=None, help="Keep original sound (for motion-control)")
        p.add_argument("--negative-prompt", dest="negative_prompt", help="Negative prompt (for motion-control)")
        p.add_argument("--mode", help="Mode (for motion-control)")
        p.add_argument("--params", help="Extra params as JSON string")
        p.add_argument("--timeout", type=float, default=600)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing workspace ID")
    p.add_argument("--workspace-id", dest="workspace_id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.action](args, parser)


if __name__ == "__main__":
    main()
