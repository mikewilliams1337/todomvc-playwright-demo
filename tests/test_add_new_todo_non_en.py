import pytest

from pages.todo_page import TodoPage


@pytest.mark.asyncio
async def test_add_new_todo_non_en(todo: TodoPage) -> None:
    item_name = "Learning more Nihongo: 日本語をもっと学ぶ"
    await todo.add_new_item(item_name)
    await todo.verify_item_exists(item_name)

    await todo.verify_item_active(item_name)
    await todo.complete_item(item_name)
    await todo.verify_item_completed(item_name)

    await todo.delete_item(item_name)
    await todo.verify_all_items_cleared()