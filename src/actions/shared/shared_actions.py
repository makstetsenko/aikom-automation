from playwright.sync_api import Locator, Page, expect

from src.app_settings import get_app_settings


def wait_network_idle(page: Page):
    page.wait_for_load_state("networkidle")


def wait_for_visible_and_stable(locator: Locator):
    locator.wait_for(state="visible")
    element = locator.element_handle()
    if element:
        element.wait_for_element_state("stable")


def wait_for_visible(locator: Locator):
    locator.wait_for(state="visible")


def wait_for_element_attached(locator: Locator):
    expect(locator).to_be_attached()


# useful when there is a need to click somewhere to loose focus from some elements
def click_on_html_body(page: Page):
    page.locator("body").click()


def fill_auth_key_iframe_and_sign(page: Page):
    page.wait_for_timeout(5_000)

    iframe = page.locator("#sign-widget")
    wait_for_visible_and_stable(iframe)

    sign_widget = iframe.content_frame

    read_file_input = sign_widget.locator("#pkReadFileInput")
    wait_for_element_attached(read_file_input)

    app_settings = get_app_settings()

    read_file_input.set_input_files(app_settings.auth_key_path.as_posix())

    file_pass_input = sign_widget.locator("#pkReadFilePasswordTextField")
    wait_for_visible(file_pass_input)
    file_pass_input.fill(app_settings.auth_key_password)

    read_file_button = sign_widget.locator("#pkReadFileButton")
    wait_for_visible(read_file_button)
    read_file_button.click()

    sign_data_button = page.get_by_role("button", name="Підписати дані", exact=True)
    wait_for_visible_and_stable(sign_data_button)
    sign_data_button.click()
    wait_network_idle(page)
