import pytest

from history_statistics.dashboard import Dashboard
from history_statistics.errors import StatisticsError
from history_statistics.scan_record import ScanRecord
from history_statistics.statistics_service import StatisticsService
from history_statistics.user import User


@pytest.fixture
def service():
    service = StatisticsService()
    service.add_record(ScanRecord(1, "Dortmund", "Recyclable", "Plastic bottle"))
    service.add_record(ScanRecord(2, "Dortmund", "Compostable", "Banana peel"))
    service.add_record(ScanRecord(3, "Bochum", "Landfill", "Used tissue"))
    service.add_record(ScanRecord(4, "Bochum", "Recyclable", "Soda can"))
    return service


def test_recycle_rate(service):
    df = service.get_dataframe()
    assert service.get_recycle_rate(df) == 50.0


def test_unknown_category_raises_error():
    with pytest.raises(StatisticsError):
        ScanRecord(1, "Dortmund", "Plutonium", "Rod")


def test_dashboard_needs_login(service):
    dashboard = Dashboard(service)
    with pytest.raises(StatisticsError):
        dashboard.filter_data()


def test_wrong_date_filter_raises_error(service):
    dashboard = Dashboard(service)
    with pytest.raises(StatisticsError):
        dashboard.set_date_filter(0)


def test_region_filter(service):
    dashboard = Dashboard(service)
    dashboard.login(User(1, "admin", "secret123"), "secret123")
    dashboard.set_region_filter("Bochum")
    charts = dashboard.show_charts()
    assert charts["waste_composition"] == {"Landfill": 1, "Recyclable": 1}
