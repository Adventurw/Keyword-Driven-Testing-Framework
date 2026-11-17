from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(browser="chrome"):
    opts = Options()
    opts.add_argument("--start-maximized")

    # --- Kill Chrome's password manager & breach-detection popups ---
    prefs = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        "profile.password_manager_leak_detection": False,   # the "Change your password" bubble
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    }
    opts.add_experimental_option("prefs", prefs)
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    if browser.lower() == "chrome":
        return webdriver.Chrome(options=opts)
    elif browser.lower() == "firefox":
        return webdriver.Firefox()
    raise ValueError(f"Unsupported browser: {browser}")