from fastapi.testclient import TestClient
from endpoints import app


client = TestClient(app)

# We can thread that as E2E tests for our application

# TODO(rkesik): make stubs for internal layers (repo, sercices/utils)
# TODO(rkesik): compose 2 test suits for each endpoint
# TODO(rkesik): mock only external resources...


# Realtime endpoints tests
def test_succesfully_get__connected_realtime_endpoint():
    response = client.get("/connected/realtime")
    assert response.status_code == 200
    assert response.json() == {}  # TODO(rkesik): ..finish that


def test_succesfully_get_and_already_register_exists__connected_realtime_endpoint():
    assert 1 == 2
    ...


def test_external_api_error__connected_realtime_endpoint():
    assert 1 == 2
    ...


def test_errors__connected_realtime_endpoint():
    assert 1 == 2
    ...


# Register endpoints tests
def test_get_with_success__connected_register_endpoint():
    response = client.get("/connected/register")
    assert response.status_code == 200
    assert response.json() == {}  # TODO(rkesik): ...finish that


def test_missing_entry_in_database__connected_register_endpoint():
    assert 1 == 2
    ...


def test_errors__connected_register_endpoint():
    assert 1 == 2
    ...


def test_missing_entry_in_database__connected_register_endpoint():
    assert 1 == 2
    ...


def test_external_api_error__connected_register_endpoint():
    assert 1 == 2
    ...