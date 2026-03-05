from collections.abc import AsyncGenerator

import pytest
from playwright.async_api import Page, async_playwright

from pages.todo_page import TodoPage


def pytest_addoption(parser):
    parser.addoption(
        "--headed", action="store_true", default=False, help="Run browser in headed mode"
    )
    parser.addoption(
        "--slowmo", type=int, default=0, help="Slow down Playwright actions (ms)"
    )

# @pytest.fixture makes this function available as a parameter to all tests
# It will be called before each test and cleaned up after
@pytest.fixture
async def page(request) -> AsyncGenerator[Page, None]:
    async with async_playwright() as p:
        headless = not request.config.getoption("--headed")
        slow_mo = request.config.getoption("--slowmo")
        browser = await p.chromium.launch(headless=headless, slow_mo=slow_mo)
        context = await browser.new_context()
        page = await context.new_page()

        yield page
        
        await context.close()
        await browser.close()


@pytest.fixture
async def todo(page: Page) -> AsyncGenerator[TodoPage, None]:
    # Create an instance of the TodoPage page object, passing in the Playwright page
    todo = TodoPage(page)
    await todo.open()               # Uses the BasePage's open method to navigate to the base URL
    await todo.verify_todo_title()  # Verify the page loaded successfully (e.g., check for a key element) 
    yield todo                      # Provide the TodoPage object to the test; test runs here