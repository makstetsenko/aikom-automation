from playwright.sync_api import Locator, Page

from src.actions.shared import shared_actions


def get_modal(page: Page):
    return page.get_by_text("Внести дані").locator("..")


def select_country(country_name: str, modal: Locator):
    textbox = modal.get_by_role("textbox", name="Назва країни проживання *")
    textbox.click()
    shared_actions.wait_network_idle(modal.page)
    shared_actions.wait(modal.page, 250)

    modal.page.get_by_role("option", name=country_name).click()
    shared_actions.wait_network_idle(modal.page)
    shared_actions.wait(modal.page, 250)


def save(modal: Locator):
    modal.get_by_role("button", name="Зберегти").click()
    shared_actions.wait_network_idle(modal.page)
    shared_actions.wait(modal.page, 250)
