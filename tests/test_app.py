"""
CloudTask - Basic Tests
Phase 4: Jenkins CI/CD

These tests verify that:
1. The Flask app imports and initializes successfully
2. The home route (/) returns a 200 OK status code
"""

import os
import sys
import pytest

# Add the project root directory to Python path
# This allows Jenkins/pytest to find app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    """
    Create a test client for the Flask app.
    TESTING=True disables error catching for better test feedback.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_app_exists():
    """Test that the Flask application object was created successfully."""
    assert app is not None


def test_home_route_returns_200(client):
    """Test that the home page (/) loads and returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200