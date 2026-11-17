import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOCATOR_MAP = {
    "id": By.ID,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "class": By.CLASS_NAME,
    "link_text": By.LINK_TEXT,
}


class KeywordActions:
    def __init__(self, context):
        self.ctx = context
    

    def _find(self, object_name):
        loc_type, loc_val = self.ctx["repo"][object_name]
        by = LOCATOR_MAP[loc_type.lower()]
        return WebDriverWait(self.ctx["driver"], 10).until(
            EC.presence_of_element_located((by, loc_val))
        )

    def open_browser(self, object_name=None, test_data=None, description=None):
        from framework.driver_factory import create_driver
        self.ctx["driver"] = create_driver(test_data or "chrome")
        print(f"  [Open Browser] {test_data or 'chrome'}")

    def navigate(self, object_name=None, test_data=None, description=None):
        self.ctx["driver"].get(test_data)
        print(f"  [Navigate] -> {test_data}")

    def enter_text(self, object_name, test_data, description=None):
        el = self._find(object_name)
        el.clear()
        el.send_keys(str(test_data))
        print(f"  [Enter Text] {object_name} = '{test_data}'")

    def click(self, object_name, test_data=None, description=None):
        self._find(object_name).click()
        print(f"  [Click] {object_name}")

    def verify_text(self, object_name, test_data, description=None):
       el = self._find(object_name)
       expected = str(test_data)   # ← coerce in case Excel sent an int/float
       actual = el.text
       assert expected in actual, f"Expected '{expected}' in '{actual}'"
       print(f"  [Verify Text] OK - '{expected}' found")

    def wait(self, object_name=None, test_data=None, description=None):
        time.sleep(float(test_data))
        print(f"  [Wait] {test_data}s")

    def close_browser(self, object_name=None, test_data=None, description=None):
        if self.ctx.get("driver"):
            self.ctx["driver"].quit()
            self.ctx["driver"] = None
        print("  [Close Browser]")

    # --- Composite keywords ---

    def login_as(self, object_name=None, test_data=None, description=None):
        """Composite: log in. test_data = 'username|password'."""
        user, pwd = test_data.split("|")
        self.navigate(test_data="https://www.saucedemo.com")
        self.enter_text("usernameBox", user)
        self.enter_text("passwordBox", pwd)
        self.click("loginButton")
        print(f"  [Login As] {user}")
    
    def add_to_cart(self, object_name=None, test_data=None, description=None):
        """Composite: click an add-to-cart button by product name."""
        self.click(f"addBtn_{test_data}")
        print(f"  [Add To Cart] {test_data}")
    
    def checkout_with(self, object_name=None, test_data=None, description=None):
        """Composite: complete the 3-step checkout. test_data = 'First|Last|Zip'."""
        first, last, zipc = test_data.split("|")
        self.click("cartIcon")
        self.click("checkoutBtn")
        self.enter_text("firstNameField", first)
        self.enter_text("lastNameField", last)
        self.enter_text("zipField", zipc)
        self.click("continueBtn")
        self.click("finishBtn")
        print(f"  [Checkout With] {first} {last} {zipc}")
    
    # --- New atomic keywords ---
    
    def verify_url(self, object_name=None, test_data=None, description=None):
        current = self.ctx["driver"].current_url
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        assert expected in current, f"Expected '{expected}' in URL '{current}'"
        print(f"  [Verify URL] OK - '{expected}' in '{current}'")
    
    def verify_title(self, object_name=None, test_data=None, description=None):
        title = self.ctx["driver"].title
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        assert expected in title, f"Expected '{expected}' in title '{title}'"
        print(f"  [Verify Title] OK - '{expected}' in title")
    
    def verify_element_present(self, object_name, test_data=None, description=None):
        self._find(object_name)
        print(f"  [Verify Element Present] OK - '{object_name}' exists")
    
    def verify_element_absent(self, object_name, test_data=None, description=None):
        loc_type, loc_val = self.ctx["repo"][object_name]
        by = LOCATOR_MAP[loc_type.lower()]
        elements = self.ctx["driver"].find_elements(by, loc_val)
        visible = [e for e in elements if e.is_displayed()]
        assert len(visible) == 0, \
            f"Expected no visible '{object_name}', found {len(visible)} visible"
        print(f"  [Verify Element Absent] OK - '{object_name}' not visible")

        by = LOCATOR_MAP[loc_type.lower()]
        elements = self.ctx["driver"].find_elements(by, loc_val)
        assert len(elements) == 0, f"Expected no '{object_name}', found {len(elements)}"
        print(f"  [Verify Element Absent] OK - '{object_name}' not present")
    
    def verify_attribute(self, object_name, test_data=None, description=None):
        """test_data = 'attributeName=expectedValue'."""
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        attr, expected = test_data.split("=", 1)
        el = self._find(object_name)
        actual = el.get_attribute(attr)
        assert actual == expected, f"Attribute '{attr}' expected '{expected}', got '{actual}'"
        print(f"  [Verify Attribute] OK - {object_name}[{attr}]='{expected}'")
    
    def verify_enabled(self, object_name, test_data=None, description=None):
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        el = self._find(object_name)
        assert el.is_enabled(), f"Element '{object_name}' is disabled"
        print(f"  [Verify Enabled] OK - '{object_name}' enabled")
    
    def verify_disabled(self, object_name, test_data=None, description=None):
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        el = self._find(object_name)
        assert not el.is_enabled(), f"Element '{object_name}' is enabled"
        print(f"  [Verify Disabled] OK - '{object_name}' disabled")
    
    def verify_count(self, object_name, test_data=None, description=None):
        """test_data = expected count (int as string)."""
        expected = str(test_data)   # ← coerce in case Excel sent an int/float
        loc_type, loc_val = self.ctx["repo"][object_name]
        by = LOCATOR_MAP[loc_type.lower()]
        elements = self.ctx["driver"].find_elements(by, loc_val)
        assert len(elements) == int(expected), \
            f"Expected {test_data} '{object_name}', found {len(elements)}"
        print(f"  [Verify Count] OK - {len(elements)} '{object_name}'")
    
    def select_dropdown(self, object_name, test_data=None, description=None):
        from selenium.webdriver.support.ui import Select
        el = self._find(object_name)
        Select(el).select_by_visible_text(test_data)
        print(f"  [Select Dropdown] {object_name} <- '{test_data}'")
    
    def refresh_page(self, object_name=None, test_data=None, description=None):
        self.ctx["driver"].refresh()
        print("  [Refresh Page]")
    
    def clear_cookies(self, object_name=None, test_data=None, description=None):
        self.ctx["driver"].delete_all_cookies()
        print("  [Clear Cookies]")
    
    def go_back(self, object_name=None, test_data=None, description=None):
        self.ctx["driver"].back()
        print("  [Go Back]")
    
    def accept_alert(self, object_name=None, test_data=None, description=None):
        WebDriverWait(self.ctx["driver"], 5).until(EC.alert_is_present())
        alert = self.ctx["driver"].switch_to.alert
        text = alert.text
        alert.accept()
        print(f"  [Accept Alert] '{text}'")
    
    def dismiss_alert(self, object_name=None, test_data=None, description=None):
        WebDriverWait(self.ctx["driver"], 5).until(EC.alert_is_present())
        alert = self.ctx["driver"].switch_to.alert
        text = alert.text
        alert.dismiss()
        print(f"  [Dismiss Alert] '{text}'")
    
    def check_checkbox(self, object_name, test_data=None, description=None):
        el = self._find(object_name)
        if not el.is_selected():
            el.click()
        print(f"  [Check Checkbox] {object_name}")
    
    def uncheck_checkbox(self, object_name, test_data=None, description=None):
        el = self._find(object_name)
        if el.is_selected():
            el.click()
        print(f"  [Uncheck Checkbox] {object_name}")    