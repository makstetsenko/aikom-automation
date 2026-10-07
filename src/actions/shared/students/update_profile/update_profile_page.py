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


def check_special_education_needs_enabled(checked: bool, page: Page):
    studying_needs_checkbox = page.get_by_role("checkbox", name="Особливі освітні потреби")
    shared_actions.wait_for_visible(studying_needs_checkbox)

    if checked:
        # doing this stupid thing because this then enables/disables SEN level dropdown
        studying_needs_checkbox.uncheck()
        studying_needs_checkbox.check()
    else:
        studying_needs_checkbox.check()
        studying_needs_checkbox.uncheck()
        
    shared_actions.wait(page, 500)
        
        
def select_special_education_needs_level(level: int, page: Page):
    sen_level_textbox = page.get_by_role("textbox", name="Необхідний рівень підтримки: *")
    shared_actions.wait_for_visible(sen_level_textbox)
    sen_level_textbox.click()

    sen_level_option = page.get_by_role("option", name=f"{level}-й рівень")
    shared_actions.wait_for_visible(sen_level_option)
    sen_level_option.click()
    
    
def check_has_free_meal(checked: bool, page: Page):
    checkbox = page.get_by_role("checkbox", name="Забезпечується безкоштовним харчуванням")
    
    if checked:
        checkbox.check()
    else:
        checkbox.uncheck()