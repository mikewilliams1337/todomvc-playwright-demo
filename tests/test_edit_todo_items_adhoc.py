import pytest
from utils import add_items, complete_items

from pages.todo_page import TodoPage


@pytest.mark.asyncio
async def test_edit_todo_items(todo: TodoPage) -> None:

    # Add multiple items to be edited in active and completed states
    items = ["Item to be edited in active", "Item 2 be edited in completed", "Item to remain unchanged"]
    await add_items(todo, items)

    # Mark the second item as completed
    await complete_items(todo, items, indices=["2"])

    # Edit the first item
    new_name_1 = "Item edited while active"
    new_name_2 = "Item edited while completed"

    await todo.edit_item(items[0], new_name_1)
    await todo.verify_item_edited(items[0], new_name_1)

    await todo.edit_item(items[1], new_name_2)
    await todo.verify_item_edited(items[1], new_name_2)

    # Validate the edited items appear in the correct filters
    await todo.verify_item_filters()

    # Cleanup: delete all items
    await todo.toggle_all_items()
    await todo.clear_completed_items()
    await todo.verify_all_items_cleared()