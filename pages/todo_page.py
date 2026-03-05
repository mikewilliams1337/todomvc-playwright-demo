from playwright.async_api import Locator, Page

from pages.base_page import BasePage


class TodoPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ---------- Page-specific locators ----------

    def todo_input(self) -> Locator:
        return self.by_placeholder("What needs to be done?")

    def list_item(self, item_name: str) -> Locator:
        return self.by_css("li").filter(has=self.by_text(item_name))

    def item_checkbox(self, item_name: str) -> Locator:
        return self.list_item(item_name).locator(".toggle")

    def item_edit(self, item_name: str) -> Locator:
        return self.list_item(item_name).locator(".edit")

    def delete_button(self, item_name: str) -> Locator:
        return self.list_item(item_name).locator('button[aria-label="Delete"]')

    def toggle_all(self) -> Locator:
        return self.by_id("toggle-all")

    def filter_all(self) -> Locator:
        return self.by_text("All")

    def filter_active(self) -> Locator:
        return self.by_text("Active")

    def filter_completed(self) -> Locator:
        return self.by_text("Completed")

    def clear_completed(self) -> Locator:
        return self.by_text("Clear completed")

    # ---------- Page-specific actions ----------

    async def add_new_item(self, item_name: str) -> None:
        await self.fill(self.todo_input(), item_name)
        await self.press(self.todo_input(), "Enter")

    async def complete_item(self, item_name: str) -> None:
        await self.click(self.item_checkbox(item_name))

    async def edit_item(self, item_name: str, new_name: str) -> None:
        await self.hover(self.list_item(item_name))
        await self.dblclick(self.list_item(item_name))
        await self.fill(self.item_edit(item_name), new_name)
        await self.press(self.item_edit(item_name), "Enter")

    async def delete_item(self, item_name: str) -> None:
        await self.hover(self.list_item(item_name))
        await self.click(self.delete_button(item_name))

    async def toggle_all_items(self) -> None:
        await self.click(self.toggle_all())

    async def filter_all_items(self) -> None:
        await self.click(self.filter_all())

    async def filter_active_items(self) -> None:
        await self.click(self.filter_active())

    async def filter_completed_items(self) -> None:
        await self.click(self.filter_completed())

    async def clear_completed_items(self) -> None:
        await self.click(self.clear_completed())

    # ---------- Page-specific List Compiler ----------

    async def compile_todo_list(self) -> list[tuple[str, bool]]:
        """
        Gather the text and completed state for each todo item using the
        generic ``compile_list`` helper from ``BasePage``.  The state accessor
        returns ``True`` when the ``li`` has the ``completed`` class.
        """
        ul = self.by_css("ul.todo-list")
        await self.filter_all_items()           # ensure we are looking at the full list

        async def state_accessor(item: Locator) -> bool:
            return await item.get_attribute("class") == "completed"

        return await self.compile_list(ul, "li", state_accessor=state_accessor)

    # ---------- Page-specific assertions ----------

    async def verify_todo_title(self) -> None:
        expected_title = "React • TodoMVC"
        await self.expect_title(expected_title)

    async def verify_item_exists(self, item_name: str) -> None:
        await self.filter_all_items()           # ensure item is not hidden by filter
        await self.expect_text(self.list_item(item_name), item_name)
        await self.expect_exists(self.list_item(item_name))

    async def verify_item_active(self, item_name: str) -> None:
        await self.filter_active_items()        # ensure item is not hidden by filter
        await self.expect_text(self.list_item(item_name), item_name)
        await self.expect_unchecked(self.item_checkbox(item_name))
        await self.filter_completed_items()     # ensure item is hidden by filter
        await self.expect_deleted(self.list_item(item_name))
        await self.filter_all_items()           # ensure item is not hidden by filter
        await self.expect_text(self.list_item(item_name), item_name)
        await self.expect_unchecked(self.item_checkbox(item_name))

    async def verify_item_completed(self, item_name: str) -> None:
        await self.filter_completed_items()     # ensure item is not hidden by filter
        await self.expect_text(self.list_item(item_name), item_name)
        await self.expect_checked(self.item_checkbox(item_name))
        await self.expect_attribute(self.list_item(item_name), "class", "completed")
        await self.filter_active_items()        # ensure item is hidden by filter
        await self.expect_deleted(self.list_item(item_name))
        await self.filter_all_items()           # ensure item is not hidden by filter
        await self.expect_text(self.list_item(item_name), item_name)

    async def verify_item_edited(self, item_name: str, new_name: str) -> None:
        await self.filter_all_items()           # ensure item is not hidden by filter
        await self.expect_text(self.list_item(new_name), new_name)
        await self.expect_deleted(self.list_item(item_name))

    async def verify_item_deleted(self, item_name: str) -> None:
        await self.filter_active_items()        # ensure item is not hidden by filter
        await self.expect_deleted(self.list_item(item_name))
        await self.filter_completed_items()     # ensure item is not hidden by filter
        await self.expect_deleted(self.list_item(item_name))
        await self.filter_all_items()           # ensure item is not hidden by filter
        await self.expect_deleted(self.list_item(item_name))

    async def verify_all_items_cleared(self) -> None:
        await self.expect_deleted(self.by_css("ul.todo-list li"))

    async def verify_item_filters(self) -> None:
        """
        Ensure filtering works correctly:
        * when 'Active' filter is selected, no completed items are visible
        * when 'Completed' filter is selected, no active items are visible
        * when 'All' filter is selected again, the full set reappears
        The comparison is performed using ``compile_todo_list`` so we don't
        duplicate locator logic.
        """
        # capture current state before applying filters (should be full list)
        full = await self.compile_todo_list()  # List of (text, completed)
        full_active = [text for text, completed in full if not completed]
        full_completed = [text for text, completed in full if completed]

        # active filter: only active items from full list should be visible
        await self.filter_active_items()
        active_items = [await item.inner_text() for item in await self.page.locator('ul.todo-list li').all()]
        assert set(active_items) == set(full_active), f"Active filter mismatch: expected {full_active}, got {active_items}"

        # completed filter: only completed items from full list should be visible
        await self.filter_completed_items()
        completed_items = [await item.inner_text() for item in await self.page.locator('ul.todo-list li').all()]
        assert set(completed_items) == set(full_completed), f"Completed filter mismatch: expected {full_completed}, got {completed_items}"  # noqa: E501

        # back to all
        await self.filter_all_items()
        all_again = await self.compile_todo_list()
        assert sorted(full) == sorted(all_again), "all filter did not restore full list"
