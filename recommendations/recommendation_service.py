from .collection_schedule import CollectionSchedule
from .errors import RecommendationError
from .recommendation import Recommendation
from .recycling_rule import RecyclingRule


class RecommendationService:

    def __init__(self, region_name="Dortmund"):
        self._region_name = region_name
        self._rules = {}
        self._schedule = CollectionSchedule(region_name)
        self._history = []

    def load_rules(self):
        # rules for Dortmund, other cities can come later
        self.add_rule(RecyclingRule("plastic", "Recyclable", "Yellow bin", "Empty the bottle first"))
        self.add_rule(RecyclingRule("metal", "Recyclable", "Yellow bin", "Rinse the can"))
        self.add_rule(RecyclingRule("paper", "Recyclable", "Blue bin"))
        self.add_rule(RecyclingRule("cardboard", "Recyclable", "Blue bin", "Flatten the box"))
        self.add_rule(RecyclingRule("glass", "Recyclable", "Glass container", "Remove the lid"))
        self.add_rule(RecyclingRule("clothes", "Recyclable", "Clothes container"))
        self.add_rule(RecyclingRule("shoes", "Recyclable", "Clothes container"))
        self.add_rule(RecyclingRule("biological", "Compostable", "Brown bin", "No plastic bags"))
        self.add_rule(RecyclingRule("battery", "Landfill", "Battery collection point"))
        self.add_rule(RecyclingRule("trash", "Landfill", "Black bin"))
        self._schedule.load_default_days()

    # region
    def get_region_name(self):
        return self._region_name

    def set_region_name(self, region_name):
        self._region_name = region_name
        self._schedule.set_region_name(region_name)

    # rules, schedule and history (only getters)
    def get_rules(self):
        return self._rules

    def get_schedule(self):
        return self._schedule

    def get_history(self):
        return self._history

    # functions
    def add_rule(self, rule):
        self._rules[rule.get_item_name()] = rule

    def remove_rule(self, item_name):
        if item_name in self._rules:
            del self._rules[item_name]

    def get_rule_count(self):
        return len(self._rules)

    def find_rules_by_category(self, category):
        found = []
        for item_name in self._rules:
            if self._rules[item_name].get_category() == category:
                found.append(self._rules[item_name])
        return found

    def recommend(self, result):
        if len(self._rules) == 0:
            raise RecommendationError("no rules loaded for " + self._region_name)
        item = result.get_item_name()
        # AI not sure or item unknown -> black bin is the safe choice
        if not result.is_certain() or item not in self._rules:
            rule = RecyclingRule(item, "Landfill", "Black bin", "Not sure? ask your local waste authority")
        else:
            rule = self._rules[item]
        pickup_day = self._schedule.get_pickup_day(rule.get_bin_name())
        recommendation = Recommendation(rule, self._region_name, pickup_day)
        self._history.append(recommendation)
        return recommendation
