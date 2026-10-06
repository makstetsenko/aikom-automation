import logging

from playwright.sync_api import Page, expect

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)


def go_to_update_classes(page: Page):
    link_name = "Оновлення класів"
    logger.info(f"Go to '{link_name}'")
    page.get_by_text(link_name).click()
    shared_actions.wait_network_idle(page)
