import pytest
from playwright.sync_api import sync_playwright

#  A new todo item can be added that includes numbers.
@pytest.mark.parametrize("todo_number", [
    "1",       # number
    "11",   # 2 length numbers
    "1234567890",  # 10 length numbers
    "12345678901234567890",  # 20 length numbers
    "1 1",  # 2 numbers with space between
    "1 1 1",  # 3 numbers with space between
    "12345 67890 1234567890",  # 20 length numbers with space between
])
def test_add_todo_item_includes_numbers(todo_number):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        # Wait for the app to load
        page.wait_for_selector("input.new-todo")

        # Add a new todo item
        # todo_number = "1234567890"
        page.fill("input.new-todo", todo_number)
        page.press("input.new-todo", "Enter")

        # Verify the new todo item appears in the list
        todo_items = page.locator("ul.todo-list li")
        assert todo_items.count() == 1
        assert todo_items.nth(0).locator("label").inner_text() == todo_number

        page.screenshot(path="running.png")

        browser.close()
