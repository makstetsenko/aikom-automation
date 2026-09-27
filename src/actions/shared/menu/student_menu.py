import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)


def go_to_student_withdrawal_during_year(page: Page):
    logger.info("Go to 'Відрахування протягом року'")
    page.get_by_text("Відрахування протягом року").click()
    shared_actions.wait_network_idle(page)


def go_to_student_update_page(page: Page):
    logger.info("Go to 'Оновлення освітнього профілю дитини'")
    page.get_by_text("Оновлення освітнього профілю дитини").click()
    shared_actions.wait_network_idle(page)

    continue_to_service_button = page.get_by_role("button", name="Продовжити надання послуги")

    try:
        shared_actions.wait_for_visible(continue_to_service_button, timeout=2000)
        continue_to_service_button.click()
    except:
        return
