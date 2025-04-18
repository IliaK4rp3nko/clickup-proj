import allure
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

WRONG_PASSWORD = "qwertyuiop"
ERROR_TEXT = "Incorrect password for this email."


@allure.title("Проверка логина c корректным паролем")
def test_login(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    profile_page = ProfilePage(page)

    with allure.step("Входим с корректными данными"):
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

        assert profile_page.check_profile_page(), (
            "Не удалось попасть на страницу профиля")


@allure.title("Проверка логина с некорректным паролем")
def test_login_with_wrong_password(browser):
    page = browser.new_page()
    login_page = LoginPage(page)

    with allure.step("Пытаемся войти с неверным паролем"):
        login_page.login_with_incorrect_password(CLICKUP_EMAIL, WRONG_PASSWORD)
        assert login_page.is_text_visible(ERROR_TEXT), "Ожидалось сообщение об ошибке"
