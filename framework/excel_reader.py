from openpyxl import load_workbook


class ExcelReader:
    def __init__(self, path, steps_sheet=None):
        self.wb = load_workbook(path)
        self.sheet = self.wb[steps_sheet] if steps_sheet else self.wb.active

    def _rows(self):
        headers = [c.value for c in self.sheet[1]]
        for row in self.sheet.iter_rows(min_row=2, values_only=True):
            if any(row):
                yield dict(zip(headers, row))

    def get_test_steps(self):
        cases = {}
        for r in self._rows():
            cases.setdefault(r["TC_ID"], []).append(r)
        return cases

    def get_object_repository(self, sheet_name="Objects"):
        ws = self.wb[sheet_name]
        headers = [c.value for c in ws[1]]
        repo = {}
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:
                continue
            data = dict(zip(headers, row))
            repo[data["ObjectName"]] = (data["LocatorType"], data["LocatorValue"])
        return repo