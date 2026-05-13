"""
Pytest configuration and fixtures for test isolation.
Uses monkeypatch to reset activities dictionary before each test.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module


# Sample activities dictionary for test reset
SAMPLE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@pytest.fixture
def client(monkeypatch):
    """
    Arrange: Initialize TestClient with clean test data.
    Uses monkeypatch to ensure test isolation by resetting activities to sample data.
    """
    # Reset activities to a deep copy for test isolation (nested participants lists)
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(SAMPLE_ACTIVITIES))
    return TestClient(app)
