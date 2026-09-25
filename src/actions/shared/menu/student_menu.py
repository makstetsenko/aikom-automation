import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)


def go_to_student_withdrawal_during_year(page: Page):
    logger.info("Go to 'Відрахування протягом року'")
    page.get_by_text("Відрахування протягом року").click()
    shared_actions.wait_network_idle(page)
