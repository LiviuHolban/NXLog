# NXLog
NXLog Test Task

Test Task
Using Playwright with Python, write automated tests for the following website:
https://demo.playwright.dev/todomvc/#/
Your tests should cover the following requirements:
• A new todo item can be added using English text.
• A new todo item can be added using non-English characters.
• A new todo item can be added that includes numbers.
• A todo item can be marked as completed and appears correctly in the "Completed"
view.
• A todo item can be deleted and no longer appears in any view.
• The "Active" filter correctly shows only items that are not completed.
• The "Completed" filter correctly shows only items that have been marked as completed.
Kindly submit your code in a public GitHub repository. Please include a brief README.md file
with clear instructions on how to run your tests. This is a great opportunity to showcase your
best work.



Code:

1. Instalation requirements:
pip install -r requirements.txt playwright install

2. Run the tests command in the terminal:
python -m pytest test1.py --html=report.html --self-contained-html

Modify the "test1.py" to the next files with counters in file name 2,3,4,5,6,7 to test/validate all the tests.

3. Open the report.html file in your browser to see the test results.
