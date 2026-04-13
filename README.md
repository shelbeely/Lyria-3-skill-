# Lyria 3 Prompting Skill

An [Agent Skills](https://agentskills.io) package for generating music with
Google's **Lyria 3** family of models (`lyria-3-pro-preview` / `lyria-3-clip-preview`)
via the Gemini API or OpenRouter.

## Install

```bash
npx skills add shelbeely/Lyria-3-skill-
```

## Skill

The skill lives in [`skills/lyria-3-prompting/`](skills/lyria-3-prompting/):

| File | Purpose |
|---|---|
| [`skills/lyria-3-prompting/SKILL.md`](skills/lyria-3-prompting/SKILL.md) | Skill instructions + quick-start API examples |
| [`skills/lyria-3-prompting/references/REFERENCE.md`](skills/lyria-3-prompting/references/REFERENCE.md) | Detailed prompt guide, image-to-music, lyrics, timestamped prompts |
| [`skills/lyria-3-prompting/scripts/generate.py`](skills/lyria-3-prompting/scripts/generate.py) | CLI script for generating a song via the Gemini Python SDK |

## Quick start

```bash
pip install 'google-genai>=1.62.0'
export GEMINI_API_KEY=your_key_here
python skills/lyria-3-prompting/scripts/generate.py "An upbeat jazz song for a coffee shop morning."
```

## References

- OpenRouter model page: https://openrouter.ai/google/lyria-3-pro-preview
- Colab quickstart: https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Lyria.ipynb
- Official prompt guide: https://deepmind.google/models/lyria/prompt-guide/
- Agent Skills spec: https://agentskills.io/specification
