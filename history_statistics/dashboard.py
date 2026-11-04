from datetime import date, timedelta

import pandas as pd


class Dashboard:
    def __init__(self, service, region_filter="All", date_filter=30):
        self._service = service
        self._region_filter = region_filter
        self._date_filter = date_filter
        self._user = None

    def reset_filters(self):
        self._region_filter = "All"
        self._date_filter = 30

    # getters and setters

    def get_region_filter(self):
        return self._region_filter

    def set_region_filter(self, region_filter):
        self._region_filter = region_filter

    def get_date_filter(self):
        return self._date_filter

    def set_date_filter(self, days):
        if days <= 0:
            print("Date filter must be more than 0 days")
            return
        self._date_filter = days

    def get_user(self):
        return self._user

    # methods

    def login(self, user, password):
        if user.check_password(password):
            self._user = user
            user.update_last_login()
            return True
        return False

    def logout(self):
        self._user = None

    def is_logged_in(self):
        return self._user is not None

    def filter_data(self):
        if not self.is_logged_in():
            print("Please log in first")
            return None
        df = self._service.get_dataframe()
        # keep only the scans of the last x days
        start = pd.Timestamp(date.today() - timedelta(days=self._date_filter))
        df = df[df["scan_date"] >= start]
        if self._region_filter != "All":
            df = df[df["region_name"] == self._region_filter]
        return df

    def show_charts(self):
        df = self.filter_data()
        if df is None:
            return None
        return {
            "waste_composition": self._service.get_totals(df),
            "recycling_rate": self._service.get_recycle_rate(df),
            "most_common_items": self._service.get_most_common_items(df),
        }

    def export_csv(self, path):
        df = self.filter_data()
        if df is not None:
            df.to_csv(path, index=False)
