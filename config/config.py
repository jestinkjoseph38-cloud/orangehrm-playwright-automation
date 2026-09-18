class Config:
    BASE_URL = "https://opensource-demo.orangehrmlive.com"
    LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
    EMPLOYEE_LIST_URL = f"{BASE_URL}/web/index.php/pim/viewEmployeeList"

    VALID_USERNAME = "Admin"
    VALID_PASSWORD = "admin123"

    DEFAULT_TIMEOUT = 15000
