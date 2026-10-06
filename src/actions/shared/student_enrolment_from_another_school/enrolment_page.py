from dataclasses import dataclass
import datetime
from enum import StrEnum

from playwright.sync_api import Page

from src.actions.shared import shared_actions

import logging

from src.constants import DATE_FORMAT
from src.domain.aikom_enums import DocumentType, RelationshipToStudentType, StudyingForm

logger = logging.getLogger(__name__)


def fill_parent_name(parent_name: str, page: Page):
    page.get_by_role(
        "textbox", name="Прізвище, ім’я, по батькові (за наявності) заявника чи одного з батьків дитини *"
    ).fill(parent_name.strip())


def select_relationship_to_student(relationship: RelationshipToStudentType, page: Page):
    page.get_by_role("textbox", name="Тип відносин з дитиною *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option", name=relationship.value).click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def fill_parent_phone_number(phone_number: str, page: Page):
    page.get_by_role("textbox", name="Контактний телефон *").fill(phone_number.strip())


def fill_order_number(order_number: str, page: Page):
    page.get_by_role("textbox", name="Номер наказу *").fill(order_number)


def fill_order_date(order_date: datetime.date, page: Page):
    page.get_by_role("textbox", name="Дата наказу *").fill(order_date.strftime(DATE_FORMAT))


def fill_application_submission_date(order_date: datetime.date, page: Page):
    page.get_by_role("textbox", name="Дата подання заяви *").fill(order_date.strftime(DATE_FORMAT))


def check_parent_has_identical_document(page: Page):
    page.get_by_role("checkbox", name="Ознака пред'явлення документу, що посвідчує особу *").check()
