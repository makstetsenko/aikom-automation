import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, student_menu
from src.actions.shared.students import update_profile

logger = logging.getLogger(__name__)


def check_if_student_requires_meal(name: str, surname: str, checked: bool, page: Page):
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

    # ---
    shared_actions.try_close_all_stupid_popups(page)

    if not update_profile.update_profile_page.has_any_living_address(page):
        update_profile.update_profile_page.click_on_add_living_address(page)
        modal = update_profile.add_living_address_modal.get_modal(page)
        update_profile.add_living_address_modal.select_country("Україна", modal)
        update_profile.add_living_address_modal.save(modal)

    update_profile.update_profile_page.check_has_free_meal(checked, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)
