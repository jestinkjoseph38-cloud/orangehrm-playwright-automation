from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Post-login landing page, home of the top navigation."""

    DASHBOARD_HEADER = "h6.oxd-topbar-header-breadcrumb-module"

    def is_loaded(self, timeout=10000):
        try:
            self.page.locator(self.DASHBOARD_HEADER).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_header_text(self):
        return self.page.locator(self.DASHBOARD_HEADER).first.inner_text()
