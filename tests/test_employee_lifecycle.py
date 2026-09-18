import logging
import os

import pytest

from api.employee_api_client import EmployeeAPIClient
from config.config import Config
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.mark.e2e
def test_employee_lifecycle(page, employee_data):
    """End-to-end: login -> add employee -> edit -> validate via API -> delete -> logout.

    Each step's outcome is checked both through the UI (toast / grid state)
    and, where the scenario calls for it, cross-checked against OrangeHRM's
    own internal REST API (api/v2/pim/employees) to prove UI and backend
    state agree.
    """
    profile_picture = os.path.join(os.path.dirname(__file__), "..", "data", "profile_picture.png")
    api = EmployeeAPIClient(page.request)

    # ---------------------------------------------------------------
    # 1. Login
    # ---------------------------------------------------------------
    logger.info("STEP 1: Logging in as %s", Config.VALID_USERNAME)
    login_page = LoginPage(page).open()
    dashboard = login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    assert dashboard.is_loaded(), "Dashboard did not become visible after a valid login"
    assert dashboard.get_header_text() == "Dashboard", "Expected the 'Dashboard' module header after login"

    # ---------------------------------------------------------------
    # 2. Add a new employee (data-driven, with a profile picture)
    # ---------------------------------------------------------------
    logger.info("STEP 2: Adding employee %s %s (ID %s)", employee_data["firstName"], employee_data["lastName"], employee_data["employeeId"])
    add_employee_page = dashboard.go_to_pim().go_to_add_employee()
    add_employee_page.fill_employee_details(
        employee_data["firstName"], employee_data["lastName"], employee_data["employeeId"]
    ).upload_profile_picture(profile_picture)

    employee_profile, save_toast = add_employee_page.save()
    assert "Success" in save_toast, f"Expected a success toast after adding the employee, got: '{save_toast}'"

    employee_number = employee_profile.get_employee_number()
    assert employee_number is not None, "Could not extract the new employee's empNumber from the URL"

    employee_profile.wait_for_page_load()
    full_name = employee_profile.get_full_name()
    assert full_name == f"{employee_data['firstName']} {employee_data['lastName']}", (
        f"Employee name on the profile page ('{full_name}') does not match the submitted data"
    )

    # ---------------------------------------------------------------
    # 3. Edit employee information (search by Employee ID, update Job tab)
    # ---------------------------------------------------------------
    logger.info("STEP 3: Searching for employee ID %s and updating job details", employee_data["employeeId"])
    employee_list = employee_profile.go_to_pim()
    employee_list.search_by_employee_id(employee_data["employeeId"])

    assert employee_list.get_result_count() == 1, (
        f"Expected exactly 1 search result for Employee ID '{employee_data['employeeId']}'"
    )

    job_details = employee_list.open_first_result().go_to_job_tab()
    job_details.update_job_title(employee_data["updatedJobTitle"])
    job_details.update_employment_status(employee_data["updatedEmploymentStatus"])
    update_toast = job_details.save()

    assert "Success" in update_toast, f"Expected a success toast after updating job details, got: '{update_toast}'"

    # ---------------------------------------------------------------
    # 4. Validate the employee via the OrangeHRM API and cross-check with the UI
    # ---------------------------------------------------------------
    logger.info("STEP 4: Cross-checking employee %s against the OrangeHRM API", employee_number)
    api_employee = api.find_employee_by_employee_id(employee_data["employeeId"])
    assert api_employee is not None, f"API returned no employee for Employee ID '{employee_data['employeeId']}'"
    assert str(api_employee["empNumber"]) == employee_number, "API empNumber does not match the UI empNumber"
    assert api_employee["firstName"] == employee_data["firstName"], "API firstName does not match the UI value"
    assert api_employee["lastName"] == employee_data["lastName"], "API lastName does not match the UI value"

    api_job_details = api.get_job_details(employee_number)
    assert api_job_details["jobTitle"]["title"] == employee_data["updatedJobTitle"], (
        "API job title does not match the value saved through the UI"
    )
    assert api_job_details["empStatus"]["name"] == employee_data["updatedEmploymentStatus"], (
        "API employment status does not match the value saved through the UI"
    )

    # ---------------------------------------------------------------
    # 5. Delete the employee via the UI, verify via both UI and API
    # ---------------------------------------------------------------
    logger.info("STEP 5: Deleting employee %s via the UI", employee_number)
    employee_list = job_details.go_to_pim()
    employee_list.search_by_employee_id(employee_data["employeeId"])
    employee_list.select_first_result()
    delete_toast = employee_list.delete_selected()

    assert "Success" in delete_toast, f"Expected a success toast after deleting the employee, got: '{delete_toast}'"

    employee_list.wait_for_page_load()
    employee_list.search_by_employee_id(employee_data["employeeId"])
    assert employee_list.get_result_count() == 0, "Deleted employee is still present in the UI search results"

    deleted_api_employee = api.find_employee_by_employee_id(employee_data["employeeId"])
    assert deleted_api_employee is None, "Deleted employee is still returned by the API"

    # ---------------------------------------------------------------
    # 6. Logout and confirm the session is invalidated
    # ---------------------------------------------------------------
    logger.info("STEP 6: Logging out")
    login_page = employee_list.logout()
    assert login_page.is_on_login_page(), "Logout did not return the user to the login page"

    page.goto(Config.EMPLOYEE_LIST_URL)
    page.wait_for_load_state("networkidle")
    assert "/auth/login" in page.url, "A protected page was reachable after logout - session was not invalidated"
