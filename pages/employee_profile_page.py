import re

from pages.base_page import BasePage


class EmployeeProfilePage(BasePage):
    """Shell shared by every tab (Personal Details, Job, ...) of a single employee record."""

    JOB_TAB_LINK = 'a:has-text("Job")'
    FIRST_NAME_INPUT = 'input[name="firstName"]'
    LAST_NAME_INPUT = 'input[name="lastName"]'

    def get_employee_number(self):
        match = re.search(r"empNumber/(\d+)", self.page.url)
        return match.group(1) if match else None

    def get_full_name(self):
        first = self.page.locator(self.FIRST_NAME_INPUT).input_value()
        last = self.page.locator(self.LAST_NAME_INPUT).input_value()
        return f"{first} {last}"

    def go_to_job_tab(self):
        from pages.job_details_page import JobDetailsPage

        self.page.click(self.JOB_TAB_LINK)
        self.wait_for_page_load()
        return JobDetailsPage(self.page)
