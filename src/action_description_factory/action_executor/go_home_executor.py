import pathlib

from playwright.sync_api import Page

from src.actions.shared import main_page


def execute(data_source: pathlib.Path | None, page: Page):
    main_page.go_to_main_page(page)
