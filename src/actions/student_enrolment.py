import datetime

from playwright.sync_api import Page

from src.actions.shared import create_student_profile, shared_actions, student_enrolment_from_another_school
from src.actions.shared.menu import main_menu, student_menu
from src.domain.aikom_enums import DocumentType, RelationshipToStudentType, StudyingForm


import logging

logger = logging.getLogger(__name__)


def enroll_student_from_another_school(
    student_birth_certificate_serial: str,
    student_birth_certificate_number: str,
    academic_year: str,
    studying_form: StudyingForm,
    class_year: int,
    class_name: str,
    parent_name: str,
    parent_phone_number: str,
    parent_relationship_to_student: RelationshipToStudentType,
    enrolment_date: datetime.date,
    enrolment_order_number: str,
    page: Page,
):

    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)

    student_menu.go_to_student_enrollment_from_another_school_page(page)

    student_enrolment_from_another_school.search_page.select_document_type(DocumentType.BIRTH_CERTIFICATE, page)
    student_enrolment_from_another_school.search_page.fill_birth_certificate_serial(
        student_birth_certificate_serial, page
    )
    student_enrolment_from_another_school.search_page.fill_birth_certificate_number(
        student_birth_certificate_number, page
    )
    student_enrolment_from_another_school.search_page.select_academic_year(academic_year, studying_form, page)
    student_enrolment_from_another_school.search_page.select_class_year(class_year, page)
    student_enrolment_from_another_school.search_page.select_class_name(class_name, page)

    shared_actions.click_next_button_on_page(page)

    student_enrolment_from_another_school.enrolment_page.fill_parent_name(parent_name, page)
    student_enrolment_from_another_school.enrolment_page.select_relationship_to_student(
        parent_relationship_to_student, page
    )
    student_enrolment_from_another_school.enrolment_page.fill_parent_phone_number(parent_phone_number, page)
    student_enrolment_from_another_school.enrolment_page.check_parent_has_identical_document(page)
    student_enrolment_from_another_school.enrolment_page.fill_order_date(enrolment_date, page)
    student_enrolment_from_another_school.enrolment_page.fill_order_number(enrolment_order_number, page)
    student_enrolment_from_another_school.enrolment_page.fill_application_submission_date(enrolment_date, page)

    shared_actions.click_next_button_on_page(page)

    shared_actions.fill_auth_key_iframe_and_read_key_and_click_continue(page)


def enroll_student(
    student_birth_certificate_serial: str,
    student_birth_certificate_number: str,
    student_birth_date: datetime.date,
    academic_year: str,
    studying_form: StudyingForm,
    class_year: int,
    class_name: str,
    parent_name: str,
    parent_phone_number: str,
    parent_relationship_to_student: RelationshipToStudentType,
    enrolment_date: datetime.date,
    enrolment_order_number: str,
    page: Page,
):

    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_students(page)

    student_menu.go_to_create_student_profile_page(page)

    create_student_profile.search_page.select_document_type(document_type=DocumentType.BIRTH_CERTIFICATE, page=page)
    create_student_profile.search_page.fill_birth_certificate_serial(student_birth_certificate_serial, page)
    create_student_profile.search_page.fill_birth_certificate_number(student_birth_certificate_number, page)
    create_student_profile.search_page.fill_birth_date(student_birth_date, page)

    shared_actions.click_next_button_on_page(page)

    if create_student_profile.search_page.is_student_missing(page):
        logger.warning(f"Student {student_birth_certificate_serial} {student_birth_certificate_number} was not found")
        return

    found_student_info = create_student_profile.search_page.try_get_student_search_result(page)

    # create student profile from scratch (aikom profile does not exist)
    if found_student_info is None:
        raise Exception("Creating student from scratch is not implemented")

    # enroll student from another school (aikom profile exists and linked with another school)
    school_types = ["ліцей", "школа", "гімназія"]

    if any([s in found_student_info.school_name.lower() for s in school_types]):
        enroll_student_from_another_school(
            found_student_info.birth_certificate_serial,  # pass here value from search result because our registry DBs could have old birthdate certificate
            found_student_info.birth_certificate_number,  # pass here value from search result because our registry DBs could have old birthdate certificate
            academic_year,
            studying_form,
            class_year,
            class_name,
            parent_name,
            parent_phone_number,
            parent_relationship_to_student,
            enrolment_date,
            enrolment_order_number,
            page,
        )
        return

    # enroll student that does not linked with any school
    raise Exception("Moving student that does not linked to school is not implemented")
