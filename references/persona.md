# Persona Module

Create, manage, and monitor custom AI personas.

## When to Use

When you need to create a custom digital human from a photo (and optionally a voice sample), check its creation status, list existing personas, or delete one.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `create` | Create a custom persona from photo + optional voice |
| `delete` | Delete a custom persona |
| `list` | List your custom personas |
| `status` | Check persona creation status |

## Usage

```bash
python {baseDir}/scripts/persona.py <subcommand> [options]
```

## Examples

```bash
# Create persona from photo
python {baseDir}/scripts/persona.py create --photo-url "https://example.com/photo.jpg" --name "My Avatar"

# Create persona with voice cloning
python {baseDir}/scripts/persona.py create --photo-url "https://example.com/photo.jpg" --voice-audio-url "https://example.com/voice.mp3" --name "My Avatar"

# Check creation status
python {baseDir}/scripts/persona.py status --actor-id <actor_id>

# List personas
python {baseDir}/scripts/persona.py list

# Delete persona
python {baseDir}/scripts/persona.py delete --actor-id <actor_id>
```

## Options

### `create`

| Option | Description |
|--------|-------------|
| `--photo-url URL` | Photo URL for persona (required) |
| `--voice-audio-url URL` | Voice audio URL for voice cloning (optional) |
| `--name NAME` | Persona name |
| `--callback-id ID` | Custom callback tracking ID |

### `delete` and `status`

| Option | Description |
|--------|-------------|
| `--actor-id ID` | Actor ID (required) |

### `list`

| Option | Description |
|--------|-------------|
| `--offset N` | Pagination offset |
| `--limit N` | Page size |

## Output

- `create` returns `OpenPersonaData`: `actor_id`, `status`, `name`, `photo_url`, `voice_url`, `preview_image_url`, `preview_video_url`, `voices`, `message`, `created_at`
- `status` returns `OpenPersonaData` with current status (pending/processing/completed/failed)
- `list` returns `{ "items": [...], "offset": N, "more": bool, "total": N }`
- `delete` returns `{ "ok": true }`
