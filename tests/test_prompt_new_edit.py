import pytest

from pages.todo_page import TodoPage


@pytest.mark.asyncio
async def test_prompt_new_edit(todo: TodoPage) -> None:

    # Prompt the user for a new todo item name, add it to the list, and verify it was added
    item_name = input("Enter the name of the new todo item: ")

    await todo.add_new_item(item_name)
    await todo.verify_item_exists(item_name)

    await todo.verify_item_active(item_name)

    # Prompt the user for a new name for the item, edit it, and verify the change
    new_name = input(f"Enter the new name for the item '{item_name}': ")

    await todo.edit_item(item_name, new_name)
    await todo.verify_item_edited(item_name, new_name)

    await todo.complete_item(new_name)
    await todo.verify_item_completed(new_name)

    await todo.delete_item(new_name)
    await todo.verify_all_items_cleared()