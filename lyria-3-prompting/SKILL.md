---
name: lyria-3-prompting
description: >
  Generates high-quality text prompts for Google's Lyria 3 music generation model
  (lyria-3-pro-preview and lyria-3-clip-preview) via the Gemini API or OpenRouter.
  Use this skill when asked to create, compose, or generate music, songs, jingles,
  soundtracks, or audio from a description. Handles text-to-music, image-to-music,
  vocal/lyric prompts, instrumental-only tracks, and structured song generation.
license: Apache-2.0
metadata:
  model-pro: lyria-3-pro-preview
  model-clip: lyria-3-clip-preview
  openrouter-id: google/lyria-3-pro-preview
  openrouter-url: https://openrouter.ai/google/lyria-3-pro-preview
  gemini-api-docs: https://ai.google.dev/gemini-api/docs/music-generation
  prompt-guide: https://deepmind.google/models/lyria/prompt-guide/
  colab-quickstart: https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Lyria.ipynb
---

# Lyria 3 Prompting Skill

Generate music with Google's Lyria 3 family of models. Choose your model, craft a
structured prompt, call the API, and handle the audio + lyrics response.

## Choose a model

| Model | Use case | Max length |
|---|---|---|
| `lyria-3-clip-preview` | Short clips, loops, experiments | ~30 seconds |
| `lyria-3-pro-preview` | Full songs with verse/chorus/bridge structure | up to 3 minutes |

## Prompt construction

Build prompts from these elements — add as many as needed:

1. **Genre / era** – e.g. `early 90s hip-hop`, `2000s pop`, `K-pop with Motown edge`
2. **Tempo / energy** – e.g. `slow ballad`, `fast drum and bass`, `120 BPM driving pulse`
3. **Instruments** – e.g. `acoustic guitar, cello, ambient pads`, `80s synth over 1950s jazz`
4. **Mood / emotion** – e.g. `uplifting and expansive`, `melancholic and introspective`
5. **Dynamics / structure** – e.g. `quiet piano builds to explosive chorus, then fades`
6. **Vocals** – e.g. `male baritone`, `female soprano`, `soulful R&B voice`, or `instrumental only`
7. **Lyrics** – prepend `Lyrics:` before any lines you want sung; use `(echo)` for backing vocals
8. **Avoid** – e.g. `avoid harsh distortion, avoid busy percussion`

### Minimal prompt (text-to-music)
```
A cheerful acoustic folk song about a sunrise in the mountains.
```

### Structured prompt (full song)
```
Genre: cinematic electronic
Mood: uplifting, expansive, hopeful
Tempo: medium-fast, driving pulse at ~110 BPM
Instrumentation: analog synth arpeggios, deep sub bass, wide pads, light percussion
Vocals: clear female lead, breathy and ethereal
Structure: atmospheric intro → verse → rising chorus → bridge with half-time feel → final chorus → soft outro
Avoid: harsh distortion, overly busy percussion
```

### Prompt with custom lyrics
```
A soulful R&B song in the style of early 2000s neo-soul.
Instrumentation: Rhodes piano, brushed drums, warm bass.

Lyrics:
Walking through the city lights (city lights)
Every step I take feels right (feels right)
```

### Image-to-music
Supply an image part alongside a text prompt — Lyria infers mood, setting, and energy
from the visual. See [references/REFERENCE.md](references/REFERENCE.md#image-to-music).

## Calling the API

### Via Gemini API (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="lyria-3-pro-preview",
    contents="A cheerful acoustic folk song about a sunrise in the mountains.",
    config=types.GenerateContentConfig(
        response_modalities=["Audio", "Text"]
    ),
)

lyrics = response.parts[0].text          # timestamped lyrics
audio  = response.parts[-1].inline_data  # audio/mpeg bytes
```

Run the full example: `scripts/generate.py`

### Via OpenRouter (OpenAI-compatible)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY",
)

response = client.chat.completions.create(
    model="google/lyria-3-pro-preview",
    messages=[{"role": "user", "content": "An upbeat jazz song for a coffee shop morning."}],
)
```

## Saving the audio

```python
import base64, pathlib

audio_b64 = response.parts[-1].inline_data.data
audio_bytes = base64.b64decode(audio_b64) if isinstance(audio_b64, str) else audio_b64
pathlib.Path("output.mp3").write_bytes(audio_bytes)
```

## Common edge cases

- **Instrumental only** — include `No vocals. Instrumental only.` in the prompt.
- **Specific language** — specify `Lyrics in Spanish` or `Sing in Japanese`.
- **Timestamped lyrics** — the API returns `[seconds:] lyric line` format automatically.
- **Clip vs Pro** — use `lyria-3-clip-preview` for fast iteration; switch to `lyria-3-pro-preview` for full-length output.
- **Cost** — `lyria-3-pro-preview` via OpenRouter costs $0.08 per song.

See [references/REFERENCE.md](references/REFERENCE.md) for detailed guidance on
timestamped prompts, image-to-music, and advanced vocal techniques.
