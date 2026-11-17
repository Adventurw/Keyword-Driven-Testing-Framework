import pytest
from pathlib import Path
from openpyxl import load_workbook

from framework.excel_reader import ExcelReader

EXCEL = Path("test_data/TestSuite.xlsx")

# Shared results collector: {TC_ID: {"result": "PASS"/"FAIL", "step": "...", "message": "..."}}
RESULTS = {}


@pytest.fixture(scope="session")
def excel():
    return ExcelReader(str(EXCEL), steps_sheet="Sheet")


@pytest.fixture(scope="session")
def test_steps(excel):
    return excel.get_test_steps()


@pytest.fixture(scope="session")
def object_repo(excel):
    return excel.get_object_repository()


def pytest_sessionfinish(session, exitstatus):
    """After all tests, write a 'Result' sheet back into TestSuite.xlsx."""
    if not RESULTS:
        return

    wb = load_workbook(EXCEL)
    if "Result" in wb.sheetnames:
        del wb["Result"]
    ws = wb.create_sheet("Result")

    ws.append(["TC_ID", "Result", "Failed Step", "Message"])
    for tc_id, info in RESULTS.items():
        ws.append([
            tc_id,
            info.get("result", ""),
            info.get("step", ""),
            info.get("message", ""),
        ])

    # Column widths for readability
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 40
    ws.column_dimensions["D"].width = 80

    wb.save(EXCEL)
    print(f"\n📋 Results written to {EXCEL} → sheet 'Result'")