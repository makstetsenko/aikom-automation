import pathlib

from playwright.sync_api import Page

from src.action_description_factory.action_executor import dto
from src.actions import teaching_load_setup
from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    load_configs = dto.teaching_load.read_from_directory(data_source)

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
