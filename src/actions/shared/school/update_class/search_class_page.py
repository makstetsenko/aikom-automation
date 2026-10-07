from enum import StrEnum
import re

from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.domain.aikom_enums import StudyingForm


def select_academic_year(academic_year: str, page: Page):
    page.get_by_role("textbox", name="Навчальний рік *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=academic_year)
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)


def select_studying_form(studying_form: StudyingForm, page: Page):
    page.get_by_role("textbox", name="Форма навчання *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=studying_form)
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)


def select_class_year(class_year: int, page: Page):
    page.get_by_role("textbox", name="Паралель *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=str(class_year), exact=True)
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)


def select_class_name(class_name: str, page: Page):
    page.get_by_role("textbox", name="Назва класу *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=re.compile(rf"^{re.escape(class_name)}"))
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)
