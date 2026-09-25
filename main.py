import datetime
import logging
import pathlib

from playwright.sync_api import Page, expect, sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.actions import student_withdrawal as student_withdrawal_action, teaching_load_setup
from src.actions.shared import main_page
from src.app_logging import setup_logging
from src.browser import create_browser
from src.domain import withdrawal_student as withdrawal_student_domain

logger = logging.getLogger("main")


def withdraw_students(page: Page):
    data_path = pathlib.Path("./data/students/withdrawal/На відрахування 10 класи - Sheet1-2.csv")
    students = withdrawal_student_domain.read_students_from_csv(data_path)

    for s in students:
        main_page.go_to_main_page(page)

        student_withdrawal_action.withdraw_student(
            student_name=s.name,
            student_surname=s.surname,
            parent_full_name=s.parent_full_name,
            parent_phone_number=s.parent_phone_number,
            withdrawal_date=datetime.date.strptime(s.withdrawal_date, "%d.%m.%Y"),
            withdrawal_order_number=s.withdrawal_order_number,
            parent_relationship_to_student=student_withdrawal_action.RelationshipToStudentType(
                s.parent_relationship_to_student
            ),
            withdrawal_type=student_withdrawal_action.WithdrawalType(s.withdrawal_type),
            withdrawal_order_reason=s.withdrawal_order_reason,
            page=page,
        )




def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        # ---
        # Here uncomment required actions.
        # Later I will add actions setup and choosing from config or smth
        # ---

        withdraw_students(page)

        context.close()


if __name__ == "__main__":
    setup_logging()
    main()
