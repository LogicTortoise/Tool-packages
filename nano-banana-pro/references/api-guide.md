# Nano Banana Pro API Reference

## Model Info

- **Model ID**: `gemini-3-pro-image-preview`
- **Provider**: Google Vertex AI
- **Pricing**: $2 text input / $0.134 per image output
- **Context**: 65k input / 32k output tokens

## GCP Environment

- **Project**: `pago-427611`
- **Location**: `global` (image gen requires global, not regional)
- **Auth**: Application Default Credentials (`gcloud auth application-default login`)
- **Proxy**: `http://127.0.0.1:7890` (if needed)
- **SDK**: `google-genai>=1.62.0` (pip install --upgrade google-genai). Versions <1.62.0 lack `ImageConfig`.

## API Patterns

### Text-to-Image

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="pago-427611", location="global")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A watercolor painting of a mountain landscape",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # Options: 1:1, 3:4, 4:3, 9:16, 16:9, 21:9
            # image_size="2K",    # Options: 1K, 2K
        ),
    ),
)

for part in response.candidates[0].content.parts:
    if getattr(part, "thought", False):
        continue
    if part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
    elif part.text:
        print(part.text)
```

### Image Editing

```python
from pathlib import Path

image_bytes = Path("input.png").read_bytes()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        "Change the background to a sunset beach",
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(image_size="1K"),
    ),
)
```

### With Google Search Grounding

```python
google_search = types.Tool(google_search=types.GoogleSearch())

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Visualize the current weather in Tokyo as an infographic",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="21:9"),
        tools=[google_search],
    ),
)
```

## Parameters

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| aspect_ratio | 1:1, 3:4, 4:3, 9:16, 16:9, 21:9 | 1:1 | Aspect ratio of generated image |
| image_size | 1K, 2K | 1K | Output resolution |
| response_modalities | ["IMAGE", "TEXT"] | - | Must include IMAGE for generation |

## Error Handling

- `FinishReason.STOP` = success
- `FinishReason.SAFETY` = content policy violation, rephrase prompt
- `FinishReason.RECITATION` = potential copyright issue
- No candidates = prompt blocked entirely

## Limitations

- No person face generation (safety filter)
- Text in images: Nano Banana Pro excels at rendering legible text
- Max ~32k output tokens per request
