import asyncio,sys
from playwright.async_api import async_playwright
PAGES=sys.argv[1:] or ['/']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        errs=[]
        for w,h,tag in [(1366,900,'d'),(390,844,'m')]:
            pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
            pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
            pg.on('pageerror',lambda e: errs.append(str(e)))
            for u in PAGES:
                await pg.goto('http://127.0.0.1:8766'+u,wait_until='networkidle')
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                n=u.strip('/').replace('/','_') or 'home'
                await pg.screenshot(path=f'/tmp/claude-0/t/s_{n}_{tag}.png',full_page=True)
                sw=await pg.evaluate('document.documentElement.scrollWidth')
                if sw>w: errs.append(f'{u} {tag} yatay taşma {sw}')
        print('ERR',errs)
        await b.close()
asyncio.run(main())
