import logging

from playwright.sync_api import Page, expect

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, student_menu
from src.actions.shared.students import update_profile
from src.actions.shared.students.update_profile import add_living_address_modal


logger = logging.getLogger(__name__)



def configure_oop_level_for_student(name: str, surname: str, sen_level: int, page: Page):
    logger.info(f"Processing student {name} {surname}")
    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)

    student_menu.go_to_student_update_page(page)

    was_student_found = update_profile.search_page.try_find_student(surname, name, page)

    if not was_student_found:
        logger.warning(f"Student {name} {surname} was not found. Skip.")
        return

    shared_actions.click_next_button_on_page(page)

    shared_actions.wait(page, 1000)

    if not update_profile.update_profile_page.has_any_living_address(page):
        update_profile.update_profile_page.click_on_add_living_address(page)
        modal = add_living_address_modal.get_modal(page)
        add_living_address_modal.select_country("Україна", modal)
        add_living_address_modal.save(modal)

    shared_actions.click_next_button_on_page(page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.try_close_all_stupid_popups(page)

    update_profile.update_profile_page.check_special_education_needs_enabled(checked=True, page=page)
    update_profile.update_profile_page.select_special_education_needs_level(sen_level, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)
