import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_smoke_example_title():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://demo.playwright.dev/todomvc/#/")
        await expect(page).to_have_title("React • TodoMVC")
        await browser.close()