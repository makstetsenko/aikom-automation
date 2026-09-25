import logging

from playwright.sync_api import Page, expect, sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.actions import teaching_load_setup
from src.actions.shared import main_page
from src.app_logging import setup_logging
from src.browser import create_browser

logger = logging.getLogger("main")


def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        # ---
        # Here uncomment required actions.
        # Later I will add actions setup and choosing from config or smth
        # ---

        main_page.go_to_main_page(page)

        context.close()


if __name__ == "__main__":
    setup_logging()
    main()
