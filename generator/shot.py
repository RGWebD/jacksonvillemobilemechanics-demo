import sys, asyncio
from playwright.async_api import async_playwright
async def main(url,out,w,h,full):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':int(w),'height':int(h)})
        await pg.goto(url); await pg.wait_for_timeout(800)
        await pg.screenshot(path=out,full_page=full=='1'); await b.close()
asyncio.run(main(*sys.argv[1:6]))
