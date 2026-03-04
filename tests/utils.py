from collections.abc import Iterable, Sequence

from pages.todo_page import TodoPage


async def add_items(todo: TodoPage, items: Sequence[str], prefix: str | None = None) -> list[str]:
    created_items: list[str] = []
    for item, text in enumerate(items, start=1):
        final = f"{prefix}-{item}: {text}" if prefix else text
        await todo.add_new_item(final)
        await todo.verify_item_exists(final)    # validate it was added to the list
        created_items.append(final)
    return created_items

async def complete_items(todo: TodoPage, created_items: Sequence[str], indices: Iterable[str]) -> None:
    for index in indices:
        text = created_items[int(index) - 1]
        await todo.complete_item(text)
        await todo.verify_item_completed(text)  # validate it is now completed

async def delete_items(todo: TodoPage, created_items: Sequence[str], indices: Iterable[str]) -> None:
    for index in indices:
        text = created_items[int(index) - 1]
        await todo.delete_item(text)
        await todo.verify_item_deleted(text)    # validate it was removed
