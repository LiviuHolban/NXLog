import pytest
from playwright.sync_api import sync_playwright

# A todo item can be deleted and no longer appears in any view.
def test_delete_todo_item_and_verify_absence():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        # Add a new todo item
        todo_text = "to delete this item"
        page.fill("input.new-todo", todo_text)
        page.press("input.new-todo", "Enter")

        # Hover to reveal the delete button and click it
        todo_item = page.locator("ul.todo-list li").nth(0)
        todo_item.hover()
        todo_item.locator("button.destroy").click()

        # Verify the item is removed from All view
        assert page.locator("ul.todo-list li").count() == 0

        # Verify the All view (curent page)
        assert page.locator("ul.todo-list li").count() == 0

        # Verify the Active view (active href)
        page.goto("https://demo.playwright.dev/todomvc/#/active")
        assert page.locator("ul.todo-list li").count() == 0

        # Verify the Completed view (completed href)
        page.goto("https://demo.playwright.dev/todomvc/#/completed")
        assert page.locator("ul.todo-list li").count() == 0
        
        page.screenshot(path="running.png")
        browser.close()
