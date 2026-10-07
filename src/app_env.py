import pathlib
import os

from dotenv import load_dotenv
from pydantic import BaseModel


class AppEnv(BaseModel):
    auth_key_path: pathlib.Path
    auth_key_password: str


class AppEnvStore(BaseModel):
    app_env: AppEnv | None


APP_ENV_STORE = AppEnvStore(app_env=None)


def get_auth_key() -> pathlib.Path:
    auth_key_path_env_value = os.getenv("AUTH_KEY_PATH")

    if auth_key_path_env_value is None or auth_key_path_env_value == "":
        raise ValueError("AUTH_KEY_PATH is required")

    auth_key_path = pathlib.Path(auth_key_path_env_value).resolve()

    if not auth_key_path.is_file():
        raise ValueError("AUTH_KEY_PATH is not a file")

    return auth_key_path


def get_auth_password() -> str:
    env_value = os.getenv("AUTH_KEY_PASSWORD")

    if env_value is None or env_value == "":
        raise ValueError("AUTH_KEY_PASSWORD is required")

    return env_value


def get_app_env() -> AppEnv:
    global APP_ENV_STORE

    if APP_ENV_STORE is None:
        APP_ENV_STORE = AppEnvStore(app_env=None)

    if APP_ENV_STORE.app_env is not None:
        return APP_ENV_STORE.app_env

    load_dotenv()

    app_env = AppEnv(auth_key_path=get_auth_key(), auth_key_password=get_auth_password())

    APP_ENV_STORE.app_env = app_env

    return app_env
