import logging
import re

from playwright.sync_api import Locator, Page
from pydantic import BaseModel
from enum import StrEnum

from src.actions.shared import shared_actions
from src.actions.shared.menu import main_menu, staff_menu

logger = logging.getLogger(__name__)


class LoadGroupType(StrEnum):
    SUBJECT = "Предмет"
    CLUB = "Гурток"
    AFTER_SCHOOL_CLUB = "ГПД"
    ELECTIVE = "Факультатив"


class JobTitle(StrEnum):
    JUNIOR_CLASSES_TEACHER = "Вчитель початкових класів закладу загальної середньої освіти"
    TEACHER = "Вчитель закладу загальної середньої освіти"


class TeachingLoadConfig(BaseModel):
    job_title: str
    load_group_type: LoadGroupType
    teaching_subject: str
    teaching_classes: list[str]
    is_main_teaching_subject: bool
    teaching_hours_per_week: float


def go_load_setup_page(surname: str, name: str, page: Page):
    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_staff(page)
    staff_menu.go_to_update_staff_teaching_load(page)

    surname_input = page.get_by_role("textbox", name="Прізвище для пошуку *")
    shared_actions.wait_for_visible_and_stable(surname_input)

    name_input = page.get_by_role("textbox", name="Ім'я для пошуку")
    shared_actions.wait_for_visible_and_stable(name_input)

    surname_input.fill(surname)
    name_input.fill(name)

    find_button = page.get_by_role("button", name="Знайти")
    shared_actions.wait_for_visible_and_stable(find_button)

    find_button.click()
    shared_actions.wait_network_idle(page)

    continue_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(continue_button)

    continue_button.click()
    shared_actions.wait_network_idle(page)


def select_job_title(job_title: str, modal: Locator):
    role_input = modal.get_by_role("textbox", name="Посада *")
    role_input.click()

    job_title_option = modal.page.get_by_role("option", name=job_title)
    shared_actions.wait_for_visible_and_stable(job_title_option)
    job_title_option.click()


def select_work_place(work_place: str, modal: Locator):
    work_place_input = modal.get_by_role("textbox", name="Місце роботи *")
    work_place_input.click()

    work_place_option = modal.page.get_by_role("option", name=work_place)
    shared_actions.wait_for_visible_and_stable(work_place_option)
    work_place_option.click()


def select_load_group_type(load_group_type: str, modal: Locator):
    modal.get_by_role("radio", name=load_group_type).check()
    shared_actions.wait_network_idle(modal.page)


def select_subject(subject: str, modal: Locator):
    subject_input = modal.get_by_role("textbox", name="Предмет викладання у класі *")
    subject_input.click()
    shared_actions.wait_network_idle(modal.page)

    subject_option = modal.page.get_by_role("option", name=subject, exact=True)
    shared_actions.wait_for_visible_and_stable(subject_option)

    subject_option.click()
    shared_actions.wait_network_idle(modal.page)


def set_is_main_teaching_subject(is_main_teaching_subject: bool, modal: Locator):
    is_main_subject_checkbox = modal.get_by_role("checkbox", name="Основний предмет викладання")
    shared_actions.wait_for_visible(is_main_subject_checkbox)

    if is_main_teaching_subject:
        is_main_subject_checkbox.check()
    else:
        is_main_subject_checkbox.uncheck()


def select_teaching_class(class_name: str, modal: Locator):
    modal.get_by_role("textbox", name="Класи *").click()

    class_name_option = modal.page.get_by_role("option", name=re.compile(rf"^{re.escape(class_name)}"))
    shared_actions.wait_network_idle(modal.page)
    shared_actions.wait_for_visible_and_stable(class_name_option)

    class_name_option.click()
    shared_actions.wait_network_idle(modal.page)


def set_teaching_hours_per_week(hors_per_week: float, modal: Locator):
    def format_number(value: float) -> str:
        return f"{value:g}".replace(".", ",")

    input = modal.get_by_role("textbox", name="К-ть годин на тиждень *")
    input.clear()
    input.fill(format_number(hors_per_week))


def set_academic_year(academic_year: str, modal: Locator):
    modal.get_by_role("textbox", name="Навчальний рік *").click()

    academic_year_option = modal.page.get_by_role("option", name=academic_year)
    shared_actions.wait_network_idle(modal.page)
    shared_actions.wait_for_visible_and_stable(academic_year_option)

    academic_year_option.click()
    shared_actions.wait_network_idle(modal.page)


def is_subject_row_exists(academic_year: str, subject_name: str, row: Locator) -> bool:
    existing_subject_name = row.locator("td").nth(2).inner_text()
    existing_academic_year = row.locator("td").nth(4).inner_text()

    return existing_subject_name == subject_name and existing_academic_year == academic_year


def does_load_table_has_no_data_text(table_with_teaching_load: Locator) -> bool:
    no_data_text = table_with_teaching_load.get_by_text("В цій таблиці поки що немає записів")
    return no_data_text.count() > 0


def is_teaching_load_exists(academic_year: str, subject_name: str, table_with_teaching_load: Locator) -> bool:
    if does_load_table_has_no_data_text(table_with_teaching_load) > 0:
        return False

    subject_rows = table_with_teaching_load.locator("tbody tr").all()

    for row in subject_rows:
        if is_subject_row_exists(academic_year, subject_name, row):
            return True

    return False


def click_on_save_changes_on_modal(load_modal: Locator):
    save_button = load_modal.get_by_role("button", name="Зберегти")
    save_button.click()  # Closes modal


def try_deselect_previous_main_subject(academic_year: str, subject_name: str, table_with_teaching_load: Locator):
    if does_load_table_has_no_data_text(table_with_teaching_load) > 0:
        return

    subject_rows = table_with_teaching_load.locator("tbody tr").all()

    for i, row in enumerate(subject_rows):
        is_main_subject_text = row.locator("td").nth(3).inner_text()
        if not is_main_subject_text.lower().strip() == "так":
            continue

        if is_subject_row_exists(academic_year, subject_name, row):
            continue

        logger.info(f"Deselect subject {subject_name} in academic year {academic_year} as main subject")

        table_option_button = table_with_teaching_load.get_by_label("table options").nth(i)
        table_option_button.click()  # opens popup with options to change or delete

        change_button = table_with_teaching_load.page.get_by_role("menuitem", name="Змінити")
        shared_actions.wait_for_visible_and_stable(change_button)
        change_button.click()

        change_load_modal = table_with_teaching_load.page.get_by_text("Змінити дані").locator("..")
        shared_actions.wait_for_visible_and_stable(change_load_modal)
        shared_actions.wait_network_idle(table_with_teaching_load.page)

        set_is_main_teaching_subject(False, change_load_modal)

        click_on_save_changes_on_modal(change_load_modal)  # closes modal


def has_new_main_subject_to_setup(configs: list[TeachingLoadConfig]):
    for c in configs:
        if c.is_main_teaching_subject:
            return True

    return False


def setup_teaching_load_for_teacher(
    academic_year: str,  # Format "2026-2027"
    work_place: str,  # Format "Ліцей №289"
    teacher_name: str,
    teacher_surname: str,
    teaching_load_configs: list[TeachingLoadConfig],
    page: Page,
):

    logger.info(f"Processing teacher {teacher_name} {teacher_surname}")

    go_load_setup_page(surname=teacher_surname, name=teacher_name, page=page)

    table_with_teaching_load = page.get_by_text("Навантаження", exact=True).locator("..")
    shared_actions.wait_for_visible(table_with_teaching_load)

    new_configs: list[TeachingLoadConfig] = []

    for config in teaching_load_configs:
        if is_teaching_load_exists(academic_year, config.teaching_subject, table_with_teaching_load):
            logger.warning(
                f"Subject {config.teaching_subject} for academic year {academic_year} was already configured. Skip."
            )
            continue

        new_configs.append(config)

    if len(new_configs) == 0:
        logger.info(f"Nothing to add. Done teacher {teacher_name} {teacher_surname}")
        return

    if has_new_main_subject_to_setup(new_configs):
        for c in new_configs:
            try_deselect_previous_main_subject(academic_year, c.teaching_subject, table_with_teaching_load)

    for config in new_configs:
        add_load_button = table_with_teaching_load.get_by_role("button", name="Додати")
        add_load_button.click()  # Opens modal

        add_load_modal = page.get_by_text("Внести дані").locator("..")
        shared_actions.wait_for_visible_and_stable(add_load_modal)
        shared_actions.wait_network_idle(page)

        # Order is important here for AIKOM.

        select_job_title(config.job_title, add_load_modal)
        select_work_place(work_place, add_load_modal)
        select_load_group_type(config.load_group_type, add_load_modal)
        select_subject(config.teaching_subject, add_load_modal)

        # junior school does not have "main" subject
        if not config.job_title.lower() == JobTitle.JUNIOR_CLASSES_TEACHER.lower():
            set_is_main_teaching_subject(config.is_main_teaching_subject, add_load_modal)

        set_academic_year(academic_year, add_load_modal)

        for c in config.teaching_classes:
            select_teaching_class(c, add_load_modal)

        set_teaching_hours_per_week(config.teaching_hours_per_week, add_load_modal)

        # ***

        click_on_save_changes_on_modal(add_load_modal)  # closes modal

    next_button = page.get_by_role("button", name="Далі")
    shared_actions.wait_for_visible_and_stable(next_button)
    next_button.click()

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)

    logger.info(f"Done teacher {teacher_name} {teacher_surname}")
