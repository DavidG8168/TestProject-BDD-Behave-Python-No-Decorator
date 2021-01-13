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
