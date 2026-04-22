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

        print("Step 2: Launching Embedded Tour")
        await page.click('#active-xr-experience')
        await page.wait_for_selector('#embedded-tour-container')
        # Wait for Three.js to render something
        await page.wait_for_timeout(2000)
        await page.screenshot(path='/home/jules/verification/2_embedded_tour_launched.png')

        print("Step 3: Starting Guided Tour")
        await page.click('#embedded-start-btn')
        await page.wait_for_timeout(1000)
        # Verify title and start button are hidden
        intro_ui = await page.query_selector('#embedded-intro-ui')
        is_hidden = not await intro_ui.is_visible()
        print(f"Intro UI hidden: {is_hidden}")
        await page.screenshot(path='/home/jules/verification/3_guided_tour_active.png')

        print("Step 4: Checking Persistent AI Chat Button")
        chat_btn = await page.query_selector('#try-ai-btn')
        if chat_btn and await chat_btn.is_visible():
            print("Persistent AI chat button is visible.")
            await chat_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path='/home/jules/verification/4_ai_chat_modal_open.png')
            await page.click('#close-ai-modal')
        else:
            print("Persistent AI chat button NOT visible.")

        print("Step 5: Testing Exit Tour")
        await page.click('text=Exit Tour')
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/jules/verification/5_back_to_square.png')

        print("Step 6: Verifying Standalone Tour UI Hiding")
        await page.goto('http://localhost:8000/ai-agents-tour')
        await page.wait_for_selector('#start-tour-btn')
        await page.screenshot(path='/home/jules/verification/6_standalone_tour_init.png')
        await page.click('#start-tour-btn')
        await page.wait_for_timeout(1000)

        # Check intro UI and sidebar
        intro_ui_standalone = await page.query_selector('#intro-ui')
        sidebar = await page.query_selector('#ai-sidebar')
        print(f"Standalone Intro UI hidden: {not await intro_ui_standalone.is_visible()}")
        print(f"Standalone Sidebar hidden: {not await sidebar.is_visible()}")
        await page.screenshot(path='/home/jules/verification/7_standalone_tour_active.png')

        await browser.close()

if __name__ == "__main__":
    if not os.path.exists('/home/jules/verification'):
        os.makedirs('/home/jules/verification')
    asyncio.run(run())
