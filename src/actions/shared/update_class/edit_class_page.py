from enum import StrEnum

from playwright.sync_api import Page

from src.actions.shared import shared_actions


class ClassType(StrEnum):
    ON_CAMPUS = "Загального типу денний очний"
    SPECIALIZED = "Спеціальний"
    BLENDED = "Загального типу денний змішаний"


def is_class_teacher_selected(page: Page):
    textbox = page.get_by_role("textbox", name="Керівник класу *")
    return textbox.inner_text().strip() != ""


def select_class_teacher(teacher_name: str, page: Page):
    page.get_by_role("textbox", name="Керівник класу *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=teacher_name)
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)


def get_class_type(page: Page) -> ClassType | None:
    textbox = page.get_by_role("textbox", name="Тип класу *")
    class_type = textbox.inner_text().strip()
    
    if class_type == "":
        return None
    
    return ClassType(class_type)


def select_class_type(class_type: ClassType, page: Page):
    page.get_by_role("textbox", name="Тип класу *").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)

    option = page.get_by_role("option", name=class_type)
    shared_actions.wait_for_visible(option)

    option.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, timeout=500)
