from playwright.sync_api import Page

from src.actions.shared import shared_actions

def get_living_address_div(page: Page):
    return page.get_by_text("Адреса фактичного місця проживання", exact=True).locator("..")

def get_living_address_table(page: Page):
    table = get_living_address_div(page).locator("table")
    return table



def has_any_living_address(page: Page):
    table = get_living_address_table(page)
    table_without_records = table.filter(has_text="В цій таблиці поки що немає записів")
    return table_without_records.count() == 0

def click_on_add_living_address(page: Page):
    btn = get_living_address_div(page).get_by_role("button", name="Додати")
    btn.click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 500)
    
    
