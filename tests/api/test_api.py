import allure
import pytest
from tests.config import LIST_ID, BASE_URL


@allure.feature("Тестирование тасков в ClickUp")
class TestPosts:

    @allure.description(
        "Создание новой задачи с базовыми параметрами и проверка полей"
    )
    def test_create_task_success(self, post_data, task_fixture):
        with allure.step("Получение данных из task_fixture"):
            response_data = task_fixture

        with allure.step("Проверка наличия ID в ответе"):
            assert "id" in response_data, "В ответе отсутствует ID задачи"

        with allure.step("Проверка совпадения имени задачи"):
            assert response_data["name"] == post_data["name"], (
                f"Имя задачи не совпадает: ожидалось {post_data['name']}, "
                f"получено {response_data['name']}"
            )

        if "description" in post_data:
            with allure.step("Проверка совпадения описания задачи"):
                assert response_data["description"] == post_data[
                    "description"
                    ], ("Описание задачи не совпадает")

        if "status" in post_data:
            with allure.step("Проверка совпадения статуса задачи"):
                assert response_data["status"]["status"] == post_data["status"], (
                    "Статус задачи не совпадает"
                )

        with allure.step("Проверка совпадения ID списка"):
            assert int(response_data["list"]["id"]) == LIST_ID, (
                f"ID списка не совпадает: ожидалось {LIST_ID}, "
                f"получено {response_data['list']['id']}"
            )

        with allure.step("Проверка URL задачи"):
            assert "url" in response_data and response_data["url"].startswith(
                "https://app.clickup.com/t/"
            ), "URL задачи некорректный или отсутствует"
    
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
        self, auth_session, invalid_data, request
    ):
        # Устанавливаем заголовок для каждого параметра в Allure
        allure.dynamic.title(
            f"Невалидный POST: {request.node.callspec.id}"
        )

        with allure.step("Отправка запроса с невалидными данными"):
            response = auth_session.post(
                f"{BASE_URL}/v2/list/{LIST_ID}/task",
                json=invalid_data
            )

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
    def test_get_task_success(self, auth_session, task_fixture):
        with allure.step("Получение ID задачи из фикстуры"):
            task_id = task_fixture["id"]
        with allure.step("Получение таска через GET"):
            get_response = auth_session.get(
                f"{BASE_URL}/v2/task/{task_id}"
                )
            assert get_response.status_code == 200, (
                "Ошибка при получении таска"
                )

        with allure.step("Проверка совпадения ID и имени таска"):
            task_data = get_response.json()
            assert task_data["id"] == task_id, "ID задачи не совпадает"
            assert task_data["name"] == task_fixture["name"], (
                "Имя таска не совпадает"
                )
            assert task_data["description"] == task_fixture["description"], (
                "Описание таска не совпадает"
                )
            assert task_data["status"] == task_fixture["status"], (
                    "Статус таска не совпадает"
                )
    
    @allure.description(
        "Попытка получения несуществующего таска и проверка полей ответа"
    )
    def test_get_task_not_found(self, auth_session):
        with allure.step("Задание несуществующего ID задачи"):
            task_id = "wrong_id"

        with allure.step("Попытка получить задачу с несуществующим ID"):
            get_response = auth_session.get(
                f"{BASE_URL}/v2/task/{task_id}"
            )
            assert get_response.status_code == 401, (
                "Ошибка при получении задачи"
            )

        with allure.step("Проверка наличия ключей err и ECODE"):
            response_json = get_response.json()
            assert "err" in response_json, "Нет ключа err в ответе"
            assert "ECODE" in response_json, "Нет ключа ECODE в ответе"

    @allure.description(
        "Обновление существующей задачи и проверка обновлённых полей"
    )
    def test_update_task_success(
        self, auth_session, task_fixture, updated_data
    ):
        with allure.step("Получение ID задачи для обновления"):
            task_id = task_fixture["id"]

        with allure.step("Отправка PUT-запроса для обновления задачи"):
            update_response = auth_session.put(
                f"{BASE_URL}/v2/task/{task_id}",
                json=updated_data
            )
            assert update_response.status_code == 200, (
                "Задача не обновилась"
            )

        with allure.step("Проверка обновлённых данных задачи"):
            updated_task = update_response.json()
            assert updated_task["id"] == task_id, (
                "ID задачи не совпадает"
            )
            assert updated_task["name"] == updated_data["name"], (
                "Имя задачи не обновилось"
            )
            assert updated_task["description"] == updated_data["description"], (
                "Описание не обновилось"
            )
            assert updated_task["status"]["status"] == updated_data["status"], (
                "Статус задачи не обновился"
            )
    
    @allure.description(
        "Попытка обновления задачи с несуществующим ID"
    )
    def test_update_task_not_found(self, auth_session, updated_data):
        with allure.step("Задание несуществующего ID"):
            fake_task_id = "nonexistent_task_id"

        with allure.step("Попытка обновить задачу с несуществующим ID"):
            response = auth_session.put(
                f"{BASE_URL}/v2/task/{fake_task_id}",
                json=updated_data
            )
            assert response.status_code == 404 or response.status_code == 401, (
                f"Ожидался статус 404 или 401, получен {response.status_code}"
            )

        with allure.step("Проверка наличия сообщения об ошибке"):
            response_json = response.json()
            assert "err" in response_json, "Нет ключа err в ответе"
            assert "ECODE" in response_json, "Нет ключа ECODE в ответе"

    @allure.description(
        "Попытка обновления задачи с некорректными данными"
    )
    def test_update_task_invalid_data(
        self, auth_session, task_fixture, invalid_data
    ):
        with allure.step("Получение ID задачи"):
            task_id = task_fixture["id"]

        with allure.step("Попытка обновления задачи с невалидными полями"):
            response = auth_session.put(
                f"{BASE_URL}/v2/task/{task_id}",
                json=invalid_data
            )
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}"
            )

        with allure.step("Проверка сообщения об ошибке"):
            response_json = response.json()
            assert "err" in response_json or "message" in response_json, (
                "Нет сообщения об ошибке в ответе"
            )
    
    @allure.description(
        "Удаление задачи с корректными данными"
    )
    def test_delete_task_success(self,
                                 auth_session,
                                 task_fixture_only_create):
        
        task_id = task_fixture_only_create["id"]

        with allure.step("Удаление задачи"):
            response = auth_session.delete(f"{BASE_URL}/v2/task/{task_id}")
            
        with allure.step("Проверка кода ответа на удаление"):
            assert response.status_code == 204, (
                "Ожидался статус 204 при успешном удалении"
                )
        
        with allure.step("Проверка отсутствия текста в ответе"):
            assert response.text == "", "Ожидается пустое тело ответа"

        with allure.step("Проверка, что задача действительно удалена"):
            check = auth_session.get(f"{BASE_URL}/v2/task/{task_id}")
            assert check.status_code == 404, "Ожидался статус 404 для удалённой задачи"
    
    @allure.description(
        "Удаление задачи с корректными данными"
    )
    def test_delete_task_fail(self, auth_session):
        
        wrong_id = 'qwejgfskip3'

        with allure.step("Удаление задачи"):
            response = auth_session.delete(f"{BASE_URL}/v2/task/{wrong_id}")
            
        with allure.step("Проверка кода ответа на удаление"):
            assert response.status_code == 401, (
                "Ожидался статус 401 при файле удаления"
                )
