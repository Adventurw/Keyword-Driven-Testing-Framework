from framework.keyword_map import build_keyword_map
from framework.excel_reader import ExcelReader
import conftest


def _load_case_ids():
    reader = ExcelReader("test_data/TestSuite.xlsx", steps_sheet="Sheet")
    return list(reader.get_test_steps().keys())


def test_driver(test_steps, object_repo, tc_id):
    steps = test_steps[tc_id]

    context = {"repo": object_repo, "driver": None}
    kw_map = build_keyword_map(context)

    print(f"\n>>> Running {tc_id}")
    current_step = ""
    try:
        for step in steps:
            keyword = step["Keyword"]
            current_step = f"{keyword} | {step.get('ObjectName') or '-'} | {step.get('TestData') or '-'}"

            func = kw_map.get(keyword)
            if not func:
                raise ValueError(f"Unknown keyword: {keyword!r} (row: {step})")

            func(
                object_name=step.get("ObjectName"),
                test_data=step.get("TestData") if step.get("TestData") is None else str(step.get("TestData")),
                description=step.get("Description"),
            )

        conftest.RESULTS[tc_id] = {"result": "PASS", "step": "", "message": ""}

    except Exception as e:
        conftest.RESULTS[tc_id] = {
            "result": "FAIL",
            "step": current_step,
            "message": f"{type(e).__name__}: {e}"[:500],
        }
        raise

    finally:
        if context.get("driver"):
            context["driver"].quit()


def pytest_generate_tests(metafunc):
    if "tc_id" in metafunc.fixturenames:
        metafunc.parametrize("tc_id", _load_case_ids())