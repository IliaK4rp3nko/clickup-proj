import allure
import pytest
from config import BASE_URL, LIST_ID
from ui.test_board_page import TASK_NAME
from playwright.sync_api import sync_playwright
from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY


@pytest.fixture(scope="session")
def clickup_client():
    return ClickUpClient(
        base_url=BASE_URL,
        api_key=CLICKUP_API_KEY
    )


@pytest.fixture()
def post_data():
    with allure.step("Формирование валидных данных задачи"):
        return {
            "name": "My First Task from API",
            "description": "Created via ClickUp API 🎯",
            "status": "to do"
        }


@pytest.fixture()
def updated_data():
    with allure.step("Формирование обновлённых данных"):
        return {
            "name": "Updated data",
            "description": "Updated description",
            "status": "in progress"
        }


@pytest.fixture()
def invalid_data():
    with allure.step("Формирование невалидных данных"):
        return {
            "name": "",
            "description": "12345",
            "status": "not_a_status"
        }


@pytest.fixture
def task_fixture(clickup_client, post_data):
    list_id = LIST_ID

    with allure.step("Создание задачи"):
        create_response = clickup_client.create_task(list_id, post_data)
        assert create_response.status_code == 200, "Ошибка создания задачи"
        task = create_response.json()
        task_id = task["id"]

    yield task

    with allure.step("Удаление задачи"):
        delete_response = clickup_client.delete_task(task_id)
        assert delete_response.status_code == 204, "Ошибка удаления"

    with allure.step("Проверка удаления"):
        check_response = clickup_client.check_task_exists(task_id)
        assert check_response.status_code == 404, "Задача не удалена"


@pytest.fixture
def task_fixture_only_create(clickup_client, post_data):
    list_id = LIST_ID
    with allure.step("Создание задачи"):
        create_response = clickup_client.create_task(list_id, post_data)
        assert create_response.status_code == 200, "Ошибка создания"
        task = create_response.json()

    yield task


@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def delete_task_if_exists(clickup_client):
    def _delete():
        with allure.step("Проверяем наличие таска и удаляем его, если найден"):
            response = clickup_client.get_task_list(LIST_ID)
            task_id = clickup_client.get_task_id_by_name(response, TASK_NAME)

            if task_id:
                delete_response = clickup_client.delete_task(task_id)
                assert delete_response.status_code == 204, f"Не удалось удалить таск {task_id}"
            else:
                print(f"Таск с названием '{TASK_NAME}' не найден — ничего не удаляем")

    yield _delete
