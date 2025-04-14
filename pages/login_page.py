from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    USERNAME_SELECTOR = "#login-email-input"
    PASSWORD_SELECTOR = "#login-password-input"
    LOGIN_BUTTON_SELECTOR = '[data-test="login-submit"]'
    PROFILE_URL = "https://app.clickup.com/90151055614/v/l/2kypqw7y-335"
    FORM_ERROR_SELECTOR = '[data-test="form__error"]'
    ERROR_TEXT = "Incorrect password for this email."

    def login(self, username, password):
        allure.attach(
            f"Logging in with {username}", 
            name="Login attempt", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_url_is_correct(self.PROFILE_URL)

    def login_with_incorrect_password(self, username, password):
        allure.attach(
            f"Logging in with {username} and incorrect password", 
            name="Failed login attempt", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_element_is_visible(self.FORM_ERROR_SELECTOR)
        self.assert_text_in_element(self.FORM_ERROR_SELECTOR, self.ERROR_TEXT)