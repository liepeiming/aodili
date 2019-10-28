#!/usr/bin/env python3
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('http://quotes.toscrape.com/js/')
    doc = pq(await page.content())
    print('Quotes:', doc('.quote').length)
    await asyncio.sleep(100)
    await browser.close()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    pass
