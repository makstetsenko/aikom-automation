import pathlib

from playwright.sync_api import Page


def execute(data_source: pathlib.Path | None, page: Page):
    if data_source is None:
        raise ValueError("Data source is required")

    raise Exception("Action is not implemented")
