from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def wait(self, until, who=None, timeout=30, step=0.1):
    if who is None:
        who = self.driver
    return WebDriverWait(who, timeout, step).until(until)


def before_all(context):
    context.browser = webdriver.PhantomJS()
    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'


def after_all(context):
    context.browser.quit()


def before_feature(context, feature):
    pass
