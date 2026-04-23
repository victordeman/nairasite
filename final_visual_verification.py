import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()

        print("Step 1: Home Page Initial State")
        await page.goto('http://localhost:8000/')
        await page.wait_for_selector('#active-xr-experience')
        await page.screenshot(path='/home/jules/verification/1_home_initial.png')

        print("Step 2: Clicking Hero Card (Redirect to Vision)")
        await page.click('#active-xr-experience')
        await page.wait_for_url('**/vision')
        await page.screenshot(path='/home/jules/verification/2_vision_redirect.png')
        await page.go_back()

        print("Step 3: Testing Hero Try AI Button")
        await page.wait_for_selector('#hero-try-ai-btn')
        await page.click('#hero-try-ai-btn')
        await page.wait_for_selector('#ai-modal', state='visible')
        print("Hero Try AI button opened modal.")
        await page.screenshot(path='/home/jules/verification/3_hero_modal_open.png')
        await page.click('#close-ai-modal')

        print("Step 4: Checking Floating AI Chat Button")
        await page.wait_for_selector('#try-ai-btn', state='visible')
        await page.click('#try-ai-btn')
        await page.wait_for_selector('#ai-modal', state='visible')
        print("Floating AI chat button opened modal.")
        await page.screenshot(path='/home/jules/verification/4_floating_modal_open.png')
        await page.click('#close-ai-modal')

        print("Step 5: Verification complete")

        await browser.close()

if __name__ == "__main__":
    if not os.path.exists('/home/jules/verification'):
        os.makedirs('/home/jules/verification')
    asyncio.run(run())
