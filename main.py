import logging

from playwright.sync_api import sync_playwright
from src import action_description_factory
from src.app_args import get_app_args
from src.app_logging import setup_logging
from src.browser import create_browser

logger = logging.getLogger("main")


def main():
    app_args = get_app_args()
    action_descriptor = action_description_factory.action_descriptor.read_from_yaml_file(
        app_args.action_descriptor_path
    )

    with sync_playwright() as p:
        context = create_browser(p)
        page = context.pages[0] if context.pages else context.new_page()

        while not action_descriptor is None:
            action_description_factory.execute(action_descriptor, page)
            action_descriptor = action_descriptor.next

        # input("PRESS ENTER")

        context.close()


if __name__ == "__main__":
    setup_logging()
    main()
