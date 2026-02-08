#!/usr/bin/env node
/**
 * Serper.dev Google Search CLI
 *
 * Usage:
 *   node serper-search.mjs <query> [options]
 *
 * Options:
 *   -t, --type <type>    search|images|news|videos (default: search)
 *   -n, --num <number>   Number of results (default: 10)
 *   -g, --gl <country>   Country code (e.g. us, cn)
 *   -l, --hl <lang>      Language code (e.g. en, zh-cn)
 *   --tbs <timerange>    Time range: qdr:d(day) qdr:w(week) qdr:m(month) qdr:y(year)
 *   -j, --json           Output raw JSON
 *   -h, --help           Show help
 *
 * Environment:
 *   SERPER_API_KEY       Required. Your serper.dev API key.
 */

const BASE_URL = 'https://google.serper.dev';

const ENDPOINTS = {
  search: '/search',
  images: '/images',
  news: '/news',
  videos: '/videos',
};

function parseArgs(args) {
  const opts = { query: '', type: 'search', num: 10, json: false, help: false, extra: {} };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '-h' || a === '--help') opts.help = true;
    else if (a === '-j' || a === '--json') opts.json = true;
    else if (a === '-t' || a === '--type') opts.type = args[++i];
    else if (a === '-n' || a === '--num') opts.num = parseInt(args[++i]);
    else if (a === '-g' || a === '--gl') opts.extra.gl = args[++i];
    else if (a === '-l' || a === '--hl') opts.extra.hl = args[++i];
    else if (a === '--tbs') opts.extra.tbs = args[++i];
    else if (!opts.query) opts.query = a;
  }
  return opts;
}

function showHelp() {
  console.log(`
Serper Search CLI - Google Search via serper.dev API

Usage:
  node serper-search.mjs <query> [options]

Options:
  -t, --type <type>    search | images | news | videos (default: search)
  -n, --num <number>   Result count (default: 10, max: 100)
  -g, --gl <country>   Country code (us, cn, jp, etc.)
  -l, --hl <lang>      Language (en, zh-cn, ja, etc.)
  --tbs <range>        Time filter: qdr:d | qdr:w | qdr:m | qdr:y
  -j, --json           Output raw JSON
  -h, --help           Show this help

Examples:
  node serper-search.mjs "Node.js best practices"
  node serper-search.mjs "AI news" -t news -n 5
  node serper-search.mjs "sunset" -t images -n 3
  node serper-search.mjs "tech" -t news --tbs qdr:w
  node serper-search.mjs "python" -j
`);
}

async function serperFetch(type, query, num, extra) {
  const endpoint = ENDPOINTS[type] || ENDPOINTS.search;
  const apiKey = process.env.SERPER_API_KEY;
  if (!apiKey) {
    console.error('Error: SERPER_API_KEY environment variable is not set.');
    process.exit(1);
  }
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: { 'X-API-KEY': apiKey, 'Content-Type': 'application/json' },
    body: JSON.stringify({ q: query, num, ...extra }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

function display(data, type) {
  if (type === 'search') {
    if (!data.organic?.length) { console.log('No results found.'); return; }
    console.log(`\n${data.organic.length} results:\n`);
    data.organic.forEach((r, i) => {
      console.log(`${i + 1}. ${r.title}`);
      console.log(`   ${r.link}`);
      if (r.snippet) console.log(`   ${r.snippet}`);
      console.log();
    });
  } else if (type === 'images') {
    if (!data.images?.length) { console.log('No images found.'); return; }
    console.log(`\n${data.images.length} images:\n`);
    data.images.forEach((r, i) => {
      console.log(`${i + 1}. ${r.title || 'Untitled'}`);
      console.log(`   Image: ${r.imageUrl}`);
      console.log(`   Source: ${r.link}`);
      console.log();
    });
  } else if (type === 'news') {
    if (!data.news?.length) { console.log('No news found.'); return; }
    console.log(`\n${data.news.length} news:\n`);
    data.news.forEach((r, i) => {
      console.log(`${i + 1}. ${r.title}`);
      console.log(`   ${r.source || 'Unknown'} | ${r.date || ''}`);
      console.log(`   ${r.link}`);
      console.log();
    });
  } else if (type === 'videos') {
    if (!data.videos?.length) { console.log('No videos found.'); return; }
    console.log(`\n${data.videos.length} videos:\n`);
    data.videos.forEach((r, i) => {
      console.log(`${i + 1}. ${r.title}`);
      console.log(`   ${r.link}`);
      if (r.channel) console.log(`   Channel: ${r.channel}`);
      console.log();
    });
  }
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) { showHelp(); return; }
  if (!opts.query) { console.error('Error: No query provided. Use --help for usage.'); process.exit(1); }

  try {
    const data = await serperFetch(opts.type, opts.query, opts.num, opts.extra);
    if (opts.json) {
      console.log(JSON.stringify(data, null, 2));
    } else {
      display(data, opts.type);
    }
  } catch (e) {
    console.error(`Search failed: ${e.message}`);
    process.exit(1);
  }
}

main();
