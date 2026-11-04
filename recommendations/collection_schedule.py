from datetime import date

from .errors import RecommendationError

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class CollectionSchedule:

    def __init__(self, region_name):
        self._region_name = region_name
        self._pickup_days = {}

    def load_default_days(self):
        # pickup day for each bin (example plan for Dortmund)
        self._pickup_days["Yellow bin"] = "Monday"
        self._pickup_days["Blue bin"] = "Tuesday"
        self._pickup_days["Brown bin"] = "Wednesday"
        self._pickup_days["Black bin"] = "Friday"

    # region
    def get_region_name(self):
        return self._region_name

    def set_region_name(self, region_name):
        self._region_name = region_name

    # pickup days
    def get_pickup_days(self):
        return self._pickup_days

    def set_pickup_day(self, bin_name, day):
        if day not in DAYS:
            raise RecommendationError(day + " is not a day")
        self._pickup_days[bin_name] = day

    # functions
    def get_pickup_day(self, bin_name):
        if bin_name in self._pickup_days:
            return self._pickup_days[bin_name]
        # containers and collection points are not picked up from home
        return "no pickup, bring it there yourself"

    def is_pickup_today(self, bin_name):
        today = DAYS[date.today().weekday()]
        return self.get_pickup_day(bin_name) == today

    def show(self):
        print("Collection plan for " + self._region_name + ":")
        for bin_name in self._pickup_days:
            print("  " + bin_name + ": " + self._pickup_days[bin_name])
