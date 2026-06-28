#!/usr/bin/env node
const puppeteer = require('puppeteer');

async function main() {
  const targetUrl = process.argv[2];
  if (!targetUrl) {
    console.error('Usage: node scraper.js <url>');
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });

  try {
    const page = await browser.newPage();
    await page.goto(targetUrl, { waitUntil: 'networkidle2' });
    await new Promise((resolve) => setTimeout(resolve, 2000));
    await page.screenshot({ path: '/tmp/test_scrape.png', fullPage: true });
    console.log(`screenshot_saved:/tmp/test_scrape.png`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
