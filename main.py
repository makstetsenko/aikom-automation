from playwright.sync_api import Page, expect, sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.actions.shared import main_page
from src.browser import create_browser

AIKOM_URL = "https://cabinet.aikom.gov.ua"


def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        page.goto(AIKOM_URL)

        # ---
        # Here uncomment required actions.
        # Later I will add actions setup and choosing from config or smth
        # ---

        main_page.go_to_main_page(page)
        input("Press Enter to continue..")

        context.close()


if __name__ == "__main__":
    main()
