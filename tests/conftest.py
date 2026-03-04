from collections.abc import AsyncGenerator

import pytest
from playwright.async_api import Page, async_playwright

from pages.todo_page import TodoPage


# @pytest.fixture makes this function available as a parameter to all tests
# It will be called before each test and cleaned up after
@pytest.fixture
async def page() -> AsyncGenerator[Page, None]:
    # Start Playwright context manager (handles cleanup automatically)
    async with async_playwright() as p:
        # Launch the Chromium browser; headless=False opens the browser UI, slow_mo=500 slows down actions for visibility
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        # Create a new browser context (isolated session with own cookies/storage)
        context = await browser.new_context()
        # Create a new page/tab within the context
        page = await context.new_page()

        # Provide the page object to the test; test runs here
        yield page

        # Cleanup: Close the context (all pages within it)
        await context.close()
        # Cleanup: Close the browser instance
        await browser.close()

@pytest.fixture
async def todo(page: Page) -> AsyncGenerator[TodoPage, None]:
    # Create an instance of the TodoPage page object, passing in the Playwright page
    todo = TodoPage(page)
    await todo.open()   # Uses the BasePage's open method to navigate to the base URL
    yield todo          # Provide the TodoPage object to the test; test runs here