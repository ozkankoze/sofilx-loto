import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1366,'height':900})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8766/bd-g01/red'); await pg.fill('#qty','5'); await pg.click('.pi [data-add]')
        await pg.goto('http://127.0.0.1:8766/urunler?k=vana'); n=await pg.locator('.pc:not([hidden])').count(); print('vana filtre:',n)
        await pg.fill('#q','f01'); print('f01 arama:',await pg.locator('.pc:not([hidden])').count())
        await pg.locator('.pc:not([hidden]) [data-add]').first.click()
        await pg.goto('http://127.0.0.1:8766/teklif'); print('sepet:',await pg.locator('.ci').count(), await pg.inner_text('.cart-n'))
        await pg.screenshot(path='/tmp/claude-0/t/cart.png')
        await pg.goto('http://127.0.0.1:8766/bu-sayfa-yok'); print('404 başlık:',await pg.title())
        print('ERR',errs); await b.close()
asyncio.run(main())
