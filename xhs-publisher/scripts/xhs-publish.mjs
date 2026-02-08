#!/usr/bin/env node
/**
 * xhs-publish.mjs - Xiaohongshu (RedNote) post publisher via Playwright
 * Usage: node xhs-publish.mjs --image <path> [--title <title>] [--content <content>] [--tags <tag1,tag2>] [--dry-run]
 *
 * Prerequisites:
 *   npm install playwright (or npx playwright install chromium)
 *   First run requires QR code login; subsequent runs reuse saved session.
 */

import { chromium } from 'playwright';
import path from 'path';
import { existsSync } from 'fs';
import os from 'os';

// ── Config ──────────────────────────────────────────────────────────
const USER_DATA_DIR = process.env.XHS_USER_DATA_DIR || path.join(os.homedir(), '.xhs-playwright-data');
const PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish';
const LOGIN_URL_FRAGMENT = '/login';
const VIEWPORT = { width: 1400, height: 900 };

// ── Argument parsing ────────────────────────────────────────────────
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { images: [], tags: [], dryRun: false, title: '', content: '' };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if ((a === '--image' || a === '-i') && args[i + 1]) {
      opts.images.push(args[++i]);
    } else if ((a === '--title' || a === '-t') && args[i + 1]) {
      opts.title = args[++i];
    } else if ((a === '--content' || a === '-c') && args[i + 1]) {
      opts.content = args[++i];
    } else if ((a === '--tags') && args[i + 1]) {
      opts.tags = args[++i].split(',').map(t => t.trim()).filter(Boolean);
    } else if (a === '--dry-run') {
      opts.dryRun = true;
    } else if (a === '--help' || a === '-h') {
      showHelp();
      process.exit(0);
    }
  }
  return opts;
}

function showHelp() {
  console.log(`
xhs-publish.mjs - Publish image posts to Xiaohongshu (RedNote)

Usage:
  node xhs-publish.mjs --image <path> [options]

Options:
  -i, --image <path>    Image file path (required, repeatable for multiple images)
  -t, --title <text>    Post title (max 20 chars)
  -c, --content <text>  Post body text (max 1000 chars)
  --tags <t1,t2,...>    Comma-separated topic tags (e.g. "aigc,氛围感写真,光影写真")
  --dry-run             Fill content but do not click publish
  -h, --help            Show this help

Environment:
  XHS_USER_DATA_DIR     Browser data directory (default: ~/.xhs-playwright-data)

Examples:
  node xhs-publish.mjs -i photo.png -t "冬日氛围感" -c "温暖的光影" --tags "aigc,写真,光影"
  node xhs-publish.mjs -i img1.png -i img2.png -t "旅行日记" --dry-run
  `);
}

// ── Helpers ─────────────────────────────────────────────────────────
function log(msg) { console.log(`[xhs] ${msg}`); }

async function waitAndCheck(page, ms = 2000) {
  await page.waitForTimeout(ms);
}

// ── Main Flow ───────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs();

  if (opts.images.length === 0) {
    console.error('Error: at least one --image is required. Use --help for usage.');
    process.exit(1);
  }

  // Validate image files exist
  for (const img of opts.images) {
    if (!existsSync(img)) {
      console.error(`Error: image file not found: ${img}`);
      process.exit(1);
    }
  }

  // Launch persistent browser context (preserves login cookies)
  log('Launching browser...');
  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: false,
    viewport: VIEWPORT,
    locale: 'zh-CN',
  });
  const page = context.pages()[0] || await context.newPage();

  try {
    // Step 1: Navigate to publish page
    log('Navigating to publish page...');
    await page.goto(PUBLISH_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await waitAndCheck(page, 3000);

    // Step 2: Check login status
    if (page.url().includes(LOGIN_URL_FRAGMENT)) {
      log('Not logged in. Switching to QR code login...');
      // Click QR toggle
      await page.evaluate(() => {
        const imgs = document.querySelectorAll('img');
        for (const img of imgs) {
          if (getComputedStyle(img).cursor === 'pointer') { img.click(); break; }
        }
      });
      await waitAndCheck(page, 1000);

      log('Please scan the QR code with Xiaohongshu APP to login...');
      // Wait for navigation away from login page (max 120s)
      await page.waitForURL(url => !url.toString().includes(LOGIN_URL_FRAGMENT), { timeout: 120000 });
      log('Login successful!');

      // Re-navigate to publish page after login
      await page.goto(PUBLISH_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await waitAndCheck(page, 3000);
    }

    // Step 3: Switch to "上传图文" (Image/Text) tab
    log('Switching to image upload tab...');
    await page.evaluate(() => {
      const tabs = document.querySelectorAll('span, div');
      for (const tab of tabs) {
        if (tab.textContent.trim() === '上传图文') { tab.click(); return; }
      }
    });
    await waitAndCheck(page, 2000);

    // Step 4: Upload images
    log(`Uploading ${opts.images.length} image(s)...`);
    const absolutePaths = opts.images.map(p => path.resolve(p));

    // Trigger file chooser and upload
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser', { timeout: 10000 }),
      page.evaluate(() => {
        const btn = document.querySelector('button');
        if (btn) btn.click();
        // Also try clicking the upload area
        const uploadArea = document.querySelector('[class*="upload"]');
        if (uploadArea) uploadArea.click();
      }),
    ]);
    await fileChooser.setFiles(absolutePaths);
    log('Images uploaded.');
    await waitAndCheck(page, 3000);

    // Step 5: Close any popups/tooltips
    await page.evaluate(() => {
      const closeButtons = document.querySelectorAll('[class*="close"], [class*="dismiss"]');
      closeButtons.forEach(b => b.click());
      // Close popover arrows
      const arrows = document.querySelectorAll('[class*="popover"] svg, [class*="arrow"] svg');
      arrows.forEach(a => a.click());
    });
    await waitAndCheck(page, 500);

    // Step 6: Fill title
    if (opts.title) {
      log(`Setting title: ${opts.title}`);
      const titleInput = page.getByRole('textbox', { name: '填写标题会有更多赞哦' });
      await titleInput.click();
      await titleInput.fill(opts.title);
      await waitAndCheck(page, 500);
    }

    // Step 7: Fill content
    if (opts.content) {
      log('Setting content...');
      const contentBox = page.getByRole('textbox').nth(1);
      await contentBox.click();
      await contentBox.fill(opts.content);
      await waitAndCheck(page, 500);
    }

    // Step 8: Add topic tags via keyboard
    if (opts.tags.length > 0) {
      log(`Adding ${opts.tags.length} tags...`);
      for (const tag of opts.tags) {
        await page.keyboard.press('End');
        await page.waitForTimeout(200);
        await page.keyboard.type(`#${tag}`, { delay: 80 });
        await page.waitForTimeout(1500); // Wait for topic search dropdown
        await page.keyboard.press('Enter'); // Select first result
        await page.waitForTimeout(800);
      }
      log('Tags added.');
    }

    // Step 9: Publish or dry-run
    if (opts.dryRun) {
      log('Dry-run mode: content filled but not published.');
      log('Review the browser window and close it when done.');
      await page.waitForTimeout(60000); // Keep open for 60s for review
    } else {
      log('Publishing...');
      await page.getByRole('button', { name: '发布' }).click();
      await waitAndCheck(page, 3000);

      // Verify success
      if (page.url().includes('success') || page.url().includes('published=true')) {
        log('Post published successfully!');
      } else {
        log('Warning: could not confirm publish success. Check the browser.');
      }
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  } finally {
    await context.close();
  }
}

main();
