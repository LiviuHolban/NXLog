# NXLog
NXLog Test Task

Test Task
Using Playwright with Python, write automated tests for the following website:
https://demo.playwright.dev/todomvc/#/
Your tests should cover the following requirements:

1 A new todo item can be added using English text.

2 A new todo item can be added using non-English characters.

3 A new todo item can be added that includes numbers.

4 A todo item can be marked as completed and appears correctly in the "Completed"
view.

5 A todo item can be deleted and no longer appears in any view.

6 The "Active" filter correctly shows only items that are not completed.

7 The "Completed" filter correctly shows only items that have been marked as completed.

Kindly submit your code in a public GitHub repository. Please include a brief README.md file
with clear instructions on how to run your tests. This is a great opportunity to showcase your
best work.



# TodoMVC Playwright Tests

This repository contains automated tests for the TodoMVC demo site using Playwright with Python.

## Requirements
- Python 3.7+
- Playwright

## Installation
1. Clone the repository:
   git clone https://github.com/LiviuHolban/NXLog.git
   cd NXLog

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`

3. Install dependencies:
   pip install -r requirements.txt

4. Install Playwright browsers:
   playwright install

## Running Tests
To run all tests:
   python -m pytest .\tests\test_todo.py --html=report.html --self-contained-html
   or just
   pytest .\tests\test_todo.py --html=report.html --self-contained-html

To run a specific test from inside the class:
    pytest tests/test_todo.py::TestTodoMVC::test_add_todo_item_english_text 

To run a specific test file:
   python -m pytest .\tests\test1.py --html=report.html --self-contained-html
