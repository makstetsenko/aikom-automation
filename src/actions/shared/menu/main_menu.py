import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)


def go_to_available_service(page: Page):
    logger.info("Go to 'Доступні послуги'")
    page.get_by_role("link", name="Доступні послуги", exact=True).click()
    shared_actions.wait_network_idle(page)


def go_to_information_about_staff(page: Page):
    logger.info("Go to 'Інформація про працівників'")
    page.get_by_text("Інформація про працівників").click()
    shared_actions.wait_network_idle(page)


def go_to_information_about_students(page: Page):
    logger.info("Go to 'Інформація про здобувачів освіти'")
    page.get_by_text("Інформація про здобувачів освіти").click()
    shared_actions.wait_network_idle(page)
