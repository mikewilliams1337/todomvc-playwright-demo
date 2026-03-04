from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

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
    
    async def dblclick(self, locator: Locator) -> None:
        await locator.dblclick()

    async def fill(self, locator: Locator, text: str) -> None:
        await locator.fill(text)

    async def press(self, locator: Locator, key: str) -> None:
        await locator.press(key)

    async def hover(self, locator: Locator) -> None:
        await locator.hover()


    # ---------- Common assertions ----------

    async def expect_title(self, expected_title: str) -> None:
        actual_title = await self.page.title()
        await expect(self.page).to_have_title(expected_title)
        print(
            f'Actual page title "{actual_title}" matches the expected "{expected_title}"'
        )

    async def expect_text(self, locator: Locator, expected_text: str) -> None:
        actual_text = await locator.text_content()
        await expect(locator).to_have_text(expected_text)
        print(
            f'Actual text "{actual_text}" matches the expected "{expected_text}"'
        )

    async def expect_visible(self, locator: Locator) -> None:
        await expect(locator).to_be_visible()
        print(f"Locator {locator} is visible on the page.")
    
    async def expect_checked(self, locator: Locator) -> None:
        await expect(locator).to_be_checked()
        print(f"Locator {locator} is checked.")

    async def expect_unchecked(self, locator: Locator) -> None:
        await expect(locator).not_to_be_checked()
        print(f"Locator {locator} is unchecked.")

    async def expect_attribute(self, locator: Locator, name: str, value: str) -> None:
        await expect(locator).to_have_attribute(name, value)
        print(
            f'Locator {locator} has attribute "{name}" with value "{value}".'
        )

    async def expect_css_property(self, locator: Locator, property_name: str, expected_value: str) -> None:
        await expect(locator).to_have_css(property_name, expected_value)
        print(
            f"Locator {locator} has CSS {property_name} == '{expected_value}'"
        )

    async def expect_exists(self, locator: Locator) -> None:
        await expect(locator).to_have_count(1)
        print(f"Locator {locator} exists in the DOM.")

    async def expect_deleted(self, locator: Locator) -> None:
        """
        Assert that *no* elements match this locator – i.e. it has been removed
        from the DOM.  This is what you want after deleting a list item.
        """
        # the to_have_count assertion waits for the count to settle, so it will
        # retry until either the element disappears or a timeout occurs.
        await expect(locator).to_have_count(0)
        print(f"Locator {locator} is not present in the DOM.")

    # ---------- State helpers ----------

    async def compile_list(
        self,
        container: Locator,
        item_selector: str,
        *,
        state_accessor: Callable[[Locator], Any] | None = None,
    ) -> list[tuple[str, Any]]:
        """
        Build a list of (text, state) for elements found under `container`.

        - `container` is a Locator pointing at the parent element that holds
          all items (e.g. the <ul> in a todo list).
        - `item_selector` is a selector scoped to `container` that matches each
          item. It can be a CSS selector, text locator, etc.
        - `state_accessor`, when provided, is a coroutine/function that receives
          the Locator for a single item and returns any additional state you
          care about (a bool, string, dict, etc.). If omitted the state field
          will be ``None``.

        The base implementation does not assume anything about the markup used
        for state; the subclass (e.g. ``TodoPage``) can supply an accessor or
        post-process the returned tuples.
        """
        items = container.locator(item_selector)
        count = await items.count()
        out: list[tuple[str, Any]] = []
        for i in range(count):
            item = items.nth(i)
            text = await item.text_content()
            state = await state_accessor(item) if state_accessor else None
            out.append((text or "", state))
        return out


    