import pytest

from pages.todo_page import TodoPage


@pytest.mark.asyncio
async def test_add_new_todo_en(todo: TodoPage) -> None:
    # Given I am on the TodoMVC app
    # (Handled by the 'todo' fixture which opens the page)

    # When I add a new todo item "My new todo item in English"
    item_name = "My new todo item in English"
    await todo.add_new_item(item_name)

    # Then I should see the new item in the list
    await todo.verify_item_exists(item_name)
    
    # Verify the item is active (not completed) by default
    await todo.verify_item_active(item_name)

    # Mark the item as completed
    await todo.complete_item(item_name)

    # Verify the item is now marked as completed
    await todo.verify_item_completed(item_name)

    # Cleanup: Delete the created item to keep the test idempotent
    await todo.delete_item(item_name)

    # Then I should not see the item in the list anymore
    await todo.verify_all_items_cleared()