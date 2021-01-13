from src.testproject.sdk.drivers import webdriver
from behave.fixture import use_fixture_by_tag
import os
from configparser import ConfigParser
from features.helpers.web_helper import get_browser

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
