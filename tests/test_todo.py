import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(autouse=True)
def setup_vars(request):
    # This fixture will run before each test in the class
    request.cls.base_url = "https://demo.playwright.dev/todomvc/#/"
    request.cls.screenshot_path = "running.png"


@pytest.mark.usefixtures("setup_vars")
class TestTodoMVC:
    # The test class for TodoMVC application
    # This class contains all the test cases for the TodoMVC application
    # def __init__(self):
    #     self.page = "https://demo.playwright.dev/todomvc/#/"

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
    def test_add_todo_item_english_text(self, todo_text):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

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

            page.screenshot(path=self.screenshot_path)

            browser.close()

    # A new todo item can be added using non-English characters.
    @pytest.mark.parametrize("todo_text", [
        "買い物に行く 食料品を買う",       # Japanese: Go shopping Buy groceries
        "去购物 买菜",              # Chinese: Go shopping Buy groceries
        "Go shopping Acheter des courses",   # English/French: Go shopping Buy groceries
        "اذهب للتسوق اشترِ البقالة",        # Arabic: Go shopping Buy groceries
        "Πήγαινε για ψώνια Αγόρασε τρόφιμα",      # Greek: Go shopping Buy groceries
        "Сходить за покупками Купить продукты"   # Russian: Go shopping Buy groceries

    ])
    def test_add_non_english_todo_item(self, todo_text):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

            page.wait_for_selector("input.new-todo")
            page.fill("input.new-todo", todo_text)
            page.press("input.new-todo", "Enter")

            todo_items = page.locator("ul.todo-list li")
            assert todo_items.count() == 1
            assert todo_items.nth(0).locator("label").inner_text() == todo_text

            page.screenshot(path=self.screenshot_path)

            browser.close()

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
    def test_add_todo_item_includes_numbers(self, todo_number):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

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

            page.screenshot(path=self.screenshot_path)

            browser.close()


    # A todo item can be marked as completed and appears correctly in the "Completed" view.
    def test_mark_todo_as_completed_and_check_completed_view(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

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

            page.screenshot(path=self.screenshot_path)
            browser.close()


    # A todo item can be deleted and no longer appears in any view.
    def test_delete_todo_item_and_verify_absence(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

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

            # Verify the All view (current page)
            assert page.locator("ul.todo-list li").count() == 0

            # Verify the Active view (active href)
            page.goto(self.base_url + "active")
            assert page.locator("ul.todo-list li").count() == 0

            # Verify the Completed view (completed href)
            page.goto(self.base_url + "completed")
            assert page.locator("ul.todo-list li").count() == 0
            
            page.screenshot(path=self.screenshot_path)
            browser.close()


    # The "Active" filter correctly shows only items that are not completed.
    def test_active_filter_shows_only_uncompleted_items(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

            # Add two todo items
            page.fill("input.new-todo", "Task 1")
            page.press("input.new-todo", "Enter")
            page.fill("input.new-todo", "Task 2")
            page.press("input.new-todo", "Enter")

            # Mark the first item as completed
            page.check("ul.todo-list li:nth-child(1) .toggle")

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

            page.screenshot(path=self.screenshot_path)
            browser.close()


    # The "Completed" filter correctly shows only items that have been marked as completed.
    def test_completed_filter_shows_only_completed_items(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url)

            # Add two todo items
            page.fill("input.new-todo", "Task 1")
            page.press("input.new-todo", "Enter")
            page.fill("input.new-todo", "Task 2")
            page.press("input.new-todo", "Enter")

            # Mark the first item as completed
            page.check("ul.todo-list li:nth-child(1) .toggle")

            # Click on the "Completed" filter
            filters = page.locator("ul.filters li")
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

            page.screenshot(path=self.screenshot_path)
            browser.close()
