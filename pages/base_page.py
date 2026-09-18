class BasePage:
    """Common behaviour shared by every page object.

    The left sidebar (PIM link) and the top-right user dropdown (Logout)
    are part of OrangeHRM's global authenticated shell, so the navigation
    helpers for them live here rather than being duplicated per page.
    """

    TOAST_MESSAGE = ".oxd-text--toast-message"
    PIM_MENU_LINK = 'a:has-text("PIM")'
    USER_DROPDOWN = ".oxd-userdropdown-tab"
    LOGOUT_LINK = 'a:has-text("Logout")'

    def __init__(self, page):
        self.page = page

    def wait_for_page_load(self):
        self.page.wait_for_load_state("networkidle")
        return self

    def get_toast_message(self, timeout=8000):
        toast = self.page.locator(self.TOAST_MESSAGE).first
        toast.wait_for(state="visible", timeout=timeout)
        return toast.inner_text()

    def current_url(self):
        return self.page.url

    def go_to_pim(self):
        from pages.employee_list_page import EmployeeListPage

        self.page.click(self.PIM_MENU_LINK)
        self.wait_for_page_load()
        return EmployeeListPage(self.page)

    def logout(self):
        from pages.login_page import LoginPage

        self.page.click(self.USER_DROPDOWN)
        self.page.click(self.LOGOUT_LINK)
        self.wait_for_page_load()
        return LoginPage(self.page)
