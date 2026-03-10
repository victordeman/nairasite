import asyncio
from playwright.async_api import async_playwright
import os

async def capture_vision():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to Vision listing
        print("Capturing Vision listing...")
        await page.goto("http://localhost:8000/vision")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification/vision_listing.png", full_page=True)

        # Navigate to AI Excellence Hub
        print("Capturing AI Excellence Hub detail...")
        await page.goto("http://localhost:8000/vision/ai-excellence-hub")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification/vision_detail_hub.png", full_page=True)

        # Navigate to Regional Leadership
        print("Capturing Regional Leadership detail...")
        await page.goto("http://localhost:8000/vision/regional-leadership")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification/vision_detail_leadership.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_vision())
