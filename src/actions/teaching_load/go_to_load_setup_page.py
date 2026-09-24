
from playwright.sync_api import Page

from src.actions.shared.menu import main_menu, staff_menu


def go_load_setup(page: Page):
    main_menu.go_to_available_service(page)
    main_menu.go_to_information_about_staff(page)
    staff_menu.go_to_update_staff_teaching_load(page)