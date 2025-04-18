from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY

BASE_URL = 'https://api.clickup.com/api'
BASE_URL_FRONT = 'https://app.clickup.com/'
client = ClickUpClient(BASE_URL, CLICKUP_API_KEY)
FOLDER_ID = '2kypqw7y-335'
WORKSPACE_ID = client.get_team_id()
