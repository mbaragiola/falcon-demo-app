import json
import falcon
import pytest

from falcon import testing

from kanda.app import app


@pytest.fixture
def client():
    return testing.TestClient(app)


def test_successful(client):
    """
    Should create a new user and return 201.
    """
    params = {
        "first_name": "Mariano",
        "last_name": "Baragiola",
        "email": "mbaragiola@linux.com",
        "password": "valid_password1",
    }

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_201


def test_blank(client):
    """
    Should return 400 with all errors.
    """
    params = {}

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_400

    content = json.loads(response.content.decode("utf-8"))
    assert content["error"] == "Bad request"
    assert content["field_errors"]["first_name"][0] == "Missing data for required field."
    assert content["field_errors"]["last_name"][0] == "Missing data for required field."
    assert content["field_errors"]["email"][0] == "Missing data for required field."
    assert content["field_errors"]["password"][0] == "Missing data for required field."


def test_blank_everything_except_password(client):
    """
    Should return 400 with all errors except password.
    """
    params = {"password": "valid_password1"}

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_400

    content = json.loads(response.content.decode("utf-8"))
    assert content["error"] == "Bad request"
    assert content["field_errors"]["first_name"][0] == "Missing data for required field."
    assert content["field_errors"]["last_name"][0] == "Missing data for required field."
    assert content["field_errors"]["email"][0] == "Missing data for required field."


def test_wrong_first_name(client):
    """
    Should return 400 with error msg for first_name.
    """
    params = {
        "first_name": 1,
        "last_name": "Baragiola",
        "email": "mbaragiola@linux.com",
        "password": "valid_password1",
    }

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_400

    content = json.loads(response.content.decode("utf-8"))
    assert content["error"] == "Bad request"
    assert content["field_errors"]["first_name"][0] == "Invalid field type"


def test_short_password(client):
    """
    Should return 400 with error msg for short password.
    """
    params = {
        "first_name": "Mariano",
        "last_name": "Baragiola",
        "email": "mbaragiola@linux.com",
        "password": "a",
    }

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_400

    content = json.loads(response.content.decode("utf-8"))
    assert content["error"] == "Bad request"
    assert content["field_errors"]["password"][0] == "Password must at least be 8 characters"


def test_invalid_email(client):
    """
    Should return 400 with error msg for invalid email.
    """
    params = {
        "first_name": "Mariano",
        "last_name": "Baragiola",
        "email": "m@l.c",
        "password": "valid_password1",
    }

    response = client.simulate_post("/signup", params=params)

    assert response.status == falcon.HTTP_400

    content = json.loads(response.content.decode("utf-8"))
    assert content["error"] == "Bad request"
    assert content["field_errors"]["email"][0] == "Not a valid email address."
