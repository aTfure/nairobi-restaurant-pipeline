#!/usr/bin/env node
const puppeteer = require('puppeteer');

async function main() {
  const targetUrl = process.argv[2];
  if (!targetUrl) {
    console.error('Usage: node scraper.js <url>');
    process.exit(1);
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();
    await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    await new Promise((resolve) => setTimeout(resolve, 2000));
    await page.screenshot({ path: '/tmp/test_scrape.png', fullPage: true });
    console.log('screenshot_saved:/tmp/test_scrape.png');
  } catch (error) {
    const message = error && error.message ? error.message : String(error);
    console.error(`scraper_error:${message}`);
    if (message.includes('timeout') || message.includes('Timed out')) {
      console.error('puppeteer_timeout_handled');
    }
  } finally {
    if (browser) {
      await browser.close().catch(() => undefined);
    }
  }
}

main();
