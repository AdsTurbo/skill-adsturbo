# AdsTurbo Skill

Agent skill for the [AdsTurbo Open API](https://adsturbo.ai/open-api): Python scripts plus instructions an agent (Claude Code, Codex, OpenClaw and others) can use to make ad creatives end to end.

- AI spokesperson videos: platform avatars, a custom avatar cloned from your photo and voice, or lip-sync a single portrait
- Video generation: text / image to video, first-and-last-frame, extend or edit an existing clip
- Ad clone: storyboard a reference ad and shoot your own version, or open an **editable draft** to rewrite the lines, swap in your own people or products and check the price before generating
- Cleanup: watermark / object removal, hard-subtitle erase, 4K upscale, subtitles
- Transform: translate and re-voice, character swap, motion control
- Images: text-to-image and editing, background removal, e-commerce product shots, posters

> This repository is generated from the same source as the AdsTurbo packages on ClawHub and skillhub.cn. Open an issue here; pull requests are welcome but get folded back into that source.

## Install

Claude Code:

```bash
git clone https://github.com/AdsTurbo/skill-adsturbo ~/.claude/skills/adsturbo
```

Codex:

```bash
git clone https://github.com/AdsTurbo/skill-adsturbo ~/.codex/skills/adsturbo
```

OpenClaw / ClawHub:

```bash
clawhub install adsturbo/adsturbo
```

ClawHub also has one smaller package per capability (`adsturbo-digital-human`, `adsturbo-video-generation`, `adsturbo-ad-clone`, `adsturbo-video-enhance`, `adsturbo-video-transform`, `adsturbo-image`) if you only need one of them.

## Setup

- Python 3.8+
- An AdsTurbo API key from https://adsturbo.ai?channel=github

```bash
export ADSTURBO_API_KEY="your_api_key"
pip install -r scripts/requirements.txt
```

Optional: `ADSTURBO_BASE_URL`, default `https://adsturbo.ai/klian/novartapi`.

Most tools need a Pro plan or above; a free key returns `Pro plan or above is required`.

## What is inside

| Path | What it is |
| --- | --- |
| `SKILL.md` | Entry point the agent reads first: when to use which tool, hard constraints, how to reply |
| `scripts/*.py` | One CLI per capability: `digital_human`, `video_generation`, `ad_clone`, `video_enhance`, `video_transform`, `image`, `upload`, `work` |
| `references/*.md` | Full parameters and examples per capability, read on demand |

```bash
# Generate a product image
python3 scripts/image.py create --prompt "A black insulated bottle on a marble countertop, studio light" --ratio 1:1

# Clone a reference ad with edited lines, check the price, then generate
python3 scripts/ad_clone.py draft-create --video-url https://example.com/ref.mp4
python3 scripts/ad_clone.py draft-preview --clone-id <clone_id> --line "L1=Your new line"
python3 scripts/ad_clone.py draft-submit --clone-id <clone_id> --line "L1=Your new line"
```

Video tasks are asynchronous. The scripts submit and then poll until the result is ready; if a wait times out, resume with `query --workspace-id <id>` instead of resubmitting, which would charge again.

## Safety and usage boundaries

- Use references as inspiration for structure, pacing and format.
- Do not use this toolkit to copy protected creative assets or impersonate people without permission.
- Users are responsible for ad claims, platform policy compliance and rights clearance.
- No hidden telemetry is included in this repository.

## Links

- Website: [adsturbo.ai](https://adsturbo.ai)
- Open API: [adsturbo.ai/open-api](https://adsturbo.ai/open-api)
- API reference: [adsturbo.readme.io](https://adsturbo.readme.io)

## 中文说明

AdsTurbo 开放接口的 agent skill：数字人口播、视频生成、广告复刻（含可改台词、换人换货的草稿流程）、视频精修与改造、AI 图片创作。安装方式同上，国内用户也可以在 [skillhub.cn](https://skillhub.cn) 搜索「AdsTurbo」安装。使用前在 https://adsturbo.ai?channel=github 获取 API Key，设置 `ADSTURBO_API_KEY` 环境变量。

## License

MIT
