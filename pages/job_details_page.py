from pages.base_page import BasePage


class JobDetailsPage(BasePage):
    """Job tab within an employee's profile - Job Title / Employment Status."""

    JOB_TITLE_DROPDOWN = '.oxd-grid-item:has(label:text("Job Title")) .oxd-select-text'
    EMPLOYMENT_STATUS_DROPDOWN = '.oxd-grid-item:has(label:text("Employment Status")) .oxd-select-text'
    DROPDOWN_OPTION = ".oxd-select-dropdown .oxd-select-option"
    SAVE_BUTTON = 'button:has-text("Save")'

    def _choose_dropdown_option(self, dropdown_selector, option_text):
        self.page.click(dropdown_selector)
        self.page.locator(self.DROPDOWN_OPTION).filter(has_text=option_text).first.click()
        return self

    def update_job_title(self, job_title):
        return self._choose_dropdown_option(self.JOB_TITLE_DROPDOWN, job_title)

    def update_employment_status(self, employment_status):
        return self._choose_dropdown_option(self.EMPLOYMENT_STATUS_DROPDOWN, employment_status)

    def save(self):
        """Submits the Job tab and returns the success toast message."""
        self.page.click(self.SAVE_BUTTON)
        toast = self.page.locator(self.TOAST_MESSAGE).first
        toast.wait_for(state="visible", timeout=8000)
        return toast.inner_text()

    def get_job_title_value(self):
        return self.page.locator(self.JOB_TITLE_DROPDOWN).inner_text()

    def get_employment_status_value(self):
        return self.page.locator(self.EMPLOYMENT_STATUS_DROPDOWN).inner_text()
