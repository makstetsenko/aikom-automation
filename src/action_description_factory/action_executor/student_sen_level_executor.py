import pathlib

from playwright.sync_api import Page

from src.action_description_factory.action_executor import dto
from src.actions import student_sen_level
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    students = dto.student_with_sen.read_students_from_csv(data_source)

    for s in students:
        main_page.go_to_main_page(page)

        student_sen_level.configure_oop_level_for_student(
            name=s.name, surname=s.surname, sen_level=s.oop_level, page=page
        )
