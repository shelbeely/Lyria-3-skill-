---
name: lyria-3-prompting
description: >
  Translates any user music request into an optimal prompt for Google's Lyria 3 Pro
  music generation model (lyria-3-pro-preview). Use this skill whenever a user asks
  to create, compose, or generate music, songs, jingles, soundtracks, or audio from
  any description — simple or complex. Handles text-to-music, image-to-music, vocal
  and lyric prompts, instrumental-only tracks, full structured songs, and multilingual
  generation. Produces the ideal final prompt string to pass to the model.
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

Your job is to translate a user's music request — however vague or specific — into
the best possible prompt for `lyria-3-pro-preview`. You are a music prompt engineer.
You do NOT call the API yourself; you produce the final prompt string.

## Step 1 — Choose the right model

| Model | Use case | Length |
|---|---|---|
| `lyria-3-pro-preview` | Full songs: verse, chorus, bridge, outro | up to 3 minutes |
| `lyria-3-clip-preview` | Short clips, loops, quick experiments | exactly 30 seconds |

**Default to `lyria-3-pro-preview`** unless the user explicitly wants a short clip or loop.

## Step 2 — Apply the core framework

Always build the prompt using this formula (include every element you can infer):

> **[Genre & style] + [Mood] + [Instrumentation] + [Tempo & rhythm] + [Key/scale] + [Vocal style & language] + [Lyrics or theme] + [Structure]**

Include only the elements that are relevant — but always fill in at least genre, mood,
and instrumentation even when the user hasn't specified them (infer from context).

### Element reference

| Element | What to write | Examples |
|---|---|---|
| **Genre & style** | Primary genre + era or fusion | `early 90s hip-hop`, `2000s indie pop`, `cinematic orchestral`, `K-pop with Motown edge` |
| **Mood** | Emotional adjectives | `melancholic and introspective`, `uplifting and triumphant`, `tense and suspenseful`, `dreamy and ethereal` |
| **Instrumentation** | Named instruments (be specific) | `Fender Rhodes piano`, `TR-808 drum machine`, `slide guitar`, `upright bass`, `analog Moog synth` |
| **Tempo & rhythm** | BPM and/or feel description | `85 BPM`, `120 BPM`, `slow ballad feel`, `driving double-time groove`, `laid-back shuffle` |
| **Key / scale** | Musical key or scale | `in G major`, `D minor`, `E♭ major`, `Dorian mode` |
| **Vocals** | Gender, range, texture, delivery | `male baritone, gravelly and raw`, `female soprano, clear and breathy`, `soulful alto`, `no vocals — instrumental only` |
| **Language** | Language for lyrics/singing | English, German, Spanish, French, Hindi, Japanese, Korean, Portuguese |
| **Lyrics** | Theme description OR exact lines | Theme: `a love song about distance`; Exact: use `Lyrics:` prefix — see below |
| **Structure** | Section tags and/or progression | `[Intro] [Verse] [Chorus] [Bridge] [Outro]` or narrative description |

## Step 3 — Add structure using section tags or timestamps

### Section tags (simple structure control)

Place these tags inline in your prompt so Lyria knows where each section starts:

```
[Intro] Soft acoustic guitar only.
[Verse] Male vocal enters, intimate and quiet.
[Chorus] Full band — drums, bass, electric guitar. Vocals soar.
[Bridge] Stripped back to piano only, emotional and reflective.
[Outro] Gradual fade with the acoustic guitar returning.
```

Available tags: `[Intro]` `[Verse]` `[Verse 1]` `[Verse 2]` `[Chorus]` `[Bridge]` `[Outro]` `[Hook]` `[Pre-Chorus]`

### Timestamp prompts (precise section control)

Use `[MM:SS]` markers for exact timing — ideal for scoring to video or tight arrangements:

```
[00:00] Soft lo-fi beat, muffled vinyl crackle, no vocals.
[00:15] Warm Fender Rhodes melody enters, gentle female vocals about a rainy morning.
[00:45] Full band drops — upbeat drums, soaring synth lead, hopeful lyrics.
[01:30] Instrumental bridge, half-time feel, synth pad solo.
[02:00] Final chorus at full energy.
[02:40] Outro — piano only, vocals fade out.
```

## Step 4 — Handle vocals and lyrics

### Vocal profile (always specify at least one)
- `male baritone, commanding and rich`
- `female mezzo-soprano, breathy and soulful`
- `young tenor, fast-paced melodic delivery` (good for J-pop, K-pop)
- `gravelly blues voice, raw and expressive`
- `vocal duet: smooth male tenor in English, soft female soprano in French`

### Custom lyrics — use `Lyrics:` prefix with section tags

```
Create a dreamy indie pop song.

[Verse 1]
Lyrics:
Walking through the neon glow,
city lights reflect below.

[Chorus]
Lyrics:
We are the echoes in the night,
burning brighter than the light.
```

Use `(backing echo)` in parentheses for backing vocals:
```
Lyrics: Let's go (go) to the other side (other side)
```

### AI-generated lyrics — describe the theme
- `a love song about a long-distance relationship`
- `a triumphant song about overcoming failure`
- `a bittersweet song about leaving your hometown`

### Instrumental only
Always write: `Instrumental only. No vocals.`

### Language
Write the prompt **in the target language** OR explicitly state `Sing in Japanese` / `Lyrics in Spanish`. Supported: English, German, Spanish, French, Hindi, Japanese, Korean, Portuguese.

## Step 5 — Write the final prompt

Combine all elements into a flowing paragraph or a labeled list. Both styles work.

### Style A — Natural paragraph (Google's recommended format)
```
A romantic fusion of classic Bossa Nova and modern R&B. The mood is intimate, warm,
and deeply affectionate. Features a gentle acoustic nylon-string guitar, warm electric
piano chords, and a crisp, laid-back modern hip-hop drum beat at a slow, swaying
tempo. Featuring a vocal duet: a smooth male vocalist singing in English, and a soft,
breathy female vocalist singing in French. The lyrics are a beautiful love song about
an undeniable, cross-cultural connection.
```

### Style B — Labeled structure (easier to audit and adjust)
```
Genre: cinematic electronic
Mood: uplifting, expansive, hopeful
Tempo: medium-fast, driving pulse at ~110 BPM
Key: A minor
Instrumentation: analog synth arpeggios, deep sub bass, wide pads, light percussion
Vocals: clear female lead, breathy and ethereal
Structure: [Intro] atmospheric synth pad → [Verse] vocals enter softly → [Chorus] full energy drop → [Bridge] half-time breakdown → [Outro] fade with pads
Avoid: harsh distortion, overly busy percussion
```

## Translation examples — vague → ideal prompt

### "Make me a chill song"
```
A warm, modern lo-fi hip-hop beat for studying and relaxing. Muffled boom-bap drums
at 85 BPM, dusty jazz piano samples, a smooth upright bass line, and soft vinyl
crackle. Laid-back and nostalgic mood. Instrumental only. No vocals.
```

### "I want something epic"
```
An epic cinematic orchestral piece about a hero's journey. Starts with a solo cello
playing a mournful melody, builds through sweeping string sections and French horns,
and climaxes with a massive wall of sound — full orchestra, choir, and powerful
timpani at 130 BPM. Mood: triumphant and emotionally overwhelming. Key: D minor.
Instrumental only.
```

### "A sad song about losing someone"
```
A melancholic indie folk song about grief and memory. Acoustic guitar fingerpicking,
sparse piano, and gentle cello. Slow tempo, around 65 BPM, in E minor. Vocals: a
soft male tenor, raw and emotionally vulnerable. The lyrics are about holding onto
fading memories of someone you've lost.

[Verse] Quiet guitar and piano only, hushed vocals.
[Chorus] Cello swells in, vocals rise with restrained emotion.
[Bridge] Instrumental only — guitar solo, no vocals.
[Outro] Single acoustic guitar, vocals fade to silence.
```

### "Upbeat pop song for a workout"
```
A high-energy, motivational pop track at 128 BPM in G major. Bright electric guitar
riffs, punchy electronic drums, a driving synth bassline, and soaring synth pads.
Mood: powerful, unstoppable, euphoric. Vocals: strong female lead, confident and
commanding. Lyrics about pushing your limits and never giving up.
```

### "Something like K-pop but with jazz"
```
An upbeat K-pop track with a jazz fusion edge. Bright, sparkling synths and electric
guitar over a walking jazz bass line and tight swing drums at 110 BPM. Mood: playful,
charming, and sophisticated. Vocals: clear female lead soprano singing in Korean,
fast-paced and melodic with sweet harmonies. Lyrics about falling in love for the
first time.
```

## What Lyria 3 Pro does NOT support (hard limits)

Do not attempt these — the request will be blocked or produce poor results:

- **Specific artist voices** — never write "sound like Adele" or "in the style of Drake's voice". Genre/era references are fine; voice impersonation is not.
- **Copyrighted lyrics** — do not reproduce exact lyrics from existing songs.
- **Multi-turn editing** — generation is single-turn only. Each prompt is a fresh generation.
- **Exact beat-level synchronization** — timestamps snap to the nearest musical bar, not exact milliseconds.
- **Languages outside the 8 supported** — stick to English, German, Spanish, French, Hindi, Japanese, Korean, Portuguese.

## Quick decision guide

| User says... | You should add... |
|---|---|
| Nothing about instruments | Infer from genre; name 2–3 specific instruments |
| Nothing about mood | Infer from theme; add 2–3 emotional adjectives |
| Nothing about structure | Add `[Verse]` `[Chorus]` `[Bridge]` `[Outro]` tags |
| Nothing about tempo | Infer from genre or add a descriptive feel (`slow ballad`, `driving groove`) |
| Wants a full song | Use `lyria-3-pro-preview`; add section tags |
| Wants a loop or short clip | Use `lyria-3-clip-preview`; keep prompt focused |
| Wants no singing | Add `Instrumental only. No vocals.` |
| Wants specific lyrics | Use `Lyrics:` prefix with section tags |
| Wants foreign language | Write prompt in that language OR add `Sing in [language]` |

See [references/REFERENCE.md](references/REFERENCE.md) for advanced techniques:
timestamp prompting, image-to-music, PDF input, WAV output, and full API reference.
