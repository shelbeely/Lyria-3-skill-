#!/usr/bin/env python3
"""
generate.py — Generate a song with Lyria 3 via the Gemini API.

Usage:
    export GEMINI_API_KEY=your_key_here
    python generate.py "An upbeat jazz song for a coffee shop morning." output.mp3

Requirements:
    pip install google-genai>=1.62.0
"""

import argparse
import os
import pathlib
import sys


def generate(prompt: str, output_path: str, model: str = "lyria-3-pro-preview") -> None:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit("Install the SDK first:  pip install 'google-genai>=1.62.0'")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Set the GEMINI_API_KEY environment variable before running.")

    client = genai.Client(api_key=api_key)

    print(f"Model : {model}")
    print(f"Prompt: {prompt}")
    print("Generating …")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Audio", "Text"]
        ),
    )

    lyrics = response.parts[0].text
    audio_data = response.parts[-1].inline_data.data

    if isinstance(audio_data, str):
        import base64
        audio_data = base64.b64decode(audio_data)

    pathlib.Path(output_path).write_bytes(audio_data)
    print(f"\nLyrics:\n{lyrics}")
    print(f"\nAudio saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate music with Lyria 3.")
    parser.add_argument("prompt", help="Text prompt describing the song")
    parser.add_argument("output", nargs="?", default="output.mp3", help="Output MP3 file (default: output.mp3)")
    parser.add_argument(
        "--model",
        default="lyria-3-pro-preview",
        choices=["lyria-3-pro-preview", "lyria-3-clip-preview"],
        help="Lyria model to use (default: lyria-3-pro-preview)",
    )
    args = parser.parse_args()
    generate(args.prompt, args.output, args.model)


if __name__ == "__main__":
    main()
