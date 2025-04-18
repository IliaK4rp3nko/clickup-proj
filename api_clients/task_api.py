import allure
import requests


class ClickUpClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
            'Content-Type': 'application/json'
        })

    @allure.step("Получение team_id через API")
    def get_team_id(self):
        response = self.session.get(f"{self.base_url}/v2/team")
        response_json = response.json()
        try:
            team_id = response_json["teams"][0]["id"]
            return team_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить team_id из ответа API") from e

    @allure.step("Получение folder_id через API")
    def get_folder_id(self):
        team_id = self.get_team_id()
        response = self.session.get(f"{self.base_url}/v2/team/{team_id}/folder")
        response_json = response.json()
        try:
            folder_id = response_json["folders"][0]["id"]
            return folder_id
        except (KeyError, IndexError) as e:
            raise ValueError("Не удалось получить folder_id из ответа API") from e

    @allure.step("Получение list_id через API")
    def get_list_id(self):
        folder_id = self.get_folder_id()
        response = self.session.get(f"{self.base_url}/v2/folder/{folder_id}/list")
        response_json = response.json()
        try:
            list_id = response_json["lists"][0]["id"]
            return list_id
        except (KeyError, IndexError)as e:
            raise ValueError("Не удалось получить list_id из ответа API") from e


    @allure.step("Создание задачи через API")
    def create_task(self, list_id, task_data):
        return self.session.post(
            f"{self.base_url}/v2/list/{list_id}/task",
            json=task_data
        )

    @allure.step("Удаление задачи через API")
    def delete_task(self, task_id):
        return self.session.delete(
            f"{self.base_url}/v2/task/{task_id}"
        )

    @allure.step("Получение задачи через API")
    def get_task(self, task_id):
        return self.session.get(
            f"{self.base_url}/v2/task/{task_id}"
        )

    @allure.step("Обновление задачи через API")
    def update_task(self, task_id, updated_data):
        return self.session.put(
            f"{self.base_url}/v2/task/{task_id}",
            json=updated_data
        )

    @allure.step("Проверка существования задачи")
    def check_task_exists(self, task_id):
        return self.session.get(
            f"{self.base_url}/v2/task/{task_id}"
        )

    @allure.step("Получение списка тасков через API")
    def get_task_list(self, list_id):
        return self.session.get(
            f"{self.base_url}/v2/list/{list_id}/task"
        )

    @allure.step("Получение id таска по названию через API")
    def get_task_id_by_name(self, response, task_name):
        get_response = response.json()
        if "tasks" in get_response:
            for task in get_response["tasks"]:
                if task["name"] == task_name:
                    return task["id"]
        return None
