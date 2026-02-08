# Serper.dev API Reference

## Base URL

`https://google.serper.dev`

## Authentication

All requests require `X-API-KEY` header with the API key.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search` | POST | Web search |
| `/images` | POST | Image search |
| `/news` | POST | News search |
| `/videos` | POST | Video search |
| `/places` | POST | Places search |
| `/shopping` | POST | Shopping search |
| `/autocomplete` | POST | Search autocomplete |

## Common Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query |
| `num` | int | 10 | Results count (max 100) |
| `gl` | string | - | Country code (us, cn, jp, etc.) |
| `hl` | string | - | Language (en, zh-cn, ja, etc.) |
| `page` | int | 1 | Page number |
| `tbs` | string | - | Time filter: `qdr:h`(hour), `qdr:d`(day), `qdr:w`(week), `qdr:m`(month), `qdr:y`(year) |

## Response Formats

### Web Search (`/search`)

```json
{
  "organic": [
    { "title": "...", "link": "...", "snippet": "...", "position": 1 }
  ],
  "answerBox": {},
  "peopleAlsoAsk": [],
  "relatedSearches": []
}
```

### Image Search (`/images`)

```json
{
  "images": [
    { "title": "...", "imageUrl": "...", "link": "...", "source": "...", "thumbnail": "..." }
  ]
}
```

### News Search (`/news`)

```json
{
  "news": [
    { "title": "...", "link": "...", "source": "...", "date": "2 hours ago", "snippet": "..." }
  ]
}
```

### Video Search (`/videos`)

```json
{
  "videos": [
    { "title": "...", "link": "...", "channel": "...", "duration": "...", "date": "..." }
  ]
}
```

## Error Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check key |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry later |

## Quota

- Free tier: 2,500 searches/month
- Paid: $0.30 per 1,000 searches
- Dashboard: https://serper.dev/dashboard

## cURL Examples

```bash
# Web search
curl -X POST https://google.serper.dev/search \
  -H 'X-API-KEY: YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"q": "query", "num": 10}'

# News with time filter (last week)
curl -X POST https://google.serper.dev/news \
  -H 'X-API-KEY: YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"q": "AI", "num": 5, "tbs": "qdr:w"}'

# Autocomplete
curl -X POST https://google.serper.dev/autocomplete \
  -H 'X-API-KEY: YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"q": "javascript"}'
```

## Node.js Inline Usage

```javascript
async function serperSearch(query, type = 'search', options = {}) {
  const endpoints = { search: '/search', images: '/images', news: '/news', videos: '/videos' };
  const res = await fetch(`https://google.serper.dev${endpoints[type]}`, {
    method: 'POST',
    headers: { 'X-API-KEY': process.env.SERPER_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ q: query, num: options.num || 10, ...options }),
  });
  return res.json();
}
```
