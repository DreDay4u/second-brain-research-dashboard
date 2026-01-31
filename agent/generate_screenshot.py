"""
Generate screenshot from HTML file using playwright.
"""

import asyncio
from playwright.async_api import async_playwright


async def create_screenshot():
    """Create screenshot from HTML file."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1400, 'height': 3000})

        # Load HTML file
        html_path = '/mnt/c/Users/colem/OpenSource/your-claude-engineer/generations/second-brain-research-dashboard/screenshots/layout-selector-results.html'
        with open(html_path, 'r') as f:
            html_content = f.read()

        await page.set_content(html_content)
        await page.wait_for_timeout(1000)  # Wait for render

        # Take full page screenshot
        screenshot_path = '/mnt/c/Users/colem/OpenSource/your-claude-engineer/generations/second-brain-research-dashboard/screenshots/DYN-190-layout-selector-results.png'
        await page.screenshot(path=screenshot_path, full_page=True)

        print(f"Screenshot saved to: {screenshot_path}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(create_screenshot())
