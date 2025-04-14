import allure
from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '90151055614/v/l/2kypqw7y-335'

    WORKSPASE_TEXT = "Ilia Karpenko's Workspace"
    HOME_TEXT = "Home"
    INBOX_TEXT = "Inbox"
    ADD_TASK_BTN_SELECTOR = (
        ".cu-task-list-footer__add-dropdown-button.ng-star-inserted"
    )
    TASK_NAME_SELECTOR = '[data-test="task-row-new__input"]'
    SAVE_TASK_BTN_SELECTOR = '[data-test="task-row-new__button"]'
    SELECT_TASK_BUTON_SELECTOR = (
        "cu-task-row-toggle.cu-task-row-toggle_alt.cu-task-row-toggle_list-view-v3."
        "ng-star-inserted"
    )
    DELETE_BTN_SELECTOR = '[data-test="dashboard-table-toolbar-delete-tasks"]'

    def check_profile_page(self):
        allure.attach(
            f"Checking profile page for {self.WORKSPASE_TEXT}", 
            name="Profile page check", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        self.assert_text_on_page(self.WORKSPASE_TEXT)
        self.assert_text_on_page(self.HOME_TEXT)
        self.assert_text_on_page(self.INBOX_TEXT)

    def create_task(self, task_name):
        allure.attach(
            f"Creating task: {task_name}", 
            name="Create task", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        self.wait_for_selector_and_click(self.ADD_TASK_BTN_SELECTOR)
        self.wait_for_selector_and_fill(self.TASK_NAME_SELECTOR, task_name)
        self.wait_for_selector_and_click(self.SAVE_TASK_BTN_SELECTOR)
        self.assert_text_on_page(task_name)

    def delete_task(self, task_name):
        allure.attach(
            f"Deleting task: {task_name}", 
            name="Delete task", 
            attachment_type=allure.attachment_type.TEXT
        )
        
        self.wait_for_selector_and_click(self.SELECT_TASK_BUTON_SELECTOR)
        self.wait_for_selector_and_click(self.DELETE_BTN_SELECTOR)
        self.assert_text_not_on_page(task_name)