import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_smoke_example_title():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://demo.playwright.dev/todomvc/#/")

        expected_title = "React • TodoMVC"
        actual_title = await page.title()

        await expect(page).to_have_title(expected_title)
        print(
            f'Actual page title "{actual_title}" matches the expected "{expected_title}"'
        )
        await browser.close()
