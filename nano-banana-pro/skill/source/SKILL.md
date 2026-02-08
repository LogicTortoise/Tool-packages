---
name: nano-banana-pro
description: Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) model via Vertex AI. Use when the user asks to generate images, create illustrations, edit photos, render text in images, create infographics, or any image generation/editing task. Triggers on keywords like "生成图片", "画", "生图", "image generation", "nano banana", "gemini image".
---

# Nano Banana Pro Image Generation

Generate and edit images via Vertex AI using model `gemini-3-pro-image-preview`.

## Quick Start

Run the bundled script directly:

```bash
python3 scripts/generate_image.py "A watercolor mountain landscape" -o landscape.png -a 16:9
```

### Script Options

```
python3 scripts/generate_image.py <prompt> [options]

Options:
  -o, --output         Output file path (default: output.png)
  -a, --aspect-ratio   1:1 | 3:4 | 4:3 | 9:16 | 16:9 | 21:9 (default: 1:1)
  -s, --image-size     1K | 2K
  -i, --input-image    Input image for editing tasks
  -p, --project        GCP project ID (default: pago-427611)
```

### Examples

```bash
# Text-to-image
python3 scripts/generate_image.py "A cute cat wearing a top hat" -o cat.png

# High resolution, wide aspect
python3 scripts/generate_image.py "Cyberpunk city skyline" -o city.png -a 16:9 -s 2K

# Image editing (provide input image)
python3 scripts/generate_image.py "Change the background to a beach sunset" -i photo.jpg -o edited.png
```

## Inline Usage (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="pago-427611", location="global")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A serene Japanese garden in autumn",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
    ),
)

for part in response.candidates[0].content.parts:
    if getattr(part, "thought", False):
        continue
    if part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

## Key Notes

- **Location must be `global`** — regional endpoints do not support this model
- **Auth**: Uses Application Default Credentials (`gcloud auth application-default login`)
- **Proxy**: Set `http_proxy`/`https_proxy` to `http://127.0.0.1:7890` if needed
- **SDK**: Requires `google-genai` (already installed at `/Users/Hht/Library/Python/3.12/lib/python/site-packages`)
- **Strengths**: Excellent at rendering legible text in images across multiple languages
- **Safety**: Will refuse to generate realistic human faces

For full API parameters and advanced patterns (Google Search grounding, multi-turn editing), see [references/api-guide.md](references/api-guide.md).
