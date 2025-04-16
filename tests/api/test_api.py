import allure
import pytest
from tests.config import LIST_ID

@allure.feature("Тестирование тасков в ClickUp")
class TestPosts:

    @allure.title("Создание и удаление задачи без использования фикстур")
    @allure.description("Создание новой задачи, проверка полей, удаление и проверка удаления")
    def test_create_and_delete_task(self, clickup_client, post_data):

        with allure.step("Создание задачи через API"):
            create_response = clickup_client.create_task(LIST_ID, post_data)
            assert create_response.status_code == 200, "Ошибка при создании задачи"
            task = create_response.json()
            task_id = task["id"]


        with allure.step("Проверка наличия ID в ответе"):
            assert "id" in task, "В ответе отсутствует ID задачи"

        with allure.step("Проверка совпадения имени задачи"):
            assert task["name"] == post_data["name"], (
                f"Имя задачи не совпадает: ожидалось {post_data['name']}, "
                f"получено {task['name']}"
            )

        if "description" in post_data:
            with allure.step("Проверка совпадения описания задачи"):
                assert task["description"] == post_data["description"], (
                    "Описание задачи не совпадает"
                )

        if "status" in post_data:
            with allure.step("Проверка совпадения статуса задачи"):
                assert task["status"]["status"] == post_data["status"], (
                    "Статус задачи не совпадает"
                )

        with allure.step("Проверка совпадения ID списка"):
            assert int(task["list"]["id"]) == LIST_ID, (
                f"ID списка не совпадает: ожидалось {LIST_ID}, "
                f"получено {task['list']['id']}"
            )

        with allure.step("Проверка URL задачи"):
            assert "url" in task and task["url"].startswith(
                "https://app.clickup.com/t/"), (
                "URL задачи некорректный или отсутствует"
            )

        with allure.step("Удаление созданной задачи"):
            delete_response = clickup_client.delete_task(task_id)
            assert delete_response.status_code == 204, "Ошибка при удалении задачи"

        with allure.step("Проверка, что задача удалена"):
            check_response = clickup_client.check_task_exists(task_id)
            assert check_response.status_code == 404, "Задача не была удалена"

    @allure.label("layer", "api")
    @allure.tag("негативный", "создание_задачи")
    @allure.description(
        "Проверка невозможности создать задачу с невалидными параметрами"
    )
    @pytest.mark.parametrize(
        "invalid_data",
        [
            pytest.param(
                {
                    "name": "",
                    "description": "Valid desc",
                    "status": "to do"
                },
                id="Пустое имя задачи"
            ),
            pytest.param(
                {
                    "name": "Task",
                    "description": "desc",
                    "status": "not_a_status"
                },
                id="Несуществующий статус"
            ),
            pytest.param(
                {},
                id="Пустое тело запроса"
            ),
        ]
    )
    def test_create_task_invalid_data_parametrized(
        self, clickup_client, invalid_data, request
    ):
        allure.dynamic.title(
            f"Невалидный POST: {request.node.callspec.id}"
        )

        with allure.step("Отправка запроса с невалидными данными"):
            response = clickup_client.create_task(LIST_ID, invalid_data)

        with allure.step("Проверка кода ответа (400 или 422)"):
            assert response.status_code in [400, 422], (
                f"Ожидался статус 400 или 422, "
                f"получен {response.status_code}"
            )

        with allure.step("Проверка наличия сообщения об ошибке"):
            try:
                response_json = response.json()
                assert "err" in response_json or "message" in response_json, (
                    "Нет сообщения об ошибке в теле ответа"
                )
            except Exception:
                pytest.fail("Ошибка при декодировании JSON-ответа")

    @allure.description("Получение таска и проверка полей ответа")
    def test_get_task_success(self, clickup_client, task_fixture):
        with allure.step("Получение ID задачи из фикстуры"):
            task_id = task_fixture["id"]
        
        with allure.step("Получение таска через GET"):
            get_response = clickup_client.get_task(task_id)
            assert get_response.status_code == 200, "Ошибка при получении таска"

        with allure.step("Проверка совпадения данных"):
            task_data = get_response.json()
            assert task_data["id"] == task_id, "ID задачи не совпадает"
            assert task_data["name"] == task_fixture["name"], "Имя не совпадает"
            assert task_data["description"] == task_fixture["description"], "Описание не совпадает"
            assert task_data["status"]["status"] == task_fixture["status"]["status"], "Статус не совпадает"
    
    @allure.description("Попытка получения несуществующего таска")
    def test_get_task_not_found(self, clickup_client):
        with allure.step("Использование невалидного ID"):
            response = clickup_client.get_task("wrong_id")
            assert response.status_code == 401, "Ожидалась ошибка авторизации"

        with allure.step("Проверка структуры ошибки"):
            response_json = response.json()
            assert "err" in response_json, "Нет ключа err в ответе"
            assert "ECODE" in response_json, "Нет ключа ECODE в ответе"

    @allure.description("Обновление существующей задачи")
    def test_update_task_success(self, clickup_client, task_fixture, updated_data):
        task_id = task_fixture["id"]
        
        with allure.step("Отправка PUT-запроса"):
            update_response = clickup_client.update_task(task_id, updated_data)
            assert update_response.status_code == 200, "Ошибка обновления"

        with allure.step("Проверка обновлённых данных"):
            updated_task = update_response.json()
            assert updated_task["name"] == updated_data["name"], "Имя не обновилось"
            assert updated_task["description"] == updated_data["description"], "Описание не обновилось"
            assert updated_task["status"]["status"] == updated_data["status"], "Статус не обновился"
    
    @allure.description("Попытка обновления несуществующей задачи")
    def test_update_task_not_found(self, clickup_client, updated_data):
        with allure.step("Использование несуществующего ID"):
            response = clickup_client.update_task("nonexistent_id", updated_data)
            assert response.status_code in [401, 404], "Неверный статус код"

        with allure.step("Проверка структуры ошибки"):
            response_json = response.json()
            assert "err" in response_json, "Нет ключа err в ответе"
            assert "ECODE" in response_json, "Нет ключа ECODE в ответе"

    @allure.description("Попытка обновления с невалидными данными")
    def test_update_task_invalid_data(self, clickup_client, task_fixture, invalid_data):
        task_id = task_fixture["id"]
        
        with allure.step("Отправка невалидных данных"):
            response = clickup_client.update_task(task_id, invalid_data)
            assert response.status_code == 400, "Ожидалась ошибка валидации"

        with allure.step("Проверка сообщения об ошибке"):
            response_json = response.json()
            assert "err" in response_json or "message" in response_json, "Нет сообщения об ошибке"
    
    @allure.description("Удаление задачи")
    def test_delete_task_success(self, clickup_client, task_fixture_only_create):
        task_id = task_fixture_only_create["id"]
        
        with allure.step("Удаление задачи"):
            response = clickup_client.delete_task(task_id)
            assert response.status_code == 204, "Ошибка удаления"
            assert response.text == "", "Тело ответа не пустое"

        with allure.step("Проверка отсутствия задачи"):
            check_response = clickup_client.check_task_exists(task_id)
            assert check_response.status_code == 404, "Задача не удалена"
    
    @allure.description("Попытка удаления несуществующей задачи")
    def test_delete_task_fail(self, clickup_client):
        with allure.step("Использование невалидного ID"):
            response = clickup_client.delete_task("invalid_task_id")
            assert response.status_code == 401, "Неверный статус код"