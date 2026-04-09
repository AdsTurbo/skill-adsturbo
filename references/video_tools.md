# Video Tools Module

Video processing utilities — video analysis, lip-sync, watermark removal, translation, super-resolution, character swap, motion control, subtitle.

## When to Use

When you need to process an existing video: analyze video content, sync lip movements to new audio, remove watermarks, translate to another language, upscale resolution, swap characters, control motion, or add subtitles.

## Tools

| Tool | API Path | Description |
|------|----------|-------------|
| `analyze` | `/openapi/v1/video/analyze` | Video content analysis (拉片) |
| `lipsync` | `/openapi/v1/video/lipsync` | Sync lip movements to audio |
| `inpaint` | `/openapi/v1/video/inpaint` | Remove watermarks |
| `translate` | `/openapi/v1/video/translate` | Translate video to another language |
| `upscale` | `/openapi/v1/video/upscale` | Upscale video resolution |
| `character-swap` | `/openapi/v1/video/character-swap` | Swap characters in video |
| `motion-control` | `/openapi/v1/video/motion-control` | Control motion in video |
| `subtitle` | `/openapi/v1/video/subtitle` | Add/translate subtitles |

## Usage

```bash
python {baseDir}/scripts/video_tools.py <run|submit|query> <tool> [options]
```

## Examples

### Analyze video
```bash
python {baseDir}/scripts/video_tools.py run analyze --video-url <video_url>
```

### Lip sync
```bash
python {baseDir}/scripts/video_tools.py run lipsync --avatar-url <avatar_url> --audio-url <audio_url>
```

### Remove watermark
```bash
python {baseDir}/scripts/video_tools.py run inpaint --video-url <video_url>
```

### Translate video
```bash
python {baseDir}/scripts/video_tools.py run translate --video-url <video_url> --target-lang "zh"
```

### Upscale video
```bash
python {baseDir}/scripts/video_tools.py run upscale --video-url <video_url>
```

### Character swap
```bash
python {baseDir}/scripts/video_tools.py run character-swap --video-url <video_url> --image-url <face_image_url>
```

### Motion control
```bash
python {baseDir}/scripts/video_tools.py run motion-control --video-url <video_url> --image-url <image_url> --prompt "description"
```

### Add subtitles
```bash
python {baseDir}/scripts/video_tools.py run subtitle --video-url <video_url> --source-language "en" --translate-language "zh"
```

## Options

| Option | Description |
|--------|-------------|
| `--video-url URL` | Video URL |
| `--audio-url URL` | Audio URL (for lipsync) |
| `--avatar-url URL` | Avatar URL (for lipsync) |
| `--image-url URL` | Image URL (for character-swap, motion-control) |
| `--prompt TEXT` | Prompt text (for lipsync, motion-control) |
| `--workspace-id ID` | Associated workspace ID |
| `--callback-id ID` | Custom callback tracking ID |
| `--target-lang LANG` | Target language (for translate) |
| `--source-language LANG` | Source language (for subtitle) |
| `--translate-language LANG` | Translate language (for subtitle) |
| `--subtitle-format FMT` | Subtitle format (for subtitle) |
| `--style-type TYPE` | Subtitle style type (for subtitle) |
| `--character-orientation DIR` | Character orientation (for motion-control) |
| `--keep-original-sound` | Keep original sound (for motion-control) |
| `--negative-prompt TEXT` | Negative prompt (for motion-control) |
| `--mode MODE` | Mode (for motion-control) |
| `--params JSON` | Extra params as JSON string |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

All tools are async and return a `workspace_id`. Status is polled via `/openapi/v1/work/status` with `{"workspace_id": "<id>"}`. Terminal statuses: `completed`, `failed`. The `run` subcommand submits and polls automatically until done.
