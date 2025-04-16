import allure
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

TASK_NAME = 'My First Task from API'

@allure.title("Удаление задачи после логина")
def test_delete_task(browser, task_fixture_only_create):
    page = browser.new_page()
    login_page = LoginPage(page)
    profile_page = ProfilePage(page)

    with allure.step("Логинимся в систему"):
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

        assert profile_page.check_profile_page(), "Профиль не открыт после логина"

    with allure.step(f"Удаляем задачу: {TASK_NAME}"):
        task_fixture_only_create
        profile_page.delete_task(TASK_NAME)
        assert not profile_page.task_does_not_exist(TASK_NAME), (
            f"Задача '{TASK_NAME}' всё ещё существует"
        )