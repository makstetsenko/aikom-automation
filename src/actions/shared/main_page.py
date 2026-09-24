from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.app_settings import get_app_settings

AIKOM_URL = "https://cabinet.aikom.gov.ua"


def wait_for_welcome_header(page: Page):
    welcome_heading = page.get_by_role("heading", name="Вітаємо!")
    shared_actions.wait_for_visible_and_stable(welcome_heading)
    shared_actions.wait_network_idle(page)


def try_auth(page: Page):
    shared_actions.wait_network_idle(page)
    auth_button = page.get_by_role("button", name="Увійти до кабінету")

    if auth_button.count() == 0:
        wait_for_welcome_header(page)
        return

    shared_actions.wait_network_idle(page)
    shared_actions.wait_for_visible_and_stable(auth_button)

    auth_button.click()
    shared_actions.wait_network_idle(page)

    app_settings = get_app_settings()

    select_file_storage_button = page.get_by_role("link", name="Файловий носій")
    shared_actions.wait_for_visible_and_stable(select_file_storage_button)

    select_file_storage_button.click()
    shared_actions.wait_network_idle(page)

    file_input = page.locator("#PKeyFileInput")
    shared_actions.wait_for_element_exist(file_input)

    file_input.set_input_files(app_settings.auth_key_path.absolute().as_posix())

    password_input = page.get_by_role("textbox", name="Пароль")
    shared_actions.wait_for_visible_and_stable(password_input)

    password_input.fill(app_settings.auth_key_password)

    submit_auth_key_button = page.get_by_role("button", name="Продовжити")
    shared_actions.wait_for_visible_and_stable(submit_auth_key_button)

    submit_auth_key_button.click()
    shared_actions.wait_network_idle(page)

    continue_to_main_button = page.get_by_role("button", name="Продовжити")
    shared_actions.wait_for_visible_and_stable(continue_to_main_button)

    continue_to_main_button.click()
    shared_actions.wait_network_idle(page)

    wait_for_welcome_header(page)


def go_to_main_page(page: Page) -> None:
    page.goto(AIKOM_URL)
    try_auth(page)
