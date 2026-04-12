# Lyria 3 — Detailed Reference

## Models

| Model ID | Description | Output length | Audio format |
|---|---|---|---|
| `lyria-3-clip-preview` | Short clips, loops, rapid prototyping | Exactly 30 seconds | MP3 |
| `lyria-3-pro-preview` | Full songs: verse/chorus/bridge/outro | Up to ~3 minutes | MP3 or WAV |

- **Output audio**: 44.1 kHz stereo (not 48 kHz as previously noted)
- **SynthID watermark**: all outputs are imperceptibly watermarked; does not affect listening
- **C2PA metadata**: cryptographically signed provenance metadata embedded in all outputs
- OpenRouter: `google/lyria-3-pro-preview` — $0.08/song — https://openrouter.ai/google/lyria-3-pro-preview
- Gemini API docs: https://ai.google.dev/gemini-api/docs/music-generation

---

## Supported vocal languages

English, German, Spanish, French, Hindi, Japanese, Korean, Portuguese

To target a language: write the prompt **in that language**, or add `Sing in Japanese` / `Lyrics in French` explicitly.

---

## Section tags

Use these tags inline in the prompt to define song structure. Lyria will honor them:

```
[Intro] Soft acoustic guitar only, no drums.
[Verse 1] Male vocal enters, quiet and intimate.
[Pre-Chorus] Energy builds — bass comes in.
[Chorus] Full band drops. Vocals soar with harmonies.
[Verse 2] Same as verse 1 but with added strings.
[Bridge] Stripped to piano only, emotional and sparse.
[Hook] Short melodic motif repeated.
[Outro] Gradual fade, return to acoustic guitar.
```

Available: `[Intro]` `[Verse]` `[Verse 1]` `[Verse 2]` `[Pre-Chorus]` `[Chorus]` `[Bridge]` `[Hook]` `[Outro]`

---

## Timestamp prompting

Use `[MM:SS]` markers to assign specific instructions to moments in the song. Timestamps snap to the nearest musical bar — do not expect sample-accurate sync.

```
[00:00] Begin with a massive gospel choir, powerful and uplifting.
[00:15] Heavy hip-hop drums and deep 808 bass drop in.
[00:30] Male rapper delivers a confident verse; choir punctuates his lines.
[01:10] Transition into a triumphant chorus — gospel choir at full volume, brass horns.
[01:50] Strip back to Hammond B3 organ; quiet emotional bridge, soft choir hums.
[02:10] Full beat and choir return at maximum energy for the final chorus.
[03:00] End on a sustained, resonant choir chord.
```

---

## Custom lyrics format

Use `Lyrics:` before each section. Use `[Section]` tags to label parts:

```
Create a dreamy indie pop song.

[Verse 1]
Lyrics:
Walking through the neon glow,
city lights reflect below,
every shadow tells a story,
every corner, fading glory.

[Chorus]
Lyrics:
We are the echoes in the night,
burning brighter than the light,
hold on tight, don't let me go,
we are the echoes down below.

[Verse 2]
Lyrics:
Footsteps lost on empty streets,
rhythms sync to heartbeats,
whispers carried by the breeze,
dancing through the autumn leaves.
```

Backing vocals — use parentheses:
```
Lyrics: Let's go (go) to the other side (other side)
```

---

## Prompt construction — element details

### Genre & era
- `early 90s hip-hop`, `2000s pop`, `1950s jazz`, `K-pop with a Motown edge`
- `classical violins fused into a funk track`, `80s synthwave`, `2020s indie folk`
- Genre blends work well: `jazz fusion`, `lo-fi hip-hop`, `cinematic orchestral`, `afrobeats with reggaeton rhythm`

### Tempo & rhythm
- Explicit BPM: `85 BPM`, `120 BPM`, `140 BPM`
- Descriptive: `slow ballad`, `fast drum and bass`, `medium-fast driving pulse`, `laid-back shuffle`, `double-time groove`

### Instruments (be specific — generic names produce generic results)
- Piano types: `Fender Rhodes`, `upright piano`, `grand piano`, `honky-tonk piano`, `prepared piano`
- Guitar types: `acoustic nylon-string guitar`, `slide guitar`, `Stratocaster electric guitar`, `12-string acoustic`
- Bass: `upright bass`, `slap bass`, `fretless bass`, `synth bass`, `TR-808 bass`
- Drums: `TR-808 drum machine`, `brushed jazz kit`, `boom-bap drums`, `live rock kit`, `hand percussion`
- Synths: `analog Moog synth`, `Oberheim pads`, `DX7 FM synth`, `modular synth arpeggios`
- Brass/strings: `French horns`, `string quartet`, `solo cello`, `gospel choir`, `Hammond B3 organ`

### Key / scale
Lyria honors musical key and scale specifications:
- Major keys: `in G major`, `in C major`, `in A♭ major`
- Minor keys: `in D minor`, `in E minor`, `in B minor`
- Modes: `Dorian mode`, `Mixolydian`, `Lydian`

### Mood descriptors
- Energy: `high-energy`, `calm`, `intense`, `driving`, `relaxed`, `explosive`
- Emotion: `melancholic`, `triumphant`, `nostalgic`, `anxious`, `euphoric`, `bittersweet`, `ethereal`, `raw`
- Atmosphere: `cinematic`, `intimate`, `vast and epic`, `lo-fi and warm`, `dark and brooding`

### Vocal profile
- Gender/range: `male baritone`, `female soprano`, `young tenor`, `mezzo-soprano`, `countertenor`
- Texture: `gravelly`, `breathy`, `smooth`, `soulful`, `raw`, `polished`, `rich and warm`
- Style: `rapping`, `spoken word`, `gospel belting`, `opera`, `whispered`, `call-and-response`
- Dynamics: `starts confident, gets quieter and more emotional as the song progresses`
- Duets: `vocal duet: smooth male tenor in English, soft female soprano in French`

---

## Multimodal inputs

### Images (up to 10)
Upload images to establish visual mood. Lyria interprets subject, location, and emotional atmosphere:

```python
from PIL import Image
image = Image.open("desert_sunset.jpg")

response = client.models.generate_content(
    model="lyria-3-pro-preview",
    contents=[
        "An atmospheric ambient track inspired by the mood and colors in this image.",
        image,
    ],
)
```

Good sources: nature photography, cityscapes, artwork, historical paintings, portraits, scientific diagrams.

### PDF inputs
PDF documents can also be used as input context alongside text prompts via the Gemini API.

---

## Output formats

### MP3 (default)
Both models output MP3 by default.

### WAV (Pro model only)
Request WAV for higher fidelity post-processing:

```python
config=types.GenerateContentConfig(
    response_modalities=["AUDIO", "TEXT"],
    response_mime_type="audio/wav",
)
```

---

## Parsing the API response (Gemini Python SDK)

```python
lyrics = []
audio_data = None

for part in response.parts:
    if part.text is not None:
        lyrics.append(part.text)
    elif part.inline_data is not None:
        audio_data = part.inline_data.data  # already bytes; no base64 decode needed

if lyrics:
    print("Lyrics:\n" + "\n".join(lyrics))

if audio_data:
    with open("output.mp3", "wb") as f:
        f.write(audio_data)
```

Timestamped lyrics format returned:
```
[0.0:] The air is still and cold up here
[4.8:] The mountaintops are sharp and clear
[9.6:] And then a streak of gentle gold
```

---

## Calling the API

### Via Gemini API (Python)
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="lyria-3-pro-preview",
    contents="Your prompt here.",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO", "TEXT"]
    ),
)
```

### Via Interactions API (Gemini — simplified state management)
```python
interaction = client.interactions.create(
    model="lyria-3-pro-preview",
    input="A melancholic jazz fusion track in D minor.",
)
for output in interaction.outputs:
    if output.text:
        print(output.text)
    elif output.inline_data:
        with open("output.mp3", "wb") as f:
            f.write(output.inline_data.data)
```

### Via OpenRouter (OpenAI-compatible)
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY",
)

response = client.chat.completions.create(
    model="google/lyria-3-pro-preview",
    messages=[{"role": "user", "content": "Your prompt here."}],
)
```

---

## Model intelligence

Lyria 3 Pro internally reasons about musical structure (intro, verse, chorus, bridge, etc.)
before generating audio. This ensures structural coherence even without explicit section tags.
Providing section tags or timestamps overrides and directs this reasoning.

---

## Hard limitations

| Limitation | Detail |
|---|---|
| **No artist voice impersonation** | Prompts requesting specific artist voices are blocked by safety filters |
| **No copyrighted lyrics** | Prompts reproducing exact copyrighted lyrics are blocked |
| **Single-turn only** | No multi-turn editing; each generation is independent |
| **Timestamp precision** | Timestamps snap to nearest musical bar, not exact milliseconds |
| **Clip length fixed** | `lyria-3-clip-preview` always produces exactly 30 seconds |
| **Language support** | Only 8 languages supported for vocals |
| **No real-time streaming** | Audio is returned as a complete file, not streamed |

---

## Best practices summary

1. **Iterate with Clip first** — use `lyria-3-clip-preview` to test prompt variations fast; then switch to Pro
2. **Be specific** — vague prompts produce generic results; name instruments, BPM, key, mood
3. **Use section tags** — `[Verse]` `[Chorus]` `[Bridge]` give clear structure
4. **Match language** — write the prompt in the language you want the lyrics in
5. **Separate lyrics from instructions** — use `Lyrics:` prefix and section tags
6. **Infer missing details** — if the user doesn't specify, fill in sensible defaults from genre context

---

## Further reading

- Official prompt guide: https://deepmind.google/models/lyria/prompt-guide/
- Gemini API music generation: https://ai.google.dev/gemini-api/docs/music-generation
- Google Cloud ultimate prompting guide: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro
- Colab quickstart: https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Lyria.ipynb
- OpenRouter model page: https://openrouter.ai/google/lyria-3-pro-preview
