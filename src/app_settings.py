import pathlib
import os

from dotenv import load_dotenv
from pydantic import BaseModel


class AppSettings(BaseModel):
    auth_key_path: pathlib.Path
    auth_key_password: str


class AppSettingsStore(BaseModel):
    app_settings: AppSettings | None


APP_SETTINGS_STORE = AppSettingsStore(app_settings=None)


def get_auth_key() -> pathlib.Path:
    auth_key_path_env_value = os.getenv("AUTH_KEY_PATH")

    if auth_key_path_env_value is None or auth_key_path_env_value == "":
        raise ValueError("AUTH_KEY_PATH is required")

    auth_key_path = pathlib.Path(auth_key_path_env_value).resolve()

    print(auth_key_path.as_posix())

    if not auth_key_path.is_file():
        raise ValueError("AUTH_KEY_PATH is not a file")

    return auth_key_path


def get_auth_password() -> str:
    env_value = os.getenv("AUTH_KEY_PASSWORD")

    if env_value is None or env_value == "":
        raise ValueError("AUTH_KEY_PASSWORD is required")

    return env_value


def get_app_settings() -> AppSettings:
    global APP_SETTINGS_STORE

    if APP_SETTINGS_STORE is None:
        APP_SETTINGS_STORE = AppSettingsStore(app_settings=None)

    if APP_SETTINGS_STORE.app_settings is not None:
        return APP_SETTINGS_STORE.app_settings

    load_dotenv()

    settings = AppSettings(auth_key_path=get_auth_key(), auth_key_password=get_auth_password())

    APP_SETTINGS_STORE.app_settings = settings

    return settings
