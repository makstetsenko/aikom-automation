import pathlib

from playwright.sync_api import Page

from src import actions
from src.action_description_factory.action_executor import dto
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    students = dto.transfer_student.read_students_from_csv(data_source)

    for s in students:
        if s.was_done:
            continue

        main_page.go_to_main_page(page)
        actions.student_transfer.transfer_student(
            student_name=s.student_name,
            student_surname=s.student_surname,
            transfer_type=s.transfer_type,
            order_number=s.order_number,
            order_date=s.order_date,
            from_academic_year=s.from_academic_year,
            from_studying_form=s.from_studying_form,
            from_class_year=s.from_class_year,
            from_class_name=s.from_class_name,
            to_academic_year=s.to_academic_year,
            to_studying_form=s.to_studying_form,
            to_class_year=s.to_class_year,
            to_class_name=s.to_class_name,
            page=page,
        )
