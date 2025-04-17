import time
import allure
from tests.config import BASE_URL_FRONT, WORKSPACE_ID, FOLDER_ID
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    USERNAME_SELECTOR = "#login-email-input"
    PASSWORD_SELECTOR = "#login-password-input"
    LOGIN_BUTTON_SELECTOR = '[data-test="login-submit"]'
    PROFILE_URL = f"{BASE_URL_FRONT}{WORKSPACE_ID}/v/l/{FOLDER_ID}"
    FORM_ERROR_SELECTOR = '[data-test="form__error-password"]'

    def _fill_and_submit_login_form(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)

    def login(self, username, password):
        allure.attach(
            f"Успешный логин с {username}",
            name="Попытка успешного логина",
            attachment_type=allure.attachment_type.TEXT
        )
        self._fill_and_submit_login_form(username, password)
        self.assert_url_is_correct(self.PROFILE_URL)
        time.sleep(3)

    def login_with_incorrect_password(self, username, password):
        allure.attach(
            f"Логин с {username} и невалидным паролем",
            name="Неуспешный логин",
            attachment_type=allure.attachment_type.TEXT
        )
        self._fill_and_submit_login_form(username, password)
        self.assert_element_is_visible(self.FORM_ERROR_SELECTOR)
        time.sleep(5)

    def is_error_message_displayed(self, error_text):
        with allure.step(f"Проверяем, что отображается сообщение об ошибке: '{error_text}'"):
            return self.assert_text_on_page(error_text)
