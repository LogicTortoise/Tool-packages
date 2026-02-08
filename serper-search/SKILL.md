---
name: serper-search
description: "Search the web using Serper.dev Google Search API. Supports web, image, news, and video search. Use when the user asks to search Google, find web pages, look up news, search for images, or needs real-time search results from the internet. Triggers on keywords like 'search', 'Google', 'look up', 'find online', 'news about', 'search images', 'web search', 'serper'."
---

# Serper Search

Search Google via the Serper.dev API. Supports web, image, news, and video search with country/language/time filtering.

## Prerequisites

Set the `SERPER_API_KEY` environment variable before use:

```bash
export SERPER_API_KEY=your_api_key_here
```

## Quick Start - CLI Script

Run the bundled script (Node.js 18+, no dependencies needed):

```bash
node scripts/serper-search.mjs "your query"
```

### Common Examples

```bash
# Web search
node scripts/serper-search.mjs "Node.js best practices" -n 5

# Image search
node scripts/serper-search.mjs "sunset landscape" -t images -n 5

# News search (last week)
node scripts/serper-search.mjs "AI technology" -t news --tbs qdr:w

# Video search
node scripts/serper-search.mjs "javascript tutorial" -t videos

# Chinese results
node scripts/serper-search.mjs "人工智能" -g cn -l zh-cn

# Raw JSON output
node scripts/serper-search.mjs "python tips" -j
```

### Script Options

| Flag | Description | Default |
|------|-------------|---------|
| `-t, --type` | search / images / news / videos | search |
| `-n, --num` | Result count (max 100) | 10 |
| `-g, --gl` | Country code (us, cn, jp) | - |
| `-l, --hl` | Language (en, zh-cn) | - |
| `--tbs` | Time: qdr:d / qdr:w / qdr:m / qdr:y | - |
| `-j, --json` | Output raw JSON | false |

## Inline Usage (Node.js)

For use within code without the CLI:

```javascript
const res = await fetch('https://google.serper.dev/search', {
  method: 'POST',
  headers: { 'X-API-KEY': process.env.SERPER_API_KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({ q: 'your query', num: 10 }),
});
const data = await res.json();
// data.organic[].title / .link / .snippet
```

## Inline Usage (cURL)

```bash
curl -X POST https://google.serper.dev/search \
  -H 'X-API-KEY: YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"q": "query", "num": 10}'
```

## Response Key Fields

- **Web**: `data.organic[]` -> `.title`, `.link`, `.snippet`
- **Images**: `data.images[]` -> `.title`, `.imageUrl`, `.link`
- **News**: `data.news[]` -> `.title`, `.link`, `.source`, `.date`
- **Videos**: `data.videos[]` -> `.title`, `.link`, `.channel`

## Notes

- Free tier: 2,500 searches/month, resets on 1st
- The script uses Node.js built-in `fetch` (requires Node 18+), no `npm install` needed
- For full API parameters and all endpoints, see [references/api-reference.md](references/api-reference.md)
