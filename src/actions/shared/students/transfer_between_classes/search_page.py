import logging
import re

from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.domain.aikom_enums import StudentTransferOrderType, StudyingForm

logger = logging.getLogger(__name__)


def wait(page: Page):
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 500)


def select_transfer_type(transfer_type: StudentTransferOrderType, page: Page):
    logger.info(f"Selecting transfer type {transfer_type.value}")

    page.get_by_role("textbox", name="Тип наказу *").click()
    wait(page)

    page.get_by_role("option", name=transfer_type.value).click()
    wait(page)


def select_from_academic_year_and_studying_form(academic_year: str, studying_form: StudyingForm, page: Page):
    logger.info(f"Selecting from academic year and studying form {academic_year} {studying_form.value}")

    for _ in range(5):
        try:
            page.get_by_role("textbox", name="Pік та форма *").first.click()
            wait(page)

            option = page.get_by_role(
                "option", name=re.compile(rf"^{re.escape(academic_year)}.+{re.escape(studying_form.value)}")
            )
            shared_actions.wait_for_visible(option, timeout=250)
            option.click()

            return
        except:
            pass


def select_from_class_year(class_year: int, page: Page):
    logger.info(f"Selecting from class year {class_year}")

    page.get_by_role("textbox", name="Паралель *").first.click()

    wait(page)

    page.get_by_role("option", name=re.compile(rf"^{re.escape(str(class_year))}\s+.+")).click()

    wait(page)


def select_from_class(class_name: str, page: Page):
    logger.info(f"Selecting from class name {class_name}")

    page.get_by_role("textbox", name="Клас *").first.click()

    wait(page)

    page.get_by_role("option", name=re.compile(fr"^{re.escape(class_name)}")).click()

    wait(page)


def select_to_academic_year_and_studying_form(academic_year: str, studying_form: StudyingForm, page: Page):
    logger.info(f"Selecting to academic year and studying form {academic_year} {studying_form.value}")

    page.get_by_role("textbox", name="Pік та форма *").last.click()

    wait(page)

    page.get_by_role(
        "option", name=re.compile(rf"^{re.escape(academic_year)}.+{re.escape(studying_form.value)}")
    ).click()

    wait(page)


def select_to_class_year(class_year: int, page: Page):
    logger.info(f"Selecting to class year {class_year}")

    page.get_by_role("textbox", name="Паралель *").last.click()

    wait(page)

    page.get_by_role("option", name=re.compile(rf"^{re.escape(str(class_year))}$")).click()

    wait(page)


def select_to_class(class_name: str, page: Page):
    logger.info(f"Selecting to class name {class_name}")

    page.get_by_role("textbox", name="Клас *").last.click()

    wait(page)

    page.get_by_role("option", name=re.compile(rf"^{re.escape(class_name)}.+")).click()

    wait(page)
