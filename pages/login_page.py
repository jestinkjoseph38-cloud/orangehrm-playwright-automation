from config.config import Config
from pages.base_page import BasePage


class LoginPage(BasePage):
    """OrangeHRM login screen."""

    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    ERROR_ALERT = ".oxd-alert-content-text"

    def open(self):
        self.page.goto(Config.LOGIN_URL)
        self.wait_for_page_load()
        return self

    def login(self, username, password):
        from pages.dashboard_page import DashboardPage

        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.SUBMIT_BUTTON)
        self.wait_for_page_load()
        return DashboardPage(self.page)

    def get_error_message(self):
        return self.page.locator(self.ERROR_ALERT).first.inner_text()

    def is_on_login_page(self, timeout=10000):
        try:
            self.page.locator(self.USERNAME_INPUT).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
