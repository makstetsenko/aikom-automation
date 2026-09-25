import datetime
import logging

from playwright.sync_api import Page, expect

from enum import StrEnum

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, student_menu
from src.constants import DATE_FORMAT

logger = logging.getLogger(__name__)


class WithdrawalType(StrEnum):
    MOVING_TO_ANOTHER_SCHOOL = "Перехід до іншого навчального закладу"


class RelationshipToStudentType(StrEnum):
    MOTHER = "Мати"
    FATHER = "Батько"
    GUARDIAN = "Опікун"


def find_student(student_surname: str, student_name: str, page: Page) -> bool:
    logger.info(f"Try find student {student_name} {student_surname}")

    surname_input = page.get_by_role("textbox", name="Прізвище для пошуку *")
    shared_actions.wait_for_visible_and_stable(surname_input)
    surname_input.fill(student_surname)

    name_input = page.get_by_role("textbox", name="Ім'я для пошуку *")
    shared_actions.wait_for_visible_and_stable(name_input)
    name_input.fill(student_name)

    search_button = page.get_by_role("button", name="Знайти")
    shared_actions.wait_for_visible_and_stable(search_button)
    search_button.click()

    shared_actions.wait_network_idle(page)

    missing_student_text = page.get_by_text(
        "Дитину з такими даними не знайдено в Реєстрі. Будь ласка, перевірте введені дані та спробуйте ще раз."
    )

    try:
        expect(missing_student_text).to_be_visible(timeout=2_000)
        return False
    except:
        pass  # student was found -> this text wont appear -> continue flow

    found_data_textbox = page.get_by_role("textbox", name="Знайдені дані")
    shared_actions.wait_for_visible_and_stable(found_data_textbox)
    found_data_textbox.click()

    student_option = page.get_by_role("option", name=f"{student_surname} {student_name}")
    shared_actions.wait_for_visible_and_stable(student_option)
    student_option.click()

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.wait_network_idle(page)

    return True


def select_withdrawal_type(withdrawal_type: WithdrawalType, page: Page):
    logger.info(f"Selecting withdrawal type")

    withdrawal_type_textbox = page.get_by_role("textbox", name="Тип відрахування *")
    shared_actions.wait_for_visible_and_stable(withdrawal_type_textbox)
    withdrawal_type_textbox.click()

    if withdrawal_type == WithdrawalType.MOVING_TO_ANOTHER_SCHOOL:
        withdrawal_option = page.get_by_role("option", name="Відрахування у зв'язку з переведенням до іншого ЗЗСО")

    shared_actions.wait_for_visible_and_stable(withdrawal_option)
    withdrawal_option.click()

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.wait_network_idle(page)


def fill_parent_info(
    parent_full_name: str,
    parent_phone_number: str,
    application_date: datetime.date,
    parent_relationship_to_student: RelationshipToStudentType,
    page: Page,
):

    logger.info(f"Filling parent info")
    parent_full_name_textbox = page.get_by_role("textbox", name="Прізвище, ім’я, по батькові (за наявності) заявника *")
    shared_actions.wait_for_visible_and_stable(parent_full_name_textbox)
    parent_full_name_textbox.fill(parent_full_name)

    relationship_to_student_textbox = page.get_by_role("textbox", name="Тип відносин з дитиною *")
    shared_actions.wait_for_visible_and_stable(relationship_to_student_textbox)
    relationship_to_student_textbox.click()

    if parent_relationship_to_student == RelationshipToStudentType.MOTHER:
        relationship_to_student_option = page.get_by_role("option", name="Мати")
    elif parent_relationship_to_student == RelationshipToStudentType.FATHER:
        relationship_to_student_option = page.get_by_role("option", name="Батько")
    elif parent_relationship_to_student == RelationshipToStudentType.GUARDIAN:
        relationship_to_student_option = page.get_by_role("option", name="Опікун")
    else:
        raise ValueError(f"Unexpected value {parent_relationship_to_student} of enum RelationshipToStudentType")

    shared_actions.wait_for_visible_and_stable(relationship_to_student_option)
    relationship_to_student_option.click()

    parent_phone_number_textbox = page.get_by_role(
        "textbox", name="Контактний телефон заявника *"
    )  # fill("(000) 000-0000_")
    shared_actions.wait_for_visible_and_stable(parent_phone_number_textbox)
    parent_phone_number_textbox.fill(parent_phone_number)

    has_id_document_checkbox = page.get_by_role(
        "checkbox", name="Ознака пред'явлення документу, що посвідчує особу заявника *"
    )
    has_id_document_checkbox.check()

    application_date_textbox = page.get_by_role("textbox", name="Дата подання заяви *")  # fill("01.09.2026_")
    shared_actions.wait_for_visible_and_stable(application_date_textbox)
    application_date_textbox.fill(application_date.strftime(DATE_FORMAT))

    shared_actions.click_on_html_body(page)

    # If need to lost focus on date picker - uncomment this
    # page.get_by_text("Тип заяви Причина подання заяви Прізвище дитини Ім’я дитини По батькові дитини (").click()

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.wait_network_idle(page)


def fill_application_acceptance_info(withdrawal_date: datetime.date, page: Page):
    logger.info(f"Filling application info")
    application_result_textbox = page.get_by_role("textbox", name="Рішення по заяві *")
    shared_actions.wait_for_visible_and_stable(application_result_textbox)
    application_result_textbox.click()

    withdraw_option = page.get_by_role("option", name="Відрахувати")
    shared_actions.wait_for_visible_and_stable(withdraw_option)
    withdraw_option.click()

    result_date_textbox = page.get_by_role("textbox", name="Дата прийняття рішення *")
    shared_actions.wait_for_visible_and_stable(result_date_textbox)
    result_date_textbox.fill(withdrawal_date.strftime(DATE_FORMAT))

    shared_actions.click_on_html_body(page)

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.wait_network_idle(page)


def fill_withdrawal_info(
    withdrawal_date: datetime.date, withdrawal_order_number: str, withdrawal_order_reason: str, page: Page
):

    logger.info(f"Filling withdrawal info")
    order_number_textbox = page.get_by_role("textbox", name="Номер наказу *")
    shared_actions.wait_for_visible_and_stable(order_number_textbox)
    order_number_textbox.fill(withdrawal_order_number)

    withdrawal_date_textbox = page.get_by_role("textbox", name="Дата відрахування *")
    shared_actions.wait_for_visible_and_stable(withdrawal_date_textbox)
    withdrawal_date_textbox.fill(withdrawal_date.strftime(DATE_FORMAT))

    shared_actions.click_on_html_body(page)

    order_date_textbox = page.get_by_role("textbox", name="Дата наказу *")
    shared_actions.wait_for_visible_and_stable(order_date_textbox)
    order_date_textbox.fill(withdrawal_date.strftime(DATE_FORMAT))

    shared_actions.click_on_html_body(page)

    order_reason_textbox = page.get_by_role("textbox", name="Підстава наказу *")
    shared_actions.wait_for_visible_and_stable(order_reason_textbox)
    order_reason_textbox.fill(withdrawal_order_reason)

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.wait_network_idle(page)


def withdraw_student(
    student_surname: str,
    student_name: str,
    parent_full_name: str,
    parent_phone_number: str,
    parent_relationship_to_student: RelationshipToStudentType,
    withdrawal_date: datetime.date,
    withdrawal_type: WithdrawalType,
    withdrawal_order_number: str,
    withdrawal_order_reason: str,
    page: Page,
):

    logger.info(f"Processing student {student_name} {student_surname}")
    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)
    student_menu.go_to_student_withdrawal_during_year(page)

    was_student_found = find_student(student_surname, student_name, page)

    if not was_student_found:
        logger.warning(f"Student {student_name} {student_surname} was not found in AIKOM. Skip.")
        return

    select_withdrawal_type(withdrawal_type, page)
    fill_parent_info(parent_full_name, parent_phone_number, withdrawal_date, parent_relationship_to_student, page)
    fill_application_acceptance_info(withdrawal_date, page)
    fill_withdrawal_info(withdrawal_date, withdrawal_order_number, withdrawal_order_reason, page)

    shared_actions.fill_auth_key_iframe_and_sign(page)

    logger.info(f"Done student {student_name} {student_surname}")
