import datetime
import logging
import pathlib

from playwright.sync_api import Page, expect, sync_playwright, TimeoutError as PlaywrightTimeoutError
from src import actions
from src.actions import (
    student_oop_level,
    student_withdrawal as student_withdrawal_action,
    teaching_load_setup,
    update_classes_type,
)
from src.actions.shared import main_page
from src.actions.shared.update_class.search_class_page import StudyingForm
from src.app_logging import setup_logging
from src.browser import create_browser
from src.domain import (
    enrolment_student,
    student_with_oop,
    teaching_load,
    update_class_type_model,
    withdrawal_student as withdrawal_student_domain,
)

logger = logging.getLogger("main")


def withdraw_students(page: Page):
    data_path = pathlib.Path("./data/students/withdrawal/ВІдрахування учня (Responses) - Form Responses 1 (1).csv")
    students = withdrawal_student_domain.read_students_from_csv(data_path)

    for s in students:
        if s.was_withdrawal_done:
            continue
        
        main_page.go_to_main_page(page)

        student_withdrawal_action.withdraw_student(
            student_name=s.name,
            student_surname=s.surname,
            parent_full_name=s.parent_full_name,
            parent_phone_number=s.parent_phone_number,
            withdrawal_date=s.withdrawal_date,
            withdrawal_order_number=s.withdrawal_order_number,
            parent_relationship_to_student=student_withdrawal_action.RelationshipToStudentType(
                s.parent_relationship_to_student
            ),
            withdrawal_type=student_withdrawal_action.WithdrawalType(s.withdrawal_type),
            withdrawal_order_reason=s.withdrawal_order_reason,
            page=page,
        )


def students_enrolment(page: Page):
    data_path = pathlib.Path("./data/students/enrolment/Зарахування учня (Відповіді) - Відповіді форми (1) (2).csv")
    students = enrolment_student.read_students_from_csv(data_path)

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


def setup_teaching_load(page: Page):

    load_configs = teaching_load.read_from_directory(pathlib.Path("data/teaching_load"))

    for c in load_configs:
        main_page.go_to_main_page(page)

        teaching_load_setup.setup_teaching_load_for_teacher(
            academic_year="2026-2027",
            work_place="ЛІЦЕЙ № 289",
            teacher_name=c.staff_name,
            teacher_surname=c.staff_surname,
            teaching_load_configs=[
                teaching_load_setup.TeachingLoadConfig(
                    job_title=c.job_title,
                    load_group_type=teaching_load_setup.LoadGroupType.SUBJECT,
                    teaching_classes=s.classes,
                    teaching_hours_per_week=s.hours_per_week,
                    is_main_teaching_subject=s.is_main,
                    teaching_subject=s.name,
                )
                for s in c.subjects
            ],
            page=page,
        )


def setup_students_oop_level(page: Page):
    students = student_with_oop.read_students_from_csv(pathlib.Path("data/учні-очні-рівень-ірц-2026-2027-2.csv"))

    for s in students:
        main_page.go_to_main_page(page)

        student_oop_level.configure_oop_level_for_student(
            name=s.name, surname=s.surname, oop_level=s.oop_level, page=page
        )


def update_classes_types(page: Page):
    classes = update_class_type_model.read_from_csv(pathlib.Path("data/classes/спец-класи-2026-2027 copy.csv"))

    for c in classes:
        main_page.go_to_main_page(page)
        update_classes_type.update_class_type(
            academic_year=c.academic_year,
            class_year=c.class_year,
            class_name=c.class_name,
            class_teacher_name=c.class_teacher_name,
            class_studying_form=c.class_studying_form,
            class_type=c.class_type,
            page=page,
        )


def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        # main_page.go_to_main_page(page)
        # input("PRESS ENTER")

        # ---
        # Here uncomment required actions.
        # Later I will add actions setup and choosing from config or smth
        # ---

        withdraw_students(page)

        # setup_teaching_load(page)

        # setup_students_oop_level(page)

        # update_classes_types(page)
        
        # students_enrolment(page)

        context.close()


if __name__ == "__main__":
    setup_logging()
    main()
