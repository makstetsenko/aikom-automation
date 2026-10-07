import pathlib

from playwright.sync_api import Page

from src.action_description_factory.action_executor import dto
from src.actions import update_classes_type
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    classes = dto.update_class_type.read_from_csv(data_source)

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
