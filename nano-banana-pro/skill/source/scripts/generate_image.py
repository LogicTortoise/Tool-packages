#!/usr/bin/env python3
"""Nano Banana Pro (Gemini 3 Pro Image) - Image generation via Vertex AI."""

import argparse
import base64
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types


def create_client(project: str | None = None, location: str = "global") -> genai.Client:
    project = project or os.environ.get("GOOGLE_CLOUD_PROJECT", "pago-427611")
    return genai.Client(vertexai=True, project=project, location=location)


def generate_image(
    prompt: str,
    *,
    output: str = "output.png",
    aspect_ratio: str = "1:1",
    image_size: str | None = None,
    project: str | None = None,
    input_image: str | None = None,
) -> str:
    """Generate or edit an image and save to file. Returns the output path."""
    client = create_client(project=project)
    model = "gemini-3-pro-image-preview"

    contents = []
    if input_image:
        img_path = Path(input_image)
        if not img_path.exists():
            raise FileNotFoundError(f"Input image not found: {input_image}")
        suffix = img_path.suffix.lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".webp": "image/webp", ".gif": "image/gif"}
        mime_type = mime_map.get(suffix, "image/png")
        contents.append(types.Part.from_bytes(data=img_path.read_bytes(), mime_type=mime_type))

    contents.append(prompt)

    img_config = types.ImageConfig(aspect_ratio=aspect_ratio)
    if image_size:
        img_config = types.ImageConfig(aspect_ratio=aspect_ratio, image_size=image_size)

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
            image_config=img_config,
        ),
    )

    if not response.candidates or response.candidates[0].finish_reason != types.FinishReason.STOP:
        reason = response.candidates[0].finish_reason if response.candidates else "NO_CANDIDATES"
        raise RuntimeError(f"Generation failed: {reason}")

    out_path = Path(output)
    text_parts = []
    for part in response.candidates[0].content.parts:
        if getattr(part, "thought", False):
            continue
        if part.inline_data:
            out_path.write_bytes(part.inline_data.data)
        elif part.text:
            text_parts.append(part.text)

    if text_parts:
        print("\n".join(text_parts))

    if out_path.exists():
        print(f"Image saved: {out_path}")
    else:
        raise RuntimeError("No image data in response")

    return str(out_path)


def main():
    parser = argparse.ArgumentParser(description="Generate images with Nano Banana Pro (Gemini 3 Pro Image)")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("-o", "--output", default="output.png", help="Output file path (default: output.png)")
    parser.add_argument("-a", "--aspect-ratio", default="1:1",
                        choices=["1:1", "3:4", "4:3", "9:16", "16:9", "21:9"],
                        help="Aspect ratio (default: 1:1)")
    parser.add_argument("-s", "--image-size", choices=["1K", "2K"],
                        help="Image size/resolution")
    parser.add_argument("-i", "--input-image", help="Input image for editing tasks")
    parser.add_argument("-p", "--project", help="GCP project ID (default: pago-427611)")
    args = parser.parse_args()

    try:
        generate_image(
            args.prompt,
            output=args.output,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            project=args.project,
            input_image=args.input_image,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
