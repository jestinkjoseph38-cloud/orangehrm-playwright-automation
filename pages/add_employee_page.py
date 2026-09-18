from pages.base_page import BasePage


class AddEmployeePage(BasePage):
    """PIM > Add Employee form."""

    FIRST_NAME_INPUT = 'input[name="firstName"]'
    LAST_NAME_INPUT = 'input[name="lastName"]'
    EMPLOYEE_ID_INPUT = '.oxd-grid-item:has(label:text("Employee Id")) input'
    PHOTO_INPUT = 'input[type="file"]'
    SAVE_BUTTON = 'button:has-text("Save")'

    def fill_employee_details(self, first_name, last_name, employee_id):
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.EMPLOYEE_ID_INPUT, "")
        self.page.fill(self.EMPLOYEE_ID_INPUT, employee_id)
        return self

    def upload_profile_picture(self, file_path):
        self.page.set_input_files(self.PHOTO_INPUT, file_path)
        return self

    def save(self):
        """Submits the form and returns (profile_page, toast_message).

        The success toast auto-dismisses in a few seconds, faster than the
        SPA route change + data fetch it triggers, so it is read straight
        after the click instead of after waiting for navigation to settle.
        """
        import re

        from pages.employee_profile_page import EmployeeProfilePage

        self.page.click(self.SAVE_BUTTON)
        toast = self.page.locator(self.TOAST_MESSAGE).first
        toast.wait_for(state="visible", timeout=8000)
        toast_message = toast.inner_text()
        self.page.wait_for_url(re.compile(r"empNumber/\d+"), timeout=20000)
        return EmployeeProfilePage(self.page), toast_message
