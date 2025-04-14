from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

WRONG_PASSWORD = "qwertyuiop"
TASK_NAME = 'test task'

def test_login_success(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    profile_page = ProfilePage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
    profile_page.check_profile_page()

def test_login_fail(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.login_with_incorrect_password(CLICKUP_EMAIL, WRONG_PASSWORD)

def test_delete_task(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    profile_page = ProfilePage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    profile_page.check_profile_page()
    
    profile_page.create_task(TASK_NAME)
    profile_page.delete_task(TASK_NAME)
