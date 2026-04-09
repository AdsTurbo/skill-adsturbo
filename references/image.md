# Image Module

AI-powered image creation.

## When to Use

When you need to generate images from a text prompt or reference images.

## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** Submit and wait | Yes (if async) |
| `submit` | Batch: fire task without waiting | No |
| `query` | Resume polling a known workspace ID | Yes |

## Usage

```bash
python {baseDir}/scripts/image.py <subcommand> [options]
```

## Examples

```bash
# Generate image from prompt
python {baseDir}/scripts/image.py run --prompt "A futuristic cityscape at sunset"

# With specific model and ratio
python {baseDir}/scripts/image.py run --prompt "Product photo" --model "nanobanana_pro" --ratio "16:9"

# Generate multiple images in parallel
python {baseDir}/scripts/image.py run --prompt "Abstract art" --concurrency 4

# Edit mode with reference images
python {baseDir}/scripts/image.py run --prompt "Make it blue" --image-urls "https://example.com/img.jpg"
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt TEXT` | Image prompt |
| `--image-urls URLS` | Comma-separated reference image URLs (edit mode) |
| `--model NAME` | Model name (default: nanobanana_pro). Options: nanobanana-pro, nano-banana-2, seedream-4.5, gpt-image-1.5, grok-2-image, etc. |
| `--ratio RATIO` | Aspect ratio |
| `--resolution RES` | Resolution |
| `--concurrency N` | Parallel output count |
| `--sync-mod` | Synchronous mode (returns images directly) |
| `--timeout SECS` | Polling timeout (default: 300) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

Returns `{ "images": ["url1", ...], "workspace_ids": ["id1", ...] }`.
In sync mode, `images` array is populated directly. In async mode, poll `workspace_ids` via work/status.
