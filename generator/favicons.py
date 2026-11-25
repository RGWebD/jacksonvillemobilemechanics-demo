import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
B=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','brand'))
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':512,'height':512})
        await pg.set_content(f'<body style="margin:0;background:transparent"><img src="file://{B}/favicon.svg" style="width:512px;height:512px;display:block"></body>')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{B}/favicon-512.png',omit_background=True)
        # OG image
        pg2=await b.new_page(viewport={'width':1200,'height':630})
        await pg2.set_content(f'''<body style="margin:0;width:1200px;height:630px;background:url(file://{R}/img/og-base.jpg) center/cover;font-family:sans-serif">
        <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,15,28,.94) 0%,rgba(10,15,28,.7) 48%,rgba(10,15,28,.05) 100%)"></div>
        <img src="file://{B}/logo-horizontal-dark.svg" style="position:absolute;left:60px;top:60px;height:80px">
        <div style="position:absolute;left:60px;top:250px;color:#F4F6EF;font:900 64px/1.02 sans-serif;letter-spacing:-1px">We come to you.<br><span style="color:#C8F031">Any hour.</span></div>
        <div style="position:absolute;left:60px;bottom:60px;color:#F4F6EF;font:600 26px sans-serif">Open 24 hours · ★ 4.6 (315 Google reviews) · (904) 800-8923</div></body>''')
        await pg2.wait_for_timeout(500)
        await pg2.screenshot(path=f'{R}/img/og.jpg',type='jpeg',quality=86)
        await b.close()
asyncio.run(main())
im=Image.open(f'{B}/favicon-512.png').convert('RGBA')
for s in (16,32,180):
    im.resize((s,s),Image.LANCZOS).save(f'{B}/favicon-{s}.png')
im.resize((180,180),Image.LANCZOS).save(f'{R}/apple-touch-icon.png')
im.save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
import shutil; shutil.copy(f'{B}/favicon.svg',f'{R}/favicon.svg')
print('ok')
