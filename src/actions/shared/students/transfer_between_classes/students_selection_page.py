from dataclasses import dataclass
import datetime
import logging
import re

from playwright.sync_api import Locator, Page

from src.actions.shared import shared_actions
from src.constants import DATE_FORMAT

logger = logging.getLogger(__name__)


def get_first_page_btn(page: Page):
    return page.get_by_role("button", name="Перша сторінка")


def get_last_page_btn(page: Page):
    return page.get_by_role("button", name="Остання сторінка")


def get_next_page_btn(page: Page):
    return page.get_by_role("button", name="Наступна сторінка")


def get_previous_page_btn(page: Page):
    return page.get_by_role("button", name="Попередня сторінка")



def check_student(search_name: str, search_surname: str, page: Page):
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 1000)

    first_page_btn = get_first_page_btn(page)
    if first_page_btn.is_enabled():
        first_page_btn.click()
        shared_actions.wait(page, 250)

    while True:
        rows = page.locator("table tbody tr").all()
        for r in rows:
            cols = r.locator("td")

            checkbox = r.get_by_role("checkbox")
            student_name = cols.nth(3).inner_text().strip()
            student_surname = cols.nth(2).inner_text().strip()

            if search_name.lower() == student_name.lower() and search_surname.lower() == student_surname.lower():
                logger.info(f"Selected student {student_name} {student_surname}")
                checkbox.check()
                shared_actions.wait(page, 250)
                return

        next_page_btn = get_next_page_btn(page)

        if next_page_btn.is_disabled():
            break

        next_page_btn.click()
        shared_actions.wait(page, 250)

    logger.warning(f"Student {search_name} {search_surname} was not found for selection")


def fill_order_date(order_date: datetime.date, page: Page):
    page.get_by_role("textbox", name="Дата наказу *").fill(order_date.strftime(DATE_FORMAT))
    shared_actions.click_on_html_body(page)
    shared_actions.wait(page, 250)


def fill_order_number(order_number: str, page: Page):
    page.get_by_role("textbox", name="Номер наказу *").fill(order_number)
    shared_actions.wait(page, 250)


def fill_enrolment_date(enrolment_date: datetime.date, page: Page):
    page.get_by_role("textbox", name="Дата зарахування *").fill(enrolment_date.strftime(DATE_FORMAT))
    shared_actions.click_on_html_body(page)
    shared_actions.wait(page, 250)
