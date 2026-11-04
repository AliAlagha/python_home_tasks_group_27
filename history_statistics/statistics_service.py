import pandas as pd

from .scan_record import ScanRecord

COLUMNS = ["scan_id", "region_name", "category", "item_name", "scan_date"]


class StatisticsService:
    def __init__(self):
        self._records = []

    def load_records(self, rows):
        # rows come from the database as dicts
        for row in rows:
            record = ScanRecord(row["scan_id"], row["region_name"], row["category"],
                                row["item_name"], row["scan_date"])
            self.add_record(record)

    # getters and setters

    def get_records(self):
        return self._records

    def set_records(self, records):
        self._records = records

    def get_scan_count(self):
        return len(self._records)

    # methods

    def add_record(self, record):
        self._records.append(record)

    def clear(self):
        self._records = []

    def get_records_by_region(self, region_name):
        found = []
        for record in self._records:
            if record.get_region_name() == region_name:
                found.append(record)
        return found

    def get_regions(self):
        regions = []
        for record in self._records:
            if record.get_region_name() not in regions:
                regions.append(record.get_region_name())
        return regions

    # pandas makes the counting much easier than loops
    def get_dataframe(self):
        df = pd.DataFrame([r.to_dict() for r in self._records], columns=COLUMNS)
        df["scan_date"] = pd.to_datetime(df["scan_date"])
        return df

    def get_totals(self, df):
        return df["category"].value_counts().to_dict()

    def get_recycle_rate(self, df):
        if len(df) == 0:
            return 0
        recyclable = len(df[df["category"] == "Recyclable"])
        return round(recyclable / len(df) * 100, 1)

    def get_most_common_items(self, df, n=5):
        return df["item_name"].value_counts().head(n).to_dict()

    def show_history(self):
        for record in self._records:
            record.show()
