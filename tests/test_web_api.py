import pymysql
import pytest

from web_api.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_page_shows_scans(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Plastic bottle" in response.data


def test_api_returns_all_scans(client):
    response = client.get("/api/scans")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_api_returns_one_scan(client):
    response = client.get("/api/scans/1")
    assert response.status_code == 200
    assert response.get_json()["item_name"] == "Plastic bottle"


def test_api_unknown_scan_returns_404(client):
    response = client.get("/api/scans/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "scan not found"


def test_unknown_page_returns_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["error"] == "page not found"


def test_database_down_returns_503(client, monkeypatch):
    def broken_connect(**kwargs):
        raise pymysql.MySQLError("connection refused")

    monkeypatch.setattr(pymysql, "connect", broken_connect)
    response = client.get("/api/scans")
    assert response.status_code == 503
    assert response.get_json()["error"] == "database is not available"


def test_api_filters_scans_by_region(client):
    response = client.get("/api/scans?region=Bochum")
    assert response.status_code == 200
    assert {scan["region_name"] for scan in response.get_json()} == {"Bochum"}


def test_api_statistics(client):
    response = client.get("/api/statistics")
    assert response.status_code == 200
    assert response.get_json()["recycling_rate"] == 60.0
