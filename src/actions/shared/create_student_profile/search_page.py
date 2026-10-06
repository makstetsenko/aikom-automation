from dataclasses import dataclass
import datetime
from enum import StrEnum

from playwright.sync_api import Page

from src.actions.shared import shared_actions

import logging

from src.constants import DATE_FORMAT
from src.domain.aikom_enums import DocumentType

logger = logging.getLogger(__name__)


@dataclass
class SearchStudentResult:
    birth_certificate_serial: str
    birth_certificate_number: str
    school_name: str


def select_document_type(document_type: DocumentType, page: Page):
    logger.info(f"Selecting document type")

    page.get_by_role("textbox", name="Тип документу, що посвідчує особу дитини *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option", name=document_type.value).click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def fill_birth_certificate_serial(serial: str, page: Page):
    logger.info(f"Filling birth certificate serial")

    page.get_by_role("textbox", name="Серія свідоцтва про народження дитини *").fill(serial)

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def fill_birth_certificate_number(number: str, page: Page):
    logger.info(f"Filling birth certificate number")

    page.get_by_role("textbox", name="Номер свідоцтва про народження дитини *").fill(number)

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def fill_birth_date(birth_date: datetime.date, page: Page):
    logger.info(f"Filling birth date")

    page.get_by_role("textbox", name="Дата народження *").fill(birth_date.strftime(DATE_FORMAT))

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def try_get_student_search_result(page: Page) -> SearchStudentResult | None:
    try:
        found_profiles_header = page.get_by_text("Профілі дитини, які знайдені в реєстрі")
        shared_actions.wait_for_visible(found_profiles_header, 1000)

        birth_certificate = page.locator("table tbody tr").first.locator("td").nth(1).inner_text().strip().split()
        school_name = page.locator("table tbody tr").first.locator("td").nth(3).inner_text().strip()

        return SearchStudentResult(
            birth_certificate_serial=birth_certificate[0],
            birth_certificate_number=birth_certificate[1],
            school_name=school_name,
        )
    except:
        return None


def is_student_missing(page: Page):
    heading = page.get_by_role("heading", name="По введеним даним дитина не була знайдена в ДРАЦС")
    return heading.count() > 0
