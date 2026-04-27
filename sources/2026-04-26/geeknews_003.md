---
source: geeknews
date: 2026-04-26
points: 22
url: "https://github.com/h4ckf0r0day/obscura"
title: Obscura - 오픈소스 헤드리스 브라우저
---

# Obscura - 오픈소스 헤드리스 브라우저

The open-source headless browser for AI agents and web scraping.
Lightweight, stealthy, and built in Rust.
Obscura is a headless browser engine written in Rust, built for web scraping and AI agent automation. It runs real JavaScript via V8, supports the Chrome DevTools Protocol, and acts as a drop-in replacement for headless Chrome with Puppeteer and Playwright.
Designed for automation at scale, not desktop browsing.
Grab the latest binary from Releases:
# Linux x86_64
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux.tar.gz
tar xzf obscura-x86_64-linux.tar.gz
./obscura fetch https://example.com --eval "document.title"
# macOS Apple Silicon
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-aarch64-macos.tar.gz
tar xzf obscura-aarch64-macos.tar.gz
# macOS Intel
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-macos.tar.gz
tar xzf obscura-x86_64-macos.tar.gz
# Windows
Download the `.zip` from the releases page and extract it manually.
Single binary. No Chrome, no Node.js, no dependencies.
git clone https://github.com/h4ckf0r0day/obscura.git
cd obscura
cargo build --release
# With stealth mode (anti-detection + tracker blocking)
cargo build --release --features stealth
Requires Rust 1.75+ (rustup.rs). First build takes ~5 min (V8 compiles from source, cached after).
# Get the page title
obscura fetch https://example.com --eval "document.title"
# Extract all links
obscura fetch https://example.com --dump links
# Render JavaScript and dump HTML
obscura fetch https://news.ycombinator.com --dump html
# Wait for dynamic content
obscura fetch https://example.com --wait-until networkidle0
obscura serve --port 9222
# With stealth mode (anti-detection + tracker blocking)
obscura serve --port 9222 --stealth
obscura scrape url1 url2 url3 ... \
--concurrency 25 \
--eval "document.querySelector('h1').textContent" \
--format json
npm install puppeteer-core
import puppeteer from 'puppeteer-core';
const browser = await puppeteer.connect({
browserWSEndpoint: 'ws://127.0.0.1:9222/devtools/browser',
});
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com');
const stories = await page.evaluate(() =>
Array.from(document.querySelectorAll('.titleline > a'))
.map(a => ({ title: a.textContent, url: a.href }))
);
console.log(stories);
await browser.disconnect();
npm install playwright-core
import { chromium } from 'playwright-core';
const browser = await chromium.connectOverCDP({
endpointURL: 'ws://127.0.0.1:9222',
});
const page = await browser.newContext().then(ctx => ctx.newPage());
await page.goto('https://en.wikipedia.org/wiki/Web_scraping');
console.log(await page.title());
await browser.close();
await page.goto('https://quotes.toscrape.com/login');
await page.evaluate(() => {
document.querySelector('#username').value = 'admin';
document.querySelector('#password').value = 'admin';
document.querySelector('form').submit();
});
// Obscura handles the POST, follows the 302 redirect, maintains cookies
Page load:
Enable with --features stealth
.
- Per-session fingerprint randomization (GPU, screen, canvas, audio, battery)
- Realistic
navigator.userAgentData
(Chrome 145, high-entropy values) event.isTrusted = true
for dispatched events- Hidden internal properties (
Object.keys(window)
safe) - Native function masking (
Function.prototype.toString()
→[native code]
) navigator.webdriver = undefined
(matches real Chrome)
- 3,520 domains blocked
- Blocks analytics, ads, telemetry, and fingerprinting scripts
- Prevents trackers from loading entirely
- Enabled automatically with
--stealth
Obscura implements the Chrome DevTools Protocol for Puppeteer/Playwright compatibility.
Start a CDP WebSocket server.
Fetch and render a single page.
Scrape multiple URLs in parallel with worker processes.
Apache 2.0