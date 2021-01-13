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

