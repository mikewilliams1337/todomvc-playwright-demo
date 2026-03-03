from playwright.async_api import Page

from pages.base_page import BasePage


class TodoPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ---------- Page-specific locators ----------
    