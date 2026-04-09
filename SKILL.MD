---
name: adsturbo-skill
description: "AI视频创作平台（AI-powered video creation）。支持：AI数字人口播、自定义Persona、视频翻译、换角色、对口型/口型同步、去水印、4K提升、动作控制、视频字幕、视频复刻、图片生成。Generate videos with AI actors, create custom personas, translate, character-swap, lip-sync, and more — all via simple commands."
metadata:
  tags: adsturbo, video, ai-actor, persona, adclone, lip-sync, character-swap, translate, image, 复刻视频, 数字人, 去水印, 换角色, 口型同步, 视频翻译, 4K, 生成图片
requires:
  bins: [python3]
primaryEnv: ADSTURBO_API_KEY
---

# AdsTurbo AI Skill

> Modular Python toolkit for the [AdsTurbo.ai](https://adsturbo.ai) Open API.
> AdsTurbo AI 视频创作工具包，支持中英文指令。

- AI Actor / AI数字人: List actors, generate TTS audio, create talking-head videos
- Persona / 自定义Persona: Create custom digital humans from photo + voice
- AdClone / 视频复刻: Analyze and recreate videos from reference
- Video Tools / 视频工具: Lip-sync 对口型, character-swap 换角色, translate 翻译, watermark removal 去水印, upscale 超分, motion control 动作控制, subtitle 字幕, video analysis 拉片
- Image Creation / AI生成图片: AI-powered image generation

## Execution Rule

> **Always use the Python scripts in `scripts/`. Do NOT use `curl` or direct HTTP calls.**

## User-Facing Reply Rules

1. **Keep replies short** — give the result or next step directly.
2. **Use plain language** — no API jargon, no terminal references, no JSON/script mentions.
3. **Never mention terminal details** — no command output, logs, exit codes, or file paths.
4. **Be result-oriented** — after task completion, give the user the result (link, video URL) directly.
5. **Explain errors simply** — one sentence about what happened, ask if they want to retry.
6. **Give time estimates** — after submitting a task, tell the user the estimated wait time.

**Estimated Generation Time**

| Task Type | Estimated Time |
|-----------|---------------|
| AI Actor Perform | ~2-5 min |
| Lip Sync | ~2-5 min |
| Video Character Swap | ~3-5 min |
| Video Translate | ~5-10 min |
| Video Inpainting (Watermark Removal) | ~2-5 min |
| Super Resolve / 4K | ~3-5 min |
| Video Subtitle | ~2-5 min |
| AdClone Generate | ~3-10 min |
| Image Create | ~30s-1 min |

## Prerequisites

- **Python 3.8+**
- **ADSTURBO_API_KEY** — Bearer token for API authentication
- Optional: **ADSTURBO_BASE_URL** (defaults to `https://adsturbo.ai/klian/novartapi`)

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent Workflow Rules

> **These rules apply to ALL async task modules.**

1. **Async task pattern**: Most tasks follow submit → poll `/openapi/v1/work/status` → get result.
   - Submit a task via the module's `run` or `submit` subcommand
   - `run` submits and polls automatically until done
   - `submit` fires the task and returns a `workspace_id`
   - `query` resumes polling a known `workspace_id`
2. **Always start with `run`** — it submits the task and polls automatically until done.
3. **Only use `submit`** for batch jobs where you want to fire-and-forget, then poll separately.
4. **Only use `query`** when `run` timed out and you have a workspace ID to resume polling.
5. **If `query` times out**, increase `--timeout` and try again. Do not resubmit unless the task actually failed.

```
Decision tree:
→ New request?       use `run`
→ run timed out?     use `query --workspace-id <id>`
→ query timed out?   use `query --workspace-id <id> --timeout 1200`
→ task failed?       resubmit with `run`
```

## Modules

| Module | Script | Reference | Description |
|--------|--------|-----------|-------------|
| AI Actor | `scripts/ai_actor.py` | [ai_actor.md](references/ai_actor.md) | AI digital humans: list actors, TTS audio, talking-head video |
| Persona | `scripts/persona.py` | [persona.md](references/persona.md) | Custom persona: create from photo+voice, list, delete, check status |
| AdClone | `scripts/adclone.py` | [adclone.md](references/adclone.md) | Video clone: analyze reference video, generate similar video |
| Video Tools | `scripts/video_tools.py` | [video_tools.md](references/video_tools.md) | Video processing: analyze, lip-sync, inpaint, translate, upscale, character-swap, motion-control, subtitle |
| Image | `scripts/image.py` | [image.md](references/image.md) | AI image creation from prompt or reference |

> **Read individual reference docs for usage, options, and examples.**

---

## Creative Guide

> **Core Principle:** Start from the user's intent, not from the API.
> **核心原则：** 从用户意图出发，而非从 API 出发。

### Step 1 — Intent Analysis / 意图分析

| Dimension / 维度 | Ask Yourself / 判断依据 | Fallback / 兜底 |
|-----------|-------------|----------|
| **Output Type / 输出类型** | Video 视频? Image 图片? Audio 音频? | Must ask / 必须追问 |
| **Purpose / 用途** | Marketing ad 广告? Social media 社交媒体? Product demo 产品演示? | General marketing / 通用营销 |
| **Source Material / 素材** | Has image/video 有图片/视频? Has script 有脚本? | Must ask / 必须追问 |
| **Style / Tone / 风格** | Professional 专业? Casual 休闲? Dynamic 动感? | Professional / 专业 |

### Step 2 — Tool Selection / 工具选择

```
用户需要什么？ / What does the user need?
│
├─ 复刻视频 / 仿制视频 / 参考视频生成新视频 / Recreate a video from reference?
│  → adclone analyze + adclone run
│
├─ 数字人说话 / AI数字人 / 真人口播 / AI actor speaking to camera?
│  → ai_actor perform (使用平台数字人)
│
├─ 创建自定义数字人 / 克隆形象 / Create custom persona?
│  → persona create (从照片+声音创建)
│
├─ 生成图片 / AI画图 / 文生图 / Generate an AI image?
│  → image run
│
├─ 语音合成 / 文字转语音 / TTS?
│  → ai_actor say
│
├─ 对口型 / 口型同步 / 换口型 / Lip-sync a video?
│  → video_tools lipsync
│
├─ 去水印 / 去除视频水印 / Remove watermark?
│  → video_tools inpaint
│
├─ 换角色 / 替换整个人 / Swap characters?
│  → video_tools character-swap
│
├─ 视频翻译 / 多语言翻译 / Translate a video?
│  → video_tools translate
│
├─ 提升分辨率 / 4K增强 / 视频高清化 / Upscale to 4K?
│  → video_tools upscale
│
├─ 动作控制 / 控制视频动作 / Motion control?
│  → video_tools motion-control
│
├─ 视频字幕 / 添加字幕 / 字幕翻译 / Add subtitles?
│  → video_tools subtitle
│
├─ 视频分析 / 拉片 / Analyze video?
│  → video_tools analyze
│
└─ 查任务状态 / 看结果 / Check task status?
   → Use the module's `query --workspace-id <id>` subcommand
```

### 中文常见表达 → 工具速查表

> 用户经常使用以下中文说法，对应的工具如下：

| 用户说法（中文） | 实际意图 | 对应工具 |
|---|---|---|
| 复刻视频、仿制视频、照着拍一个 | 基于参考视频生成相似视频 | `adclone analyze` + `adclone run` |
| 数字人口播、让数字人说这段话 | AI 数字人说话视频 | `ai_actor perform` |
| 克隆我的形象、用我的照片做数字人 | 创建自定义数字人 | `persona create` |
| 生成图片、AI 画图、文生图 | 从文本生成图片 | `image run` |
| 对口型、口型同步、换音频 | 视频口型匹配新音频 | `video_tools lipsync` |
| 去水印、去 logo | 移除视频水印 | `video_tools inpaint` |
| 换角色、替换整个人 | 视频角色整体替换 | `video_tools character-swap` |
| 翻译视频、视频翻译成英文 | 视频多语言翻译 | `video_tools translate` |
| 4K、提升画质、高清化、超分 | 提升视频分辨率 | `video_tools upscale` |
| 动作控制、控制人物动作 | 视频动作引导 | `video_tools motion-control` |
| 加字幕、字幕翻译、视频字幕 | 视频字幕添加/翻译 | `video_tools subtitle` |
| 拉片、视频分析 | 视频内容分析 | `video_tools analyze` |
| 语音合成、文字转语音、TTS | 文本转语音 | `ai_actor say` |
| 管理我的数字人、查看自定义角色 | 自定义 Persona | `persona list` / `persona status` |

---

## Capability Boundaries / 能力边界

| Capability / 能力 | Status | Script |
|---------------------------------|-----------|-----|
| AI Actor — 数字人列表/口播视频/TTS | Available | `scripts/ai_actor.py` |
| Persona — 自定义数字人(创建/删除/列表/状态) | Available | `scripts/persona.py` |
| AdClone — 视频复刻(分析/生成) | Available | `scripts/adclone.py` |
| Lip Sync / 对口型 | Available | `scripts/video_tools.py lipsync` |
| Video Inpainting / 去水印 | Available | `scripts/video_tools.py inpaint` |
| Video Character Swap / 视频换角色 | Available | `scripts/video_tools.py character-swap` |
| Video Translate / 视频翻译 | Available | `scripts/video_tools.py translate` |
| 4K Super Resolve / 4K超分 | Available | `scripts/video_tools.py upscale` |
| Video Motion Control / 动作控制 | Available | `scripts/video_tools.py motion-control` |
| Video Analyze / 视频分析 | Available | `scripts/video_tools.py analyze` |
| Video Subtitle / 视频字幕 | Available | `scripts/video_tools.py subtitle` |
| Image Creation / AI生成图片 | Available | `scripts/image.py` |

> **Never promise capabilities that don't exist as modules.**
