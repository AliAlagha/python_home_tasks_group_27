from datetime import datetime


class Recommendation:

    def __init__(self, rule, region_name, pickup_day=""):
        self._rule = rule
        self._region_name = region_name
        self._pickup_day = pickup_day
        self._created_at = datetime.now()

    # rule
    def get_rule(self):
        return self._rule

    def set_rule(self, rule):
        self._rule = rule

    # region
    def get_region_name(self):
        return self._region_name

    def set_region_name(self, region_name):
        self._region_name = region_name

    # pickup day
    def get_pickup_day(self):
        return self._pickup_day

    def set_pickup_day(self, pickup_day):
        self._pickup_day = pickup_day

    # created at (only getter, it should not change)
    def get_created_at(self):
        return self._created_at

    # short cuts so we dont need get_rule() every time
    def get_category(self):
        return self._rule.get_category()

    def get_bin_name(self):
        return self._rule.get_bin_name()

    # functions
    def to_dict(self):
        return {
            "item_name": self._rule.get_item_name(),
            "category": self._rule.get_category(),
            "bin_name": self._rule.get_bin_name(),
            "tip": self._rule.get_tip(),
            "pickup_day": self._pickup_day,
            "region_name": self._region_name,
        }

    def show(self):
        self._rule.show()
        if self._rule.has_tip():
            print("  Tip: " + self._rule.get_tip())
        print("  Pickup: " + self._pickup_day + " (" + self._region_name + ")")
