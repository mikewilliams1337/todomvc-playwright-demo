# todomvc-playwright-demo
Playwright + Python E2E testing demo (TodoMVC) with pytest, POM structure.

Automated tests for the following website: https://demo.playwright.dev/todomvc/#/

Tests cover the following requirements:
• A new todo item can be added using English text.
• A new todo item can be added using non-English characters.
• A new todo item can be added that includes numbers.
• A todo item can be marked as completed and appears correctly in the "Completed" view.
• A todo item can be deleted and no longer appears in any view.
• The "Active" filter correctly shows only items that are not completed.
• The "Completed" filter correctly shows only items that have been marked as completed.
