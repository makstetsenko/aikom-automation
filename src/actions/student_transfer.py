import datetime
import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, student_menu
from src.actions.shared.students import transfer_between_classes
from src.domain.aikom_enums import StudentTransferOrderType, StudyingForm

logger = logging.getLogger(__name__)


def transfer_student(
    student_name: str,
    student_surname: str,
    transfer_type: StudentTransferOrderType,
    order_number: str,
    order_date: datetime.date,
    from_academic_year: str,
    from_studying_form: StudyingForm,
    from_class_year: int,
    from_class_name: str | None,
    to_academic_year: str,
    to_studying_form: StudyingForm,
    to_class_year: int,
    to_class_name: str | None,
    page: Page,
):

    logger.info(f"Processing student {student_name} {student_surname}")

    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)
    student_menu.go_to_student_student_transfer_between_years(page)

    transfer_between_classes.search_page.select_transfer_type(transfer_type, page)

    transfer_between_classes.search_page.select_from_academic_year_and_studying_form(
        from_academic_year, from_studying_form, page
    )
    transfer_between_classes.search_page.select_from_class_year(from_class_year, page)

    if not from_class_name is None and from_class_name != "":
        transfer_between_classes.search_page.select_from_class(from_class_name, page)

    transfer_between_classes.search_page.select_to_academic_year_and_studying_form(
        to_academic_year, to_studying_form, page
    )
    transfer_between_classes.search_page.select_to_class_year(to_class_year, page)

    if not to_class_name is None and to_class_name != "":
        transfer_between_classes.search_page.select_to_class(to_class_name, page)

    shared_actions.click_next_button_on_page(page)

    transfer_between_classes.students_selection_page.check_student(student_name, student_surname, page)
    transfer_between_classes.students_selection_page.fill_order_number(order_number, page)
    transfer_between_classes.students_selection_page.fill_order_date(order_date, page)
    transfer_between_classes.students_selection_page.fill_enrolment_date(order_date, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)
