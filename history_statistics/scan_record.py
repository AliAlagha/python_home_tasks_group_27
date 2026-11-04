from datetime import date

CATEGORIES = ["Recyclable", "Compostable", "Landfill"]


class ScanRecord:
    def __init__(self, scan_id, region_name, category, item_name, scan_date=None):
        self._scan_id = scan_id
        self._region_name = region_name
        self._category = category
        self._item_name = item_name
        # no date given means the scan is from today
        if scan_date is None:
            scan_date = date.today()
        self._scan_date = scan_date

    # getters and setters

    def get_scan_id(self):
        return self._scan_id

    def get_region_name(self):
        return self._region_name

    def set_region_name(self, region_name):
        self._region_name = region_name

    def get_category(self):
        return self._category

    def set_category(self, category):
        if category not in CATEGORIES:
            print("Unknown category:", category)
            return
        self._category = category

    def get_item_name(self):
        return self._item_name

    def set_item_name(self, item_name):
        self._item_name = item_name

    def get_scan_date(self):
        return self._scan_date

    def set_scan_date(self, scan_date):
        self._scan_date = scan_date

    # methods

    def is_recyclable(self):
        return self._category == "Recyclable"

    def is_from_today(self):
        return self._scan_date == date.today()

    def to_dict(self):
        return {
            "scan_id": self._scan_id,
            "region_name": self._region_name,
            "category": self._category,
            "item_name": self._item_name,
            "scan_date": self._scan_date,
        }

    def show(self):
        print(self._scan_date, "|", self._region_name, "|", self._item_name, "|", self._category)
