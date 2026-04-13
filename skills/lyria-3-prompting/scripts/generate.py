#!/usr/bin/env python3
"""
generate.py — Generate a song with Lyria 3 via the Gemini API.

Usage:
    export GEMINI_API_KEY=your_key_here
    python generate.py "Your prompt here." output.mp3
    python generate.py "An ambient track." output.wav --format wav

Requirements:
    pip install google-genai>=1.62.0
"""

import argparse
import os
import pathlib
import sys


def generate(prompt: str, output_path: str, model: str = "lyria-3-pro-preview", fmt: str = "mp3") -> None:
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

    config_kwargs = dict(response_modalities=["AUDIO", "TEXT"])
    if fmt == "wav":
        if model == "lyria-3-pro-preview":
            config_kwargs["response_mime_type"] = "audio/wav"
        else:
            print("Warning: WAV output is only supported by lyria-3-pro-preview; falling back to MP3.")
            fmt = "mp3"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    lyrics = []
    audio_data = None
    for part in response.parts:
        if part.text is not None:
            lyrics.append(part.text)
        elif part.inline_data is not None:
            audio_data = part.inline_data.data

    if lyrics:
        print(f"\nLyrics:\n{''.join(lyrics)}")

    if audio_data:
        pathlib.Path(output_path).write_bytes(audio_data)
        print(f"\nAudio saved to: {output_path}")
    else:
        sys.exit("No audio data returned in response.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate music with Lyria 3.")
    parser.add_argument("prompt", help="Text prompt describing the song")
    parser.add_argument("output", nargs="?", default="output.mp3", help="Output audio file (default: output.mp3)")
    parser.add_argument(
        "--model",
        default="lyria-3-pro-preview",
        choices=["lyria-3-pro-preview", "lyria-3-clip-preview"],
        help="Lyria model to use (default: lyria-3-pro-preview)",
    )
    parser.add_argument(
        "--format",
        default="mp3",
        choices=["mp3", "wav"],
        dest="fmt",
        help="Output audio format; wav only supported by lyria-3-pro-preview (default: mp3)",
    )
    args = parser.parse_args()
    generate(args.prompt, args.output, args.model, args.fmt)


if __name__ == "__main__":
    main()
