import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)


def try_continue_to_service(page: Page):
    logger.info(f"Try continue to services")
    for _ in range(5):
        try:
            continue_to_service_button = page.get_by_role("button", name="Продовжити надання послуги")
            shared_actions.wait_for_visible(continue_to_service_button, timeout=200)
            continue_to_service_button.click()
            return
        except:
            pass


def go_to_student_withdrawal_during_year(page: Page):
    logger.info("Go to 'Відрахування протягом року'")
    page.get_by_text("Відрахування протягом року").click()
    shared_actions.wait_network_idle(page)


def go_to_student_update_page(page: Page):
    logger.info("Go to 'Оновлення освітнього профілю дитини'")
    page.get_by_text("Оновлення освітнього профілю дитини").click()
    shared_actions.wait_network_idle(page)

    try_continue_to_service(page)


def go_to_create_student_profile_page(page: Page):
    logger.info("Go to 'Створення освітнього профілю дитини'")
    page.locator("p", has_text="Cтворення освітнього профілю дитини").locator("..").click()
    shared_actions.wait_network_idle(page)

    try_continue_to_service(page)


def go_to_student_enrollment_from_another_school_page(page: Page):
    link_name = "Переведення учня між школами протягом року"

    logger.info(f"Go to '{link_name}'")
    page.get_by_text(link_name).click()

    shared_actions.wait_network_idle(page)

    try_continue_to_service(page)


def go_to_student_enrollment_page(page: Page):
    link_name = "Зарахування учня (учень не має звʼязку зі школою)"

    logger.info(f"Go to '{link_name}'")
    page.get_by_text(link_name).click()

    shared_actions.wait_network_idle(page)

    try_continue_to_service(page)


def go_to_student_student_transfer_between_years(page: Page):
    link_name = "Переведення учнів між класами та роками навчання"

    logger.info(f"Go to '{link_name}'")
    page.get_by_text(link_name).click()

    shared_actions.wait_network_idle(page)

    try_continue_to_service(page)
