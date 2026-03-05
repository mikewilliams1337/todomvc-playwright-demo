import pytest

from pages.todo_page import TodoPage
from tests.utils import add_items, complete_items, delete_items


@pytest.mark.asyncio
async def test_todo_filters_work(todo: TodoPage) -> None:
    # Add several items to the todo list
    items = ["Learn Python", "Learn Playwright", "Write tests", "Build portfolio", "Have fun"]
    await add_items(todo, items)

    # Mark some of them as completed
    await complete_items(todo, items, indices=["2", "4"])

    # Validate the filters show the todo items correctly
    await todo.verify_item_filters()

    await delete_items(todo, items, indices=["2", "3"])

    # Validate the filters still work after deletions
    await todo.verify_item_filters()

    # Toggle all remaining items to completed
    await todo.toggle_all_items()

    # Validate all items are now completed
    await todo.verify_item_filters() # active should be empty, completed should have all remaining items

    # Cleanup: clear completed items
    await todo.clear_completed_items()

    # Validate all items are cleared
    await todo.verify_all_items_cleared()