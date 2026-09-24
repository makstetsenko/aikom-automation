from playwright.sync_api import Page

from src.actions.shared import shared_actions


def go_to_available_service(page: Page):
    page.get_by_role("link", name="Доступні послуги", exact=True).click()
    shared_actions.wait_network_idle(page)


def go_to_information_about_staff(page: Page):
    page.get_by_text("Інформація про працівників").click()
    shared_actions.wait_network_idle(page)
