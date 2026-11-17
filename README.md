# Keyword-Driven Testing Framework

A Python + Selenium test automation framework built around the **keyword-driven testing** methodology.

## What it is

Test cases live entirely in Excel. Testers write steps using business-friendly keywords
(`Open Browser`, `Login As`, `Click`, `Verify Text`) and reference elements by semantic
names (`usernameBox`, `loginButton`), never touching locators or code. A single Python
file maps each keyword to a Selenium action; a single Excel sheet maps each object name
to a locator.

## The workflow it enables

1. **Tester** adds a new row block to `TestSuite.xlsx` with a new `TC_ID` → done.
2. **Lead** (only when a new element appears) adds one row to the `Objects` sheet.
3. **Anyone** runs `pytest tests/` → one new test appears per `TC_ID`, runs, and reports.
4. **Results** are written back into `TestSuite.xlsx` in the `Result` tab (latest run)
   and `History` tab (timestamped, appended).

No code changes are required to add test cases — only to add a *new kind of action*
(a new keyword), which happens roughly once per new feature area.

## Why keyword-driven

| Traditional scripting | This framework |
|---|---|
| Testers must know Python/Selenium | Testers edit Excel |
| Locators are embedded in test code | Locators live in one `Objects` sheet |
| Adding a test = PR to codebase | Adding a test = new Excel rows |
| Debugging requires stack traces | Failed step + error written to Excel |

Non-technical QA contributors can own the test suite. Developers own the keyword
library (7 keywords today, ~15 after the current test-case scope). Reviewers review
the spreadsheet directly.

## Quick start

```bash
git clone <your-repo>
cd keyword_framework
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
copy test_data/TestSuite.template.xlsx test_data/TestSuite.xlsx   # Windows
pytest tests/ -v -s
```

### Populate `requirements.txt` correctly
You may have added `pytest-xdist` — update


