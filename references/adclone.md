# AdClone Module

Video clone — analyze a reference video segment and generate similar videos.

## When to Use

When you need to recreate/clone a video from a reference. Two-step workflow: analyze first, then generate.

## Subcommands

| Subcommand | Description | Async? |
|------------|-------------|--------|
| `analyze` | Analyze a video segment, get AI-generated prompt | No |
| `run` | Submit clone generation and poll until done | Yes |
| `submit` | Submit generation only | No |
| `query` | Resume polling a workspace ID | Yes |

## Usage

```bash
python {baseDir}/scripts/adclone.py <subcommand> [options]
```

## Typical Workflow

```bash
# 1. Analyze source video (extracts prompt and segment)
python {baseDir}/scripts/adclone.py analyze --video-url "https://example.com/video.mp4" --clip-start 0 --clip-end 8

# 2. Generate clone video using the prompt from step 1
python {baseDir}/scripts/adclone.py run --prompt "<prompt_from_analyze>" --video-url "<segment_url_from_analyze>" --duration 8
```

## Options

### `analyze`

| Option | Description |
|--------|-------------|
| `--video-url URL` | Source video URL (required) |
| `--clip-start N` | Start time in seconds |
| `--clip-end N` | End time in seconds (max segment: 12s) |

### `run` and `submit`

| Option | Description |
|--------|-------------|
| `--prompt TEXT` | Text-to-video prompt (from analyze, editable) |
| `--video-url URL` | Source video segment URL (from analyze) |
| `--concurrent N` | Parallel generation count |
| `--duration N` | Duration: 4, 8, or 12 seconds |
| `--callback-id ID` | Custom callback tracking ID |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

- `analyze` returns: `{ "prompt": "...", "video_segment_url": "...", "duration": N }`
- `run`/`query` returns `OpenWorkData` with `workspace_id`, `status`, `result_url`, etc.
