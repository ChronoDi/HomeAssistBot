from homeassistant_api import Client
from tg_bot.config_data import config

def get_client() -> Client:
    url = config.home_assist.url
    token = config.home_assist.token

    return Client(url, token)