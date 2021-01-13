BDD with TestProject and Behave in Python

Prerequisites:

1.	Install Behave:
```
pip install behave
```

2.	Install TestProject Python OpenSDK:
```
pip3 install testproject-python-sdk
```

3.	Create a ‘Features’ folder.
 
4.	Inside the folder, create your ‘.feature’ files. For example:
```
Feature: TestProject with Behave Framework

  Scenario: Run a Simple BDD test with TestProject
     Given I navigate to the TestProject example page
     When I perform a login
     Then I should see a logout button
```
 
5.	Then you’ll need to create your step definitions, create a folder called ‘steps’ inside your ‘features’ folder, and there create a class with your step definitions.
 
You can also hover over the steps in your feature file with no created definitions and select the option to automatically create one for you:
 
To view your reports on TestProject, you’ll need to setup the TestProject driver for your Selenium tests or use the TestProject Generic driver for non-UI tests.
The driver will need pass into the context used by each step and scenario.
To pass the driver into the context, you’ll need to store it in the context before starting to run your tests.
To do that we’ll start by creating a helper object to store the driver and handle our reporting for us.
1.	In your ‘Features’  folder create another folder called ‘helpers’, and in there create a new ‘.py’ file to store where we will create a class to store the driver. Here we’ll call it ‘selenium_helper.py’
 
The ‘HelperFunc’ class will store the driver and handle reporting.
You can use the following code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

```
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
 ```

Next, we’ll setup a configuration file where you can decide with type of driver you’d like to use, specify your developer token, project name and job name for your TestProject report.
Create a file called ‘setup.cfg’ at the root of your project and fill it with the following details:
 
 ```
[Browser]
Browser = browser_type
[Token]
Token = my_dev_token
[Project]
Project = my_project_name
[Job]
Job = my_job_name
```

Then we can create another helper that will create the class that creates your driver based on the information from the setup.cfg file, create another .py file in your ‘helpers’ folder, here we’ll call it ‘web_helper.py’.
 
You can use the following code:

```
from src.testproject.sdk.drivers import webdriver
from .selenium_helper import HelperFunc


def get_browser(browser, token, project, job):
    if browser == "chrome":
        return HelperFunc(webdriver.Chrome(token=token, projectname=project, jobname=job))
    if browser == "firefox":
        return HelperFunc(webdriver.Firefox(token=token, projectname=project, jobname=job))
    if browser == "edge":
        return HelperFunc(webdriver.Edge(token=token, projectname=project, jobname=job))
    if browser == "safari":
        return HelperFunc(webdriver.Safari(token=token, projectname=project, jobname=job))
    if browser == "ie":
        return HelperFunc(webdriver.Ie(token=token, projectname=project, jobname=job))
    if browser == "generic":
        return HelperFunc(webdriver.Generic(token=token, project_name=project, job_name=job))
  ```
  
The final step would be to create our ‘environmet.py’ file where we define our execution hooks, in here in the before_all hook, we can create our driver and store it in the context to be passed to all our steps.
Create ‘environment.py’ in your ‘features’ folder.
 
You can use the following code:

```
from src.testproject.sdk.drivers import webdriver
from behave.fixture import use_fixture_by_tag
import os
from configparser import ConfigParser
from helper.helper_web import get_browser

""" Executed once per test run: Before any features and scenarios are run.
    Initialize the driver and start the session.
"""


def before_all(context):
    config = ConfigParser()
    configuration_file = (os.path.join(os.getcwd(), 'setup.cfg'))
    config.read(configuration_file)

    # Reading details from the setup.cfg at the base of the project.
    # Browser type.
    # TestProject developer token.
    # Project name.
    # Job name.
    helper_func = get_browser(config.get('Browser', 'Browser'),
                              config.get('Token', 'Token'),
                              config.get('Project', 'Project'),
                              config.get('Job', 'Job')
                              )
    context.helperfunc = helper_func


""" Executed after each step in the scenario.
    Reports the test step.
"""


def after_step(context, step):
    step_description = "{} {}".format(step.keyword, step.name)
    step_passed = True if step.status == 'passed' else False
    step_message = "{} {}".format(str(step.exception), step.error_message) if not step_passed else step_description
    context.helperfunc.report_step(step_description, step_message, step_passed)


""" Executed after each scenario in the feature.
    Reports the scenario as a test.
"""


def after_scenario(context, scenario):
    test_name = scenario.name
    test_passed = True if scenario.status == 'passed' else False
    context.helperfunc.report_test(test_name, test_passed)


""" Executed once per test run: after all features and scenarios are run.
    Quit the driver and close the session.
"""


def after_all(context):
    context.helperfunc.get_driver().quit()
```

Now the TestProject driver will be stored in your context, and you can use it in all your step definitions to create your Selenium or non-UI based tests.
For example, let’s edit our step definitions to perform a simple login and validation scenario:

```
from behave import *


@given('I navigate to the TestProject example page')
def step_impl(context):
    context.helperfunc.get_driver().get("https://example.testproject.io/web/")


@when('I perform a login')
def step_impl(context):
    context.helperfunc.get_driver().find_element_by_css_selector("#name").send_keys("John Smith")
    context.helperfunc.get_driver().find_element_by_css_selector("#password").send_keys("12345")
    context.helperfunc.get_driver().find_element_by_css_selector("#login").click()


@then('I should see a logout button')
def step_impl(context):
    passed = context.helperfunc.get_driver().find_element_by_css_selector("#logout").is_displayed()
    assert passed is True
```

By utilizing the TestProject driver in your tests, you’ll be able to view your test reports and statistics on the TestProject platform.
 
