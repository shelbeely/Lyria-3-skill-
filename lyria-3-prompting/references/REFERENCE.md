# Lyria 3 — Detailed Reference

## Models

| Model ID | Description |
|---|---|
| `lyria-3-clip-preview` | 30-second clips; ideal for loops and experiments |
| `lyria-3-pro-preview` | Full songs up to 3 minutes; verse/chorus/bridge structure, vocals |

OpenRouter model id: `google/lyria-3-pro-preview`  
OpenRouter page: https://openrouter.ai/google/lyria-3-pro-preview  
Gemini API docs: https://ai.google.dev/gemini-api/docs/music-generation  

---

## Prompt construction

### Genre / era

Pick a genre and era for a consistent sonic palette:
- `early 90s hip-hop`
- `2000s pop`
- `1950s jazz`
- `K-pop with a Motown edge`
- `classical violins fused into a funk track`

### Tempo

Set tempo explicitly or implicitly through genre:
- `slow ballad`
- `fast drum and bass`
- `120 BPM`
- `medium-fast driving pulse`

### Instruments

Lyria picks instruments automatically from genre if unspecified. Override with:
- `acoustic guitar, cello, ambient pads`
- `80s synth added to a 1950s jazz band`
- `no guitar — only brass and strings`

### Dynamics and structure

Describe how the music evolves:
- `quiet piano intro builds into an explosive chorus`
- `instrumental bridge with half-time feel`
- `vocals get softer and fade out over the last 30 seconds`

### Mood / emotion

- `uplifting and expansive`
- `melancholic and introspective`
- `tense and suspenseful`
- `playful and whimsical`

---

## Prompting vocals and lyrics

### Vocal profile

Describe voice characteristics:
- `male baritone, commanding and rich`
- `female soprano, clear and high`
- `gravelly blues voice`
- `soulful R&B voice, breathy`

### Custom lyrics

Prepend `Lyrics:` to the lines you want sung:

```
Lyrics:
Walking through the city lights (city lights)
Every step I take feels right (feels right)
```

Use parentheses `(echo words)` for backing-vocal echoes.

### AI-generated lyrics

Let Lyria write lyrics by describing the theme:
- `a love song about distance`
- `a song about overcoming failure`
- `a new happy birthday song for my best friend`

### Instrumental-only

```
Instrumental only. No vocals.
```

### Multiple languages

```
Sing in Spanish.
Lyrics in Japanese.
```

---

## Image-to-music

Supply an image part alongside a text description. Lyria interprets:
- **Subject** — who or what is depicted; mood conveyed
- **Location** — urban, nature, exotic landscape
- **Activity** — posed portrait, action shot, etc.

```python
import pathlib
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

image_bytes = pathlib.Path("photo.jpg").read_bytes()

response = client.models.generate_content(
    model="lyria-3-pro-preview",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        "Generate a soundtrack that matches the mood and setting of this image.",
    ],
    config=types.GenerateContentConfig(
        response_modalities=["Audio", "Text"]
    ),
)
```

Good image sources: holiday photos, pet photos, artwork, scientific diagrams,
historical paintings, cartoons, illustrations.

---

## Timestamped prompts

Control song structure explicitly by specifying what happens at each timestamp:

```
[0:00] Gentle acoustic guitar intro, no vocals
[0:20] Female vocal enters, soft and intimate
[0:50] Full band enters — drums, bass, electric guitar
[1:30] Instrumental bridge, tempo doubles
[2:00] Final chorus, full dynamics
[2:40] Outro, vocals fade, guitar solo closes
```

The model will also return timestamped lyrics in the response:
```
[0.0:] The air is still and cold up here
[4.8:] The mountaintops are sharp and clear
[9.6:] And then a streak of gentle gold
```

---

## Experimenting

### Musicality
- Prompt counterpoints and harmonies
- Layer unusual instruments into genre expectations
- Ask for specific chord progressions or scales

### Vocals
- Describe vocal patterns: `fast-paced delivery`, `laid-back groove`
- Request call-and-response patterns
- Layer multiple vocal styles: `lead soprano over gospel choir`

### Images
- Try wildly different images to hear how Lyria interprets them
- Pair abstract art with genre prompts for unexpected results

---

## Parsing API responses (Gemini)

```python
# response.parts[0].text  → timestamped lyrics
# response.parts[-1].inline_data.data  → audio bytes (audio/mpeg)

import base64, pathlib

lyrics = response.parts[0].text
audio_data = response.parts[-1].inline_data.data

# inline_data.data may already be bytes
if isinstance(audio_data, str):
    audio_data = base64.b64decode(audio_data)

pathlib.Path("output.mp3").write_bytes(audio_data)
print(lyrics)
```

---

## Pricing

| Provider | Cost |
|---|---|
| OpenRouter (`google/lyria-3-pro-preview`) | $0.08 per song |
| Gemini API (direct) | See https://ai.google.dev/pricing |

---

## Further reading

- Quickstart notebook: https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Lyria.ipynb
- Official prompt guide: https://deepmind.google/models/lyria/prompt-guide/
- Gemini API music generation docs: https://ai.google.dev/gemini-api/docs/music-generation
- OpenRouter model page: https://openrouter.ai/google/lyria-3-pro-preview
