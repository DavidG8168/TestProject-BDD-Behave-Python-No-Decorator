from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HelperFunc(object):
    __TIMEOUT = 15

    def __init__(self, driver):
        super(HelperFunc, self).__init__()
        self._driver_wait = WebDriverWait(driver, HelperFunc.__TIMEOUT)
        self._driver = driver
        self.disable_auto_reports()

    # Retrieve the TestProject driver from the helper.
    def get_driver(self):
        return self._driver

    # Helper functions for  in environment.py.

    def disable_auto_reports(self):
        self._driver.report().disable_auto_test_reports(True)
        self._driver.report().disable_command_reports(True)

    def report_step(self, step_description, step_message, step_status):
        self._driver.report().step(description=step_description, message=step_message, passed=step_status)

    def report_test(self, test_name, test_status):
        self._driver.report().test(name=test_name, passed=test_status)
