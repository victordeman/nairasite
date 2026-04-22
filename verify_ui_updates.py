
import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. AI Agents Tour - Start Tour UI Visibility
        await page.goto("http://localhost:8000/ai-agents-tour")
        await page.click("#start-tour-btn")
        await asyncio.sleep(2)
        await page.screenshot(path="/home/jules/verification/v8_tour_started_ui_hidden.png")

        # 2. Check Pioneer Image
        # Click a pioneer node (Alan Turing is first in helix)
        # We'll use raycasting click indirectly by clicking the canvas center after fly-in
        await page.mouse.click(500, 400)
        await asyncio.sleep(1)
        await page.screenshot(path="/home/jules/verification/v9_pioneer_info_with_image.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
