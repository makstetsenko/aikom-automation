from dataclasses import dataclass
import datetime
from enum import StrEnum

from playwright.sync_api import Page

from src.actions.shared import shared_actions

import logging

from src.constants import DATE_FORMAT
from src.domain.aikom_enums import DocumentType, StudyingForm

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

