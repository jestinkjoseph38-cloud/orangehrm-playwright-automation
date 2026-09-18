from pages.base_page import BasePage


class EmployeeListPage(BasePage):
    """PIM > Employee List, the search/manage grid."""

    ADD_EMPLOYEE_TAB = 'a:has-text("Add Employee")'
    EMPLOYEE_ID_FILTER = '.oxd-grid-item:has(label:text("Employee Id")) input'
    SEARCH_BUTTON = 'button:has-text("Search")'
    RESULT_ROWS = ".oxd-table-card"
    ROW_CHECKBOX = ".oxd-table-card .oxd-checkbox-wrapper"
    DELETE_SELECTED_BUTTON = 'button:has-text("Delete Selected")'
    CONFIRM_DELETE_BUTTON = 'button:has-text("Yes, Delete")'
    # Scoped to a <span>: OrangeHRM also raises a "No Records Found" *toast*
    # (a <p>) on an empty search, and a bare text= selector matches both.
    NO_RECORDS_TEXT = 'span.oxd-text--span:has-text("No Records Found")'

    def go_to_add_employee(self):
        from pages.add_employee_page import AddEmployeePage

        self.page.click(self.ADD_EMPLOYEE_TAB)
        self.wait_for_page_load()
        return AddEmployeePage(self.page)

    def search_by_employee_id(self, employee_id):
        """Fills the filter and waits for the underlying list API call to resolve.

        `networkidle` alone is not reliable here: the grid re-renders from
        Vue's reactive state a beat after the response lands, so counting
        rows right after it can race the UI and see the stale/empty grid.
        """
        self.page.fill(self.EMPLOYEE_ID_FILTER, employee_id)
        with self.page.expect_response(lambda r: "/api/v2/pim/employees" in r.url and r.request.method == "GET"):
            self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_timeout(500)
        return self

    def get_result_count(self):
        if self.page.locator(self.NO_RECORDS_TEXT).is_visible():
            return 0
        return self.page.locator(self.RESULT_ROWS).count()

    def open_first_result(self):
        from pages.employee_profile_page import EmployeeProfilePage

        self.page.locator(self.RESULT_ROWS).first.click()
        self.wait_for_page_load()
        return EmployeeProfilePage(self.page)

    def select_first_result(self):
        self.page.locator(self.ROW_CHECKBOX).first.click()
        return self

    def delete_selected(self):
        """Confirms the delete and returns the success toast message."""
        self.page.click(self.DELETE_SELECTED_BUTTON)
        self.page.click(self.CONFIRM_DELETE_BUTTON)
        toast = self.page.locator(self.TOAST_MESSAGE).first
        toast.wait_for(state="visible", timeout=8000)
        return toast.inner_text()
