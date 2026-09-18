import json
import time

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Force video recording + a stable viewport for every test, regardless of CLI flags."""
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720},
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def employee_data():
    """Loads the data-driven employee fixture and stamps a unique Employee ID.

    A unique suffix is appended on every run because the target site is a
    shared public demo instance - a hardcoded ID would eventually collide
    with a record created by another user/run.
    """
    with open("data/employee_data.json") as f:
        data = json.load(f)

    unique_suffix = str(int(time.time() * 1000))[-8:]
    data["employeeId"] = f"{data['employeeIdPrefix']}{unique_suffix}"
    return data
