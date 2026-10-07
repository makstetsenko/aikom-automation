import pathlib

from playwright.sync_api import Page

from src import actions
from src.action_description_factory.action_executor import dto
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    students = dto.enrolment_student.read_students_from_csv(data_source)

    for s in students:
        if s.was_enrolment_done:
            continue

        main_page.go_to_main_page(page)
        actions.student_enrolment.enroll_student(
            student_birth_certificate_serial=s.student_birth_certificate_serial,
            student_birth_certificate_number=s.student_birth_certificate_number,
            student_birth_date=s.student_birth_date,
            academic_year=s.academic_year,
            studying_form=s.studying_form,
            class_year=s.class_year,
            class_name=s.class_name,
            parent_name=s.parent_name,
            parent_phone_number=s.parent_phone_number,
            parent_relationship_to_student=s.parent_relationship_to_student,
            enrolment_date=s.enrolment_date,
            enrolment_order_number=s.enrolment_order_number,
            page=page,
        )
