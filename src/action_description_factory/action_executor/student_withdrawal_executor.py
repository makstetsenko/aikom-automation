import pathlib

from playwright.sync_api import Page

from src import actions
from src.action_description_factory.action_executor import dto
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    students = dto.withdrawal_student.read_students_from_csv(data_source)

    for s in students:
        if s.was_withdrawal_done:
            continue

        main_page.go_to_main_page(page)

        actions.student_withdrawal.withdraw_student(
            student_name=s.name,
            student_surname=s.surname,
            parent_full_name=s.parent_full_name,
            parent_phone_number=s.parent_phone_number,
            withdrawal_date=s.withdrawal_date,
            withdrawal_order_number=s.withdrawal_order_number,
            parent_relationship_to_student=actions.student_withdrawal.RelationshipToStudentType(
                s.parent_relationship_to_student
            ),
            withdrawal_type=actions.student_withdrawal.WithdrawalType(s.withdrawal_type),
            withdrawal_order_reason=s.withdrawal_order_reason,
            page=page,
        )
