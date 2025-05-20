import pytest
from playwright.sync_api import sync_playwright

# A new todo item can be added using non-English characters.
@pytest.mark.parametrize("todo_text", [
    "買い物に行く",       # Japanese
    "买菜",              # Chinese
    "English French",   # English/French
    "شراء الخبز",        # Arabic
    "Αγορά ψωμιού",      # Greek
    "Купить продукты",   # Russian
])
def test_add_non_english_todo_item(todo_text):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        page.wait_for_selector("input.new-todo")
        page.fill("input.new-todo", todo_text)
        page.press("input.new-todo", "Enter")

        todo_items = page.locator("ul.todo-list li")
        assert todo_items.count() == 1
        assert todo_items.nth(0).locator("label").inner_text() == todo_text

        page.screenshot(path="running.png")

        browser.close()
