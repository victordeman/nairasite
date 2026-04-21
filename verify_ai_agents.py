import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def verify():
    # Start the server
    server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for server to start

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1280, 'height': 720})

            # Verify Homepage Launch Button
            await page.goto("http://localhost:8001/")
            await page.screenshot(path="homepage_launch.png")
            print("Captured homepage_launch.png")

            # Click Launch
            await page.click("#launch-ai-tour")
            await asyncio.sleep(2) # Wait for transition

            # Verify Tour Page
            await page.goto("http://localhost:8001/ai-agents-tour")
            await asyncio.sleep(5) # Wait for 3D to load and fly-in
            await page.screenshot(path="ai_agents_tour_main.png")
            print("Captured ai_agents_tour_main.png")

            # Click a Pioneer
            # We use evaluate to click since it's a 3D canvas, but the instruction panel might be easier to trigger via tour button
            await page.click("#start-tour-btn")
            await asyncio.sleep(2)
            await page.screenshot(path="ai_agents_tour_step.png")
            print("Captured ai_agents_tour_step.png")

            await browser.close()
    finally:
        server_process.terminate()

if __name__ == "__main__":
    asyncio.run(verify())
