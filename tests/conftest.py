import allure
import pytest
import requests
from utils.helpers import CLICKUP_API_KEY
from config import BASE_URL, CREATE_TASK_URL

import pytest
from playwright.sync_api import sync_playwright


@allure.title("Фикстура авторизованной сессии")
@pytest.fixture(scope="session")
def auth_session():
    with allure.step("Создание сессии авторизации"):
        session = requests.session()
        session.headers.update({
            'Authorization': f'{CLICKUP_API_KEY}',
            'Content-Type': 'application/json'
        })
    return session

@allure.title("Фикстура данных для создания задачи")
@pytest.fixture()
def post_data():
    with allure.step("Формирование валидных данных задачи"):
        data = {
            "name": "My First Task from API",
            "description": "Created via ClickUp API 🎯",
            "status": "to do"
        }
    return data

@allure.title("Фикстура данных для обновления задачи")
@pytest.fixture()
def updated_data():
    with allure.step("Формирование обновлённых данных для PUT-запроса"):
        data = {
            "name": "Updated data",
            "description": "Updated description",
            "status": "in progress"
        }
    return data

@allure.title("Фикстура с невалидными данными")
@pytest.fixture()
def invalid_data():
    with allure.step("Формирование невалидных данных задачи"):
        data = {
            "name": "",
            "description": "12345",
            "status": "not_a_status"
        }
    return data

@allure.title("Фикстура создания и удаления задачи")
@pytest.fixture
def task_fixture(auth_session, post_data):
    with allure.step("Создание задачи через API"):
        create_response = auth_session.post(
            f"{BASE_URL}{CREATE_TASK_URL}",
            json=post_data
        )
        assert create_response.status_code == 200,(
            "Ошибка при создании задачи")
        task = create_response.json()
        task_id = task["id"]

        yield task

    with allure.step("Удаление задачи"):
        delete_response = auth_session.delete(
            f"{BASE_URL}/v2/task/{task_id}"
        )
        assert delete_response.status_code == 204,(
            "Ошибка при удалении задачи"
        )

    with allure.step("Проверка, что задача удалена"):
        check_response = auth_session.get(f"{BASE_URL}/v2/task/{task_id}")
        assert check_response.status_code == 404, "Задача не была удалена"
    
    
@allure.title("Фикстура создания задачи")
@pytest.fixture
def task_fixture_only_create(auth_session, post_data):
    with allure.step("Создание задачи через API"):
        create_response = auth_session.post(
            f"{BASE_URL}{CREATE_TASK_URL}",
            json=post_data
            )
        assert create_response.status_code == 200,(
            "Ошибка при создании задачи")
        task = create_response.json()
        task_id = task["id"]

        yield task

@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()
