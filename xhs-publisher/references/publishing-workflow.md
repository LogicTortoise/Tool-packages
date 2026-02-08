# Xiaohongshu Publishing Workflow Reference

## Page Structure

- Creator Platform URL: `https://creator.xiaohongshu.com/publish/publish`
- Login URL pattern: `/login` (redirect when not authenticated)
- Success URL pattern: `/publish/success` or `published=true`

## Step-by-Step Browser Automation

### 1. Navigate & Auth Check

```
goto https://creator.xiaohongshu.com/publish/publish
if URL contains '/login' → need login
```

Login: click QR toggle image → user scans with XHS APP → wait for redirect away from login page.

Session persistence: use `launchPersistentContext` with a `userDataDir` to keep cookies across runs.

### 2. Switch to Image Upload Tab

The page defaults to "上传视频" (video). Must switch to "上传图文" (image+text):

```js
// JS click needed (Playwright's click may fail due to viewport)
page.evaluate(() => {
  document.querySelectorAll('span, div').forEach(el => {
    if (el.textContent.trim() === '上传图文') el.click();
  });
});
```

URL changes to `?from=tab_switch` on success.

### 3. Upload Images

Trigger file chooser → `fileChooser.setFiles(paths)`. Supports 1-18 images (png, jpg, jpeg, webp). Max 32MB per image. Recommended aspect ratio 3:4 to 2:1, min 720x960.

### 4. Fill Title

Selector: `textbox[name="填写标题会有更多赞哦"]`
Max 20 characters.

### 5. Fill Content

Selector: second `textbox` in the form (`.getByRole('textbox').nth(1)`)
Max 1000 characters. Supports line breaks (`\n`).

### 6. Add Topic Tags

Two methods:

**Method A - Click recommended tags**: The page shows recommended tags like `#氛围感写真`, `#光影写真` below the content box. Click to insert as proper topic markers.

**Method B - Keyboard search**: Type `#keyword` in the content area → dropdown appears with matching topics and browse counts → press Enter to select the first result. This inserts a proper `[话题]` marker.

### 7. Publish

Click button with role `button` name `发布`. Success redirects to `/publish/success`.

## DOM Selectors Summary

| Element | Selector |
|---------|----------|
| Title input | `getByRole('textbox', { name: '填写标题会有更多赞哦' })` |
| Content input | `getByRole('textbox').nth(1)` |
| Publish button | `getByRole('button', { name: '发布' })` |
| Save draft | `getByRole('button', { name: '暂存离开' })` |
| Upload tab | JS: `textContent === '上传图文'` |
| Recommended tags | `getByText('#tagName').first()` |

## Common Issues

- **Viewport**: "上传图文" tab click may fail with "element is outside viewport". Use `page.evaluate` JS click or set viewport to 1400x900+.
- **File path**: Playwright MCP restricts file paths to allowed roots. Copy files to accessible paths if needed.
- **Tag insertion position**: Tags are inserted at current cursor position. Press `End` before typing `#tag` to append at line end.
- **`fill()` clears tags**: `textbox.fill()` replaces all content including previously inserted topic markers. Add tags AFTER filling content.
