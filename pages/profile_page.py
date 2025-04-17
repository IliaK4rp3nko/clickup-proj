import allure
from pages.base_page import BasePage
from tests.config import WORKSPACE_ID, FOLDER_ID


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = f'{WORKSPACE_ID}/v/l/{FOLDER_ID}'

    WORKSPASE_TEXT = "Ilia Karpenko's Workspace"
    HOME_TEXT = "Home"
    INBOX_TEXT = "Inbox"
    ADD_TASK_BTN_SELECTOR = (
        ".cu-task-list-footer__add-dropdown-button.ng-star-inserted"
    )
    TASK_NAME_SELECTOR = '[data-test="task-row-new__input"]'
    SAVE_TASK_BTN_SELECTOR = '[data-test="task-row-new__button"]'
    SELECT_TASK_BUTON_SELECTOR = (
        '[data-test="task-row-main__My First Task from API"]'
    )
    TASK_MENU_BTN_SELECTOR = '[data-test="task-view-header__task-settings"]'
    DELETE_BTN_SELECTOR = '[data-test="dropdown-list-item__Delete"]'

    def check_profile_page(self):
        with allure.step(
            f"Проверяем наличие текста на странице профиля: "
            f"{self.WORKSPASE_TEXT}, {self.HOME_TEXT}, {self.INBOX_TEXT}"):
            self.assert_text_on_page(self.WORKSPASE_TEXT)
            self.assert_text_on_page(self.HOME_TEXT)
            self.assert_text_on_page(self.INBOX_TEXT)
            return True

    def create_task(self, task_name):
        with allure.step(f"Создаём задачу с названием: {task_name}"):
            self.wait_for_selector_and_click(self.ADD_TASK_BTN_SELECTOR)
            self.wait_for_selector_and_fill(self.TASK_NAME_SELECTOR, task_name)
            self.wait_for_selector_and_click(self.SAVE_TASK_BTN_SELECTOR)
            self.assert_text_on_page(task_name)

    def delete_task(self, task_name):
        with allure.step(f"Удаляем задачу из списка: {task_name}"):
            self.wait_for_selector_and_click(self.SELECT_TASK_BUTON_SELECTOR)
            self.wait_for_selector_and_click(self.TASK_MENU_BTN_SELECTOR)
            self.wait_for_selector_and_click(self.DELETE_BTN_SELECTOR)

    def task_does_not_exist(self, task_name):
        self.assert_text_not_on_page(task_name)

    def task_exist(self, task_name):
        try:
            self.assert_text_on_page(task_name)
            return True
        except AssertionError:
            return False
