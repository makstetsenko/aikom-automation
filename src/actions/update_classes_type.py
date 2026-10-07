import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, school_menu
from src.actions.shared.school.update_class import search_class_page
from src.actions.shared.school.update_class import edit_class_page
from src.actions.shared.school.update_class.edit_class_page import ClassType
from src.actions.shared.school.update_class.search_class_page import StudyingForm

logger = logging


def update_class_type(
    academic_year: str,
    class_year: int,
    class_name: str,
    class_studying_form: StudyingForm,
    class_teacher_name: str,
    class_type: ClassType,
    page: Page,
):

    main_menu.go_to_available_service(page)
    main_menu.go_to_school_menu(page)
    school_menu.go_to_update_classes(page)

    search_class_page.select_academic_year(academic_year, page)
    search_class_page.select_studying_form(class_studying_form, page)
    search_class_page.select_class_year(class_year, page)
    search_class_page.select_class_name(class_name, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.wait(page, timeout=1000)

    is_class_teacher_selected = edit_class_page.is_class_teacher_selected(page)
    is_class_type_already_correct = edit_class_page.get_class_type(page) == class_type

    # Do nothing if data is already correct
    if is_class_teacher_selected and is_class_type_already_correct:
        return

    if not is_class_teacher_selected:
        edit_class_page.select_class_teacher(class_teacher_name, page)

    edit_class_page.select_class_type(class_type, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)
