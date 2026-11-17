from framework.keyword_actions import KeywordActions


def build_keyword_map(context):
    actions = KeywordActions(context)
    return {
        # Navigation / lifecycle
        "Open Browser":           actions.open_browser,
        "Navigate":               actions.navigate,
        "Refresh Page":           actions.refresh_page,
        "Go Back":                actions.go_back,
        "Clear Cookies":          actions.clear_cookies,
        "Close Browser":          actions.close_browser,

        # Composites (business-level actions)
        "Login As":               actions.login_as,
        "Add To Cart":            actions.add_to_cart,
        "Checkout With":          actions.checkout_with,

        # Input
        "Enter Text":             actions.enter_text,
        "Click":                  actions.click,
        "Select Dropdown":        actions.select_dropdown,
        "Check Checkbox":         actions.check_checkbox,
        "Uncheck Checkbox":       actions.uncheck_checkbox,

        # Alerts
        "Accept Alert":           actions.accept_alert,
        "Dismiss Alert":          actions.dismiss_alert,

        # Assertions
        "Verify Text":            actions.verify_text,
        "Verify URL":             actions.verify_url,
        "Verify Title":           actions.verify_title,
        "Verify Element Present": actions.verify_element_present,
        "Verify Element Absent":  actions.verify_element_absent,
        "Verify Attribute":       actions.verify_attribute,
        "Verify Enabled":         actions.verify_enabled,
        "Verify Disabled":        actions.verify_disabled,
        "Verify Count":           actions.verify_count,

        # Utility
        "Wait":                   actions.wait,
    }