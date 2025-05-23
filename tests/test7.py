import pytest
from playwright.sync_api import sync_playwright

# The "Completed" filter correctly shows only items that have been marked as completed.
def test_completed_filter_shows_only_completed_items():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc/#/")

        # Add two todo items
        page.fill("input.new-todo", "Task 1")
        page.press("input.new-todo", "Enter")
        page.fill("input.new-todo", "Task 2")
        page.press("input.new-todo", "Enter")

        # Mark the first item as completed
        page.check("ul.todo-list li:nth-child(1) .toggle")

        # # Verify the Completed view (completed href)
        # page.goto("https://demo.playwright.dev/todomvc/#/completed")

        # Click on the "Completed" filter
        filters = page.locator("ul.filters li")
        # assert filters.nth(2).inner_text() == "Completed"
        # filters.nth(2).click()
        counts = filters.count()
        f = filters.nth(0)
        for i in range(counts):
            if filters.nth(i).inner_text() == "Completed":
                f = filters.nth(i)
                break
        f.click()

        # Verify only the completed item is shown
        completed_items = page.locator("ul.todo-list li")
        assert completed_items.count() == 1
        assert completed_items.nth(0).locator("label").inner_text() == "Task 1"
        assert "completed" in completed_items.nth(0).get_attribute("class")

        page.screenshot(path="running.png")
        browser.close()
