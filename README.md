# Lyria 3 Prompting Skill

An [Agent Skills](https://agentskills.io) package for generating music with
Google's **Lyria 3** family of models (`lyria-3-pro-preview` / `lyria-3-clip-preview`)
via the Gemini API or OpenRouter.

## Skill

The skill lives in [`lyria-3-prompting/`](lyria-3-prompting/):

| File | Purpose |
|---|---|
| [`lyria-3-prompting/SKILL.md`](lyria-3-prompting/SKILL.md) | Skill instructions + quick-start API examples |
| [`lyria-3-prompting/references/REFERENCE.md`](lyria-3-prompting/references/REFERENCE.md) | Detailed prompt guide, image-to-music, lyrics, timestamped prompts |
| [`lyria-3-prompting/scripts/generate.py`](lyria-3-prompting/scripts/generate.py) | CLI script for generating a song via the Gemini Python SDK |

## Quick start

```bash
pip install 'google-genai>=1.62.0'
export GEMINI_API_KEY=your_key_here
python lyria-3-prompting/scripts/generate.py "An upbeat jazz song for a coffee shop morning."
```

## References

- OpenRouter model page: https://openrouter.ai/google/lyria-3-pro-preview
- Colab quickstart: https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Lyria.ipynb
- Official prompt guide: https://deepmind.google/models/lyria/prompt-guide/
- Agent Skills spec: https://agentskills.io/specification
