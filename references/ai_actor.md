# AI Actor Module

Manage and use AI digital humans for TTS and talking-head video generation.

## When to Use

When you need to browse AI actors, generate TTS audio, or create a talking-head video.

## Subcommands

| Subcommand | When to use | Async? |
|------------|-------------|--------|
| `list` | Browse available AI actors with filters | No |
| `say` | Generate TTS audio with an actor's voice | No |
| `perform` | Generate talking-head video with AI actor | Yes — polls work/status |
| `query` | Resume polling a workspace ID | Yes |

## Usage

```bash
python {baseDir}/scripts/ai_actor.py <subcommand> [options]
```

## Examples

### List actors
```bash
python {baseDir}/scripts/ai_actor.py list
python {baseDir}/scripts/ai_actor.py list --gender "female" --age "adult" --limit 10
```

### Generate TTS audio
```bash
python {baseDir}/scripts/ai_actor.py say --actor-id <id> --script "Hello, welcome to our demo!"
```

### Generate talking-head video (submit + poll)
```bash
python {baseDir}/scripts/ai_actor.py perform --actor-id <id> --script "Hello, welcome to our product demo!"
```

## Options

### `list`

| Option | Description |
|--------|-------------|
| `--gender CSV` | Filter: female, male |
| `--age CSV` | Filter: senior, adult, young-adult, kid |
| `--situation CSV` | Filter: balcony, beach, bedroom, ... |
| `--pose CSV` | Filter: arms-crossed, sitting, standing, ... |
| `--shot-type CSV` | Filter: close-up, full-shot, medium-shot, ... |
| `--sort-by FIELD` | Sort field |
| `--offset N` | Pagination offset |
| `--limit N` | Page size |

### `say`

| Option | Description |
|--------|-------------|
| `--actor-id ID` | Actor ID (required) |
| `--script TEXT` | Text to speak (required) |
| `--auto-emotion` | Enable auto emotion |
| `--speed FLOAT` | Speech speed |
| `--stability FLOAT` | Voice stability |
| `--similarity FLOAT` | Voice similarity |

### `perform`

| Option | Description |
|--------|-------------|
| `--actor-id ID` | Actor ID (required) |
| `--script TEXT` | Text for the actor to speak (required) |
| `--auto-emotion` | Enable auto emotion |
| `--speed FLOAT` | Speech speed |
| `--stability FLOAT` | Voice stability |
| `--similarity FLOAT` | Voice similarity |
| `--style FLOAT` | Voice style |
| `--speaker-boost` | Enable speaker boost |
| `--callback-id ID` | Custom callback tracking ID |
| `--submit-only` | Submit only, don't poll |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

- `list` returns actor list with actor info (id, name, gender, age, voices, etc.)
- `say` returns `{ "audio_url": "...", "duration": N }`
- `perform` returns `OpenWorkData` with `workspace_id`, `status`, `result_url`, etc.
