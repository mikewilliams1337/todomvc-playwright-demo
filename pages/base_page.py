from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.async_api import Locator, Page, expect

if TYPE_CHECKING:
    from playwright._impl._api_structures import AriaRole
else:
    AriaRole = str # Type alias for AriaRole to avoid circular imports in type checking

class BasePage:
    """
    Base class for all page objects.

    Design goals:
    - Keep shared behavior here (navigation, common actions, common assertions).
    - Keep page-specific locators in the concrete page classes.
    - Keep tests focused on test logic, not implementation details of how to interact with the page.
    - Keep reduncant code out of tests and page objects. (Don't write the same code twice. No copy-paste.)
    - Prefer Playwright's auto-waiting via Locator + expect (avoid sleeps).
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = "https://demo.playwright.dev/todomvc/#/"

    async def open(self, path: str = "") -> None:   # Navigate to base_url + path (or base_url alone if path is empty).
        path = path.lstrip("/")                     # Ensure no leading slash to avoid double slashes in URL
        url = f"{self.base_url}{path}" if path else self.base_url
        await self.page.goto(url)

    # ---------- Locator helpers ----------

    def by_css(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def by_id(self, element_id: str) -> Locator:
        return self.page.locator(f"#{element_id}")

    def by_name(self, name: str) -> Locator:
        return self.page.locator(f'[name="{name}"]')
    
    def by_text(self, text: str, exact: bool = True) -> Locator:
        return self.page.get_by_text(text, exact=exact)
    
    def by_placeholder(self, placeholder: str, exact: bool = True) -> Locator:
        return self.page.get_by_placeholder(placeholder, exact=exact)
    
    def by_role(self, role: "AriaRole", name: str | None = None, exact: bool = True) -> Locator:
        if name is None:
            return self.page.get_by_role(role)
        return self.page.get_by_role(role, name=name, exact=exact)
    
    # ---------- Common actions ----------

    async def click(self, locator: Locator) -> None:
        await locator.click()

    async def fill(self, locator: Locator, text: str) -> None:
        await locator.fill(text)

    async def press(self, locator: Locator, key: str) -> None:
        await locator.press(key)

    async def hover(self, locator: Locator) -> None:
        await locator.hover()

    # ---------- Common assertions ----------

    async def expect_title(self, title: str) -> None:
        await expect(self.page).to_have_title(title)

    async def expect_visible(self, locator: Locator) -> None:
        await expect(locator).to_be_visible()

    async def expect_hidden(self, locator: Locator) -> None:
        await expect(locator).to_be_hidden()

    async def expect_count(self, locator: Locator, count: int) -> None:
        await expect(locator).to_have_count(count)

    async def expect_text(self, locator: Locator, text: str) -> None:
        await expect(locator).to_have_text(text)

    # ---------- State helpers ----------

    async def clear_storage(self) -> None:
        """
        Useful for resetting app state between tests when the app uses localStorage.
        Call BEFORE navigating, or after with a reload.
        """
        await self.page.add_init_script("localStorage.clear(); sessionStorage.clear();")
