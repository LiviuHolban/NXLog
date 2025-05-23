import pytest
from playwright.sync_api import sync_playwright

# The "Active" filter correctly shows only items that are not completed.
def test_active_filter_shows_only_uncompleted_items():
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

        # # Verify the Active view (active href)
        # page.goto("https://demo.playwright.dev/todomvc/#/active")

        # Click on the "Active" filter
        filters = page.locator("ul.filters li")
        assert filters.nth(1).inner_text() == "Active"
        filters.nth(1).click()
        counts = filters.count()
        f = filters.nth(0)
        for i in range(counts):
            if filters.nth(i).inner_text() == "Active":
                f = filters.nth(i)
                break
        f.click()

        # Verify only the uncompleted item is shown
        active_items = page.locator("ul.todo-list li")
        assert active_items.count() == 1
        assert active_items.nth(0).locator("label").inner_text() == "Task 2"
        
        page.screenshot(path="running.png")
        browser.close()
