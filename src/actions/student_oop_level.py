import logging

from playwright.sync_api import Page, expect

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, student_menu

logger = logging.getLogger(__name__)


def find_student(student_surname: str, student_name: str, page: Page) -> bool:
    logger.info(f"Try find student {student_name} {student_surname}")

    surname_input = page.get_by_role("textbox", name="Прізвище для пошуку *")
    shared_actions.wait_for_visible_and_stable(surname_input)
    surname_input.fill(student_surname)

    name_input = page.get_by_role("textbox", name="Ім'я для пошуку")
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
        expect(missing_student_text).to_be_visible(timeout=1_000)
        return False
    except:
        pass  # student was found -> this text wont appear -> continue flow

    shared_actions.click_next_button_on_page(page)

    return True


def fill_oop_info(oop_level: int, page: Page):
    shared_actions.try_close_all_stupid_popups(page)
    
    studying_needs_checkbox = page.get_by_role("checkbox", name="Особливі освітні потреби")
    shared_actions.wait_for_visible(studying_needs_checkbox)
    
    # do uncheck -> check just to enable field oop_level_textbox
    studying_needs_checkbox.uncheck()    
    studying_needs_checkbox.check()

    oop_level_textbox = page.get_by_role("textbox", name="Необхідний рівень підтримки: *")
    shared_actions.wait_for_visible(oop_level_textbox)
    oop_level_textbox.click()

    oop_level_option = page.get_by_role("option", name=f"{oop_level}-й рівень")
    shared_actions.wait_for_visible(oop_level_option)
    oop_level_option.click()


def configure_oop_level_for_student(name: str, surname: str, oop_level: int, page: Page):
    logger.info(f"Processing student {name} {surname}")
    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)
    student_menu.go_to_student_update_page(page)

    was_student_found = find_student(surname, name, page)

    if not was_student_found:
        logger.warning(f"Student {name} {surname} was not found. Skip.")
        return

    shared_actions.click_next_button_on_page(page)

    shared_actions.click_next_button_on_page(page)

    fill_oop_info(oop_level, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_sign(page)
