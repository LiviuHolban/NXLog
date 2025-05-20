import pytest
from playwright.sync_api import sync_playwright

#  A new todo item can be added using English text.
@pytest.mark.parametrize("todo_text", [
    "test",       # English text
    "English text",   # 2 words
    "English text with spaces",  # 4 words
    "E n g l i s h t e x t",   # 1 word with spaces
    " space before first word",  # 1 word with space before ==> generates error
    "space after last word ",  # 1 word with space after ==> generates error
    "English text with special characters !@#$%^&*()",  # 1 word with special characters
    # "English 1234567890",  # 1 word with numbers ==> separate tests
    "English . , ; : ' \"",  # 1 word with punctuation
])
def test1_add_todo_item_english_text(todo_text):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        # Wait for the app to load
        page.wait_for_selector("input.new-todo")

        # Add a new todo item
        # todo_text = "English text"
        page.fill("input.new-todo", todo_text)
        page.press("input.new-todo", "Enter")

        # Verify the new todo item appears in the list
        todo_items = page.locator("ul.todo-list li")
        assert todo_items.count() == 1
        assert todo_items.nth(0).locator("label").inner_text() == todo_text

        page.screenshot(path="running.png")

        browser.close()
