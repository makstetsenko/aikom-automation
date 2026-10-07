
import logging

from playwright.sync_api import Page

from src.actions.shared import shared_actions

logger = logging.getLogger(__name__)

def fill_student_surname(surname: str, page: Page):
    surname_input = page.get_by_role("textbox", name="Прізвище для пошуку *")
    shared_actions.wait_for_visible_and_stable(surname_input)
    surname_input.fill(surname)
    
    
def fill_student_name(student_name: str, page: Page):
    name_input = page.get_by_role("textbox", name="Ім'я для пошуку")
    shared_actions.wait_for_visible_and_stable(name_input)
    name_input.fill(student_name)
    
    
def click_search_button(page: Page):
    search_button = page.get_by_role("button", name="Знайти")
    shared_actions.wait_for_visible_and_stable(search_button)
    search_button.click()
    shared_actions.wait_network_idle(page)
    
    
    
    
def is_student_missing(page: Page):
    for _ in range(5):
        missing_student_text = page.get_by_text(
            "Дитину з такими даними не знайдено в Реєстрі. Будь ласка, перевірте введені дані та спробуйте ще раз."
        )

        try:
            shared_actions.wait_for_visible(missing_student_text, timeout=200)
            return False
        except:
            pass  # student was found -> this text wont appear -> continue flow
    
    return True






def try_find_student(student_surname: str, student_name: str, page: Page) -> bool:
    logger.info(f"Try find student {student_name} {student_surname}")

    fill_student_surname(student_surname, page)
    fill_student_name(student_name, page)
    click_search_button(page)

    return not is_student_missing(page)