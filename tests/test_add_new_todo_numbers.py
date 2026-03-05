import pytest

from pages.todo_page import TodoPage


@pytest.mark.asyncio
async def test_add_new_todo_numbers(todo: TodoPage) -> None:
    item_name = "My new todo item with numbers: 12345"
    await todo.add_new_item(item_name)
    await todo.verify_item_exists(item_name)

    await todo.verify_item_active(item_name)
    await todo.complete_item(item_name)
    await todo.verify_item_completed(item_name)

    await todo.delete_item(item_name)
    await todo.verify_all_items_cleared()