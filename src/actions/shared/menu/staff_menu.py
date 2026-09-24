from playwright.sync_api import Page

from src.actions.shared import shared_actions


def go_to_update_staff_teaching_load(page: Page):
    page.get_by_text("Оновлення інформації про працівника (навантаження)").click()
    shared_actions.wait_network_idle(page)
