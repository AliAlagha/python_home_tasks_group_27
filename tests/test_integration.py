import pytest

from integration.api_gateway import ApiGateway
from integration.errors import IntegrationError


@pytest.fixture
def gateway():
    gateway = ApiGateway()
    gateway.setup()
    gateway.register("anna", "anna123", "citizen", "Dortmund")
    gateway.register("city", "city123", "municipality", "Dortmund")
    return gateway


def test_scan_is_saved_in_history(gateway):
    token = gateway.login("anna", "anna123")
    recommendation = gateway.scan(token, "biological_peel.jpg", 2)
    assert recommendation.get_category() == "Compostable"
    assert gateway.get_statistics().get_scan_count() == 1


def test_wrong_password_returns_401(gateway):
    with pytest.raises(IntegrationError) as error:
        gateway.login("anna", "wrong")
    assert error.value.status_code == 401


def test_citizen_cannot_open_dashboard(gateway):
    token = gateway.login("anna", "anna123")
    with pytest.raises(IntegrationError) as error:
        gateway.dashboard(token)
    assert error.value.status_code == 403


def test_same_username_twice_returns_409(gateway):
    with pytest.raises(IntegrationError) as error:
        gateway.register("anna", "other123")
    assert error.value.status_code == 409


def test_bad_image_returns_422(gateway):
    token = gateway.login("anna", "anna123")
    with pytest.raises(IntegrationError) as error:
        gateway.scan(token, "notes.txt", 1)
    assert error.value.status_code == 422
