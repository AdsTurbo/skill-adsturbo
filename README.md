# AdsTurbo API Skill

Agent-friendly Python scripts and skill instructions for the [AdsTurbo Open API](https://adsturbo.ai/open-api).

Use this repository when you want an agent or local workflow to call AdsTurbo API modules for image generation, AI actors, custom personas, Ad Clone, video translation, lip sync, character swap, upscaling, watermark removal, motion control, subtitles, and video analysis.

## What this repo is

- A Codex-style skill definition in `SKILL.MD`
- Python wrappers in `scripts/`
- Reference docs in `references/`
- A practical API operations kit, not a prompt-only creative planning pack

For a free creative planning workflow, see [`product-page-to-ad-brief`](https://github.com/AdsTurbo/product-page-to-ad-brief).

## Prerequisites

- Python 3.8+
- An AdsTurbo API key

```bash
export ADSTURBO_API_KEY="your_api_key"
pip install -r scripts/requirements.txt
```

Optional:

```bash
export ADSTURBO_BASE_URL="https://adsturbo.ai/klian/novartapi"
```

## Modules

| Module | Script | What it does |
| --- | --- | --- |
| AI Actor | `scripts/ai_actor.py` | List actors, generate TTS audio, create actor videos |
| Persona | `scripts/persona.py` | Create, list, delete, and query custom personas |
| Ad Clone | `scripts/adclone.py` | Analyze a reference clip and generate new ad variations |
| Video Tools | `scripts/video_tools.py` | Lip sync, translate, upscale, inpaint, character swap, motion control, subtitles, analysis |
| Image | `scripts/image.py` | Generate or edit images |

Read `SKILL.MD` and each file in `references/` before wiring these scripts into an agent.

## Example workflow

```bash
python scripts/image.py run \
  --prompt "A clean ecommerce product ad image, bright studio lighting, 9:16 composition" \
  --ratio 9:16
```

Most video tasks are asynchronous. The skill defaults to a submit-and-poll pattern so agents can return the final result when the job completes.

## Safety and usage boundaries

- Use references as inspiration for structure, pacing, and format.
- Do not use this toolkit to copy protected creative assets or impersonate people without permission.
- Users are responsible for ad claims, platform policy compliance, and rights clearance.
- No hidden telemetry is included in this repository.

## Links

- Website: [adsturbo.ai](https://adsturbo.ai)
- Open API: [adsturbo.ai/open-api](https://adsturbo.ai/open-api)
- Features: [adsturbo.ai/features](https://adsturbo.ai/features)

## License

MIT
