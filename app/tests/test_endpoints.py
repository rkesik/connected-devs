from fastapi.testclient import TestClient
from endpoints import app


client = TestClient(app)

# We can thread that as E2E tests for our application

# TODO(rkesik): make stubs for internal layers (repos)
# TODO(rkesik): compose 2 test suits for each endpoint
# TODO(rkesik): mock only external resources...


class TestRealtimeEndpoint:
    def test_succesfully_get(self):
        handleone = "xxx"
        handletwo = "yyy"
        response = client.get(f"/connected/realtime/{handleone}/{handletwo}")
        assert response.status_code == 200
        assert response.json() == {}  # TODO(rkesik): ..finish that


    def test_succesfully_get_and_already_register_exists(self):
        assert 1 == 2
        ...


    def test_external_api_error__connected_realtime_endpoint(self):
        assert 1 == 2
        ...


    def test_errors__connected_realtime_endpoint(self):
        assert 1 == 2
        ...

class TestRegisterEndpoint:
    def setUp(self):
        self.url_pattern = "/connected/register/{}/{}"
        self.url = self.url_pattern.format('rkesik', 'rkesik')

    def test_get_with_success(self):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json() == {}  # TODO(rkesik): ...finish that

    def test_missing_entry_in_database(self):
        assert 1 == 2
        ...

    def test_errors(self):
        assert 1 == 2
        ...

    def test_missing_entry_in_database(self):
        assert 1 == 2
        ...


    def test_external_api_error(self):
        assert 1 == 2
        ...
