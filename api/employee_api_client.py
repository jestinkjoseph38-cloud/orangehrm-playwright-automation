import json

from config.config import Config


class EmployeeAPIClient:
    """Thin wrapper around OrangeHRM's internal REST API (api/v2/pim/employees).

    Reuses the session cookie created by the UI login (via Playwright's
    request context, which shares cookies with the browser context) so the
    same authenticated session drives both the UI actions and the API checks.
    """

    EMPLOYEES_ENDPOINT = f"{Config.BASE_URL}/web/index.php/api/v2/pim/employees"

    def __init__(self, request_context):
        self.request = request_context

    def find_employee_by_employee_id(self, employee_id):
        params = {
            "limit": 50,
            "offset": 0,
            "model": "detailed",
            "employeeId": employee_id,
            "includeEmployees": "onlyCurrent",
            "sortField": "employee.firstName",
            "sortOrder": "ASC",
        }
        response = self.request.get(self.EMPLOYEES_ENDPOINT, params=params)
        assert response.ok, f"GET {self.EMPLOYEES_ENDPOINT} failed with status {response.status}"
        body = response.json()
        records = body.get("data", [])
        return records[0] if records else None

    def get_job_details(self, employee_number):
        url = f"{self.EMPLOYEES_ENDPOINT}/{employee_number}/job-details"
        response = self.request.get(url)
        assert response.ok, f"GET {url} failed with status {response.status}"
        return response.json().get("data", {})

    def delete_employee(self, employee_number):
        response = self.request.delete(
            self.EMPLOYEES_ENDPOINT,
            data=json.dumps({"ids": [int(employee_number)]}),
            headers={"Content-Type": "application/json"},
        )
        assert response.ok, f"DELETE {self.EMPLOYEES_ENDPOINT} failed with status {response.status}"
        return response.json()
