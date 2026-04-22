import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()

        print("Navigating to Home...")
        await page.goto('http://localhost:8000/')
        await page.wait_for_selector('#active-xr-experience')
        await page.screenshot(path='/home/jules/verification/v12_home_xr_square.png')

        print("Clicking XR Square...")
        await page.click('#active-xr-experience')
        await page.wait_for_timeout(2000)

        print("Verifying Tour Page...")
        if '/ai-agents-tour' in page.url:
            print("Successfully transitioned to tour.")

        await page.wait_for_selector('#ai-canvas-container')
        await page.screenshot(path='/home/jules/verification/v13_tour_page_init.png')

        print("Verifying Back to Home link...")
        back_link = await page.wait_for_selector('text=Back to NAIRA Home')
        if back_link:
            print("Back link found.")

        print("Starting Tour to verify UI vanish...")
        await page.click('#start-tour-btn')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='/home/jules/verification/v14_tour_started_immersive.png')

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
