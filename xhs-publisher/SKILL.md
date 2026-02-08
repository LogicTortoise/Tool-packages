---
name: xhs-publisher
description: "Publish image posts to Xiaohongshu (小红书/RedNote) via browser automation. Use when the user wants to publish a note/post on Xiaohongshu, upload images to XHS, create social media content for RedNote, or automate XHS publishing. Triggers on keywords: '小红书', 'xiaohongshu', 'XHS', 'RedNote', '发布笔记', 'publish post', '发小红书'."
---

# XHS Publisher

Automate publishing image posts to Xiaohongshu (小红书) creator platform using Playwright browser automation.

## Prerequisites

- Node.js 18+
- Playwright: `npm install playwright`
- First run requires QR code login via XHS APP; session persists in `~/.xhs-playwright-data`

## Two Usage Modes

### Mode 1: Standalone Script

Run `scripts/xhs-publish.mjs` directly:

```bash
node scripts/xhs-publish.mjs \
  -i /path/to/image.png \
  -t "标题文字" \
  -c "正文内容描述" \
  --tags "aigc,氛围感写真,光影写真"
```

Options: `-i` image (repeatable), `-t` title (max 20 chars), `-c` content (max 1000 chars), `--tags` comma-separated topics, `--dry-run` to preview without publishing.

### Mode 2: Playwright MCP Interactive

Use the Playwright MCP tools step by step. Follow the workflow below.

## Publishing Workflow (Playwright MCP)

### Step 1 — Navigate

```
browser_navigate → https://creator.xiaohongshu.com/publish/publish
```

If redirected to login page, click QR toggle image → user scans → wait for redirect.

### Step 2 — Switch to Image Tab

```js
// Use JS click (viewport issues with normal click)
page.evaluate(() => {
  document.querySelectorAll('span, div').forEach(el => {
    if (el.textContent.trim() === '上传图文') el.click();
  });
});
```

### Step 3 — Upload Images

Click upload area → `browser_file_upload` with image paths. Supports 1-18 images, png/jpg/jpeg/webp, max 32MB each.

### Step 4 — Fill Title & Content

- Title: `getByRole('textbox', { name: '填写标题会有更多赞哦' })` → `fill(title)`
- Content: `getByRole('textbox').nth(1)` → `fill(content)`

### Step 5 — Add Tags

Type `#keyword` in content area → topic dropdown appears → press Enter to select first result. Repeat for each tag. Always `press('End')` first to position cursor.

**Important**: Add tags AFTER `fill()` — `fill()` clears all existing content including tag markers.

### Step 6 — Publish

```
browser_click → button name="发布"
```

Success: URL contains `/publish/success` or `published=true`.

## Content Generation Tips

When user provides an image and topic, generate appropriate content:
- Title: catchy, under 20 chars, relevant to image mood/theme
- Content: 2-3 short paragraphs describing the mood/scene, ending with engagement question
- Tags: 6-8 tags across dimensions — style (#氛围感写真), technique (#光影写真), scene (#室内氛围感), genre (#aigc, #ai绘画), mood (#情绪人像)

## Detailed Reference

For DOM selectors, common issues, and troubleshooting, see [references/publishing-workflow.md](references/publishing-workflow.md).
