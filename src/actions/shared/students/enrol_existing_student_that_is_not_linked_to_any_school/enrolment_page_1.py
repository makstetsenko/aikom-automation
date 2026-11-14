from dataclasses import dataclass
import datetime
from enum import StrEnum
import re

from playwright.sync_api import Page

from src.actions.shared import shared_actions

import logging

from src.constants import DATE_FORMAT
from src.domain.aikom_enums import DocumentType, RelationshipToStudentType, StudyingForm

logger = logging.getLogger(__name__)


def select_first_available_school(page: Page):
    logger.info(f"Selecting first available school")

    page.get_by_role("textbox", name="Назва ЗЗСО для зарахування *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option").nth(0).click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def select_academic_year(academic_year: str, studying_form: StudyingForm, page: Page):
    logger.info(f"Selecting academic year")

    page.get_by_role("textbox", name="Навчальний рік та форма навчання (інституційна) *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option", name=f"{academic_year} {studying_form.value}").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)



def select_class_year(class_year: int, page: Page):
    logger.info(f"Selecting class year")

    page.get_by_role("textbox", name="Паралель *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option", name=re.compile(rf"^{re.escape(str(class_year))}$")).click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)



def select_class_name(class_name: str, page: Page):
    logger.info(f"Selecting class name")

    page.get_by_role("textbox", name="Клас *").click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)

    page.get_by_role("option", name=re.compile(rf"^{re.escape(str(class_name))}.+")).click()

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def fill_order_number(order_number: str, page: Page):
    logger.info(f"Filling order number")
    page.get_by_role("textbox", name="Номер наказу *").fill(order_number)


def fill_order_date(order_date: datetime.date, page: Page):
    logger.info(f"Filling order date")
    page.get_by_role("textbox", name="Дата наказу").fill(order_date.strftime(DATE_FORMAT))







