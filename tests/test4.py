import pytest
from playwright.sync_api import sync_playwright

# A todo item can be marked as completed and appears correctly in the "Completed" view.
def test_mark_todo_as_completed_and_check_completed_view():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        # Wait for the input to be ready
        page.wait_for_selector("input.new-todo")

        # Add a new todo item
        todo_text = "item mark complete"
        page.fill("input.new-todo", todo_text)
        page.press("input.new-todo", "Enter")

        # Mark the item as completed
        page.check("ul.todo-list li .toggle")

        # # Click on the "Completed" filter
        # page.click("text=Completed")
        filters = page.locator("ul.filters li")
        assert filters.nth(2).inner_text() == "Completed"
        filters.nth(2).click()

        # Verify the completed item appears in the list
        completed_items = page.locator("ul.todo-list li")
        assert completed_items.count() == 1
        assert completed_items.nth(0).locator("label").inner_text() == todo_text
        assert "completed" in completed_items.nth(0).get_attribute("class")

        page.screenshot(path="running.png")
        browser.close()
