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

