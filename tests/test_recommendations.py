from datetime import date

import pytest

from classification.classification_result import ClassificationResult
import json

from recommendations.collection_schedule import CollectionSchedule
from recommendations.edg_calendar import EdgCalendar, normalize_street, parse_ics, rhythm_weeks
from recommendations.errors import RecommendationError
from recommendations.recommendation_service import RecommendationService
from recommendations.recycling_rule import RecyclingRule


@pytest.fixture
def service():
    service = RecommendationService("Dortmund")
    service.load_rules()
    return service


def test_plastic_goes_to_yellow_bin(service):
    recommendation = service.recommend(ClassificationResult("plastic", 0.9))
    assert recommendation.get_rule().get_bin_name() == "Yellow bin"


def test_uncertain_result_goes_to_grey_bin(service):
    recommendation = service.recommend(ClassificationResult("plastic", 0.3))
    assert recommendation.get_rule().get_bin_name() == "Grey bin"


def test_unknown_category_raises_error():
    with pytest.raises(RecommendationError):
        RecyclingRule("pizza box", "Burnable", "Grey bin")


def test_recommend_without_rules_raises_error():
    with pytest.raises(RecommendationError):
        RecommendationService().recommend(ClassificationResult("plastic", 0.9))


def test_without_address_only_the_rhythm_is_known(service):
    recommendation = service.recommend(ClassificationResult("plastic", 0.9))
    assert recommendation.get_pickup_day() == "depends on your address"
    assert recommendation.get_rhythm() == "every 2 weeks"
    assert recommendation.get_next_pickup() is None


def test_wrong_pickup_day_raises_error(service):
    with pytest.raises(RecommendationError):
        service.get_schedule().set_pickup_day("Yellow bin", "Funday")


def test_unknown_item_goes_to_grey_bin(service):
    recommendation = service.recommend(ClassificationResult("pizza box", 0.95))
    assert recommendation.get_bin_name() == "Grey bin"
    assert recommendation.get_rule().has_tip()


def test_recommend_needs_classification_result(service):
    with pytest.raises(RecommendationError):
        service.recommend("plastic")
    with pytest.raises(RecommendationError):
        service.recommend(None)


def test_remove_unknown_rule_raises_error(service):
    with pytest.raises(RecommendationError):
        service.remove_rule("pizza box")


def test_battery_is_not_put_in_a_bin(service):
    recommendation = service.recommend(ClassificationResult("battery", 0.9))
    assert recommendation.get_bin_name() == "Battery collection point"
    assert recommendation.get_pickup_day() == "no pickup, bring it there yourself"


def test_recommendations_are_saved_in_history(service):
    service.recommend(ClassificationResult("paper", 0.9))
    service.recommend(ClassificationResult("metal", 0.9))
    assert len(service.get_history()) == 2
    assert len(service.find_rules_by_category("Compostable")) == 1


# ----- EDG calendar of one address (no internet needed: FakeEdg plays the EDG website) -----

# same format as a real EDG calendar; Wertstoffe on 5 Dec is a Saturday (holiday shift)
EDG_ICS = "\r\n".join(["BEGIN:VCALENDAR"] + [
    "BEGIN:VEVENT\r\nDTSTART;VALUE=DATE:" + day + "\r\nSUMMARY;LANGUAGE=de:" + title + "\r\nEND:VEVENT"
    for day, title in [
        ("20261103", "Restabfall 1100 l 01-wöchentl."), ("20261110", "Restabfall 1100 l 01-wöchentl."),
        ("20261106", "Wertstoffe 1100 l 02-wöchentl."), ("20261120", "Wertstoffe 1100 l 02-wöchentl."),
        ("20261205", "Wertstoffe 1100 l 02-wöchentl."),
        ("20261113", "Bioabfall 240 l 02-wöchentl."), ("20261127", "Bioabfall 240 l 02-wöchentl."),
        ("20261110", "Altpapier 1100 l 04-wöchentl."), ("20261208", "Altpapier 1100 l 04-wöchentl."),
    ]] + ["END:VCALENDAR"])

FORM_PAGE = """<form><input type="hidden" name="SessionId" value="abc">
<select name="Ort"><option value="" selected></option><option value="S">S</option></select>
<select name="Strasse"><option value="" selected></option></select>
<select name="Hausnummer"><option value="" selected></option></select></form>"""
RESULT_PAGE = '<a href="WasteManagementServiceServlet?ApplicationName=Calendar&amp;SubmitAction=sync&amp;StandortID=1&amp;AboID=2">URL</a>'


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


class FakeEdg:
    def __init__(self):
        self.steps = []

    def get(self, url, params=None, headers=None, timeout=None):
        if "StandortID=1&AboID=2" in url:
            self.steps.append("calendar")
            return FakeResponse(EDG_ICS)
        self.steps.append("form")
        return FakeResponse(FORM_PAGE)

    def post(self, url, data=None, files=None, headers=None, timeout=None):
        if files is not None:
            self.steps.append("forward " + files["Strasse"][1] + " " + files["Hausnummer"][1])
            return FakeResponse(RESULT_PAGE)
        fields = dict(pair.split("=", 1) for pair in data.decode("utf-8").split("&"))
        self.steps.append(fields["SubmitAction"])
        if fields["SubmitAction"] == "CITYCHANGED":
            items = [{"item": "Schwanenwall"}, {"item": "Sonnenstr."}]
            return FakeResponse(json.dumps({"Response": {"values": [{"name": "Strasse", "items": items}]}}))
        items = [{"item": "94"}, {"item": "96"}, {"item": "96 a"}]
        return FakeResponse(json.dumps({"Response": {"values": [{"name": "Hausnummer", "items": items}]}}))


class FakeEdgNoBrown(FakeEdg):
    # an address without a brown bin: the calendar has no "Bioabfall" dates
    def get(self, url, params=None, headers=None, timeout=None):
        response = super().get(url, params, headers, timeout)
        if "StandortID" in url:
            events = response.text.split("BEGIN:VEVENT")
            kept = [e for e in events if "Bioabfall" not in e]
            response = FakeResponse("BEGIN:VEVENT".join(kept) + "\r\nEND:VCALENDAR")
        return response


def test_edg_helpers():
    assert normalize_street("Sonnenstraße") == normalize_street("Sonnenstr.")
    assert rhythm_weeks("Altpapier 1100 l 04-wöchentl.") == 4
    assert len(parse_ics(EDG_ICS)) == 9


def test_edg_form_is_filled_step_by_step():
    edg = FakeEdg()
    EdgCalendar(session=edg).fetch_ics("Sonnenstraße", "96")
    assert edg.steps == ["form", "CITYCHANGED", "STREETCHANGED", "forward Sonnenstr. 96", "calendar"]


def test_address_gives_real_days_and_rhythm(service):
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdg()))
    schedule = service.get_schedule()
    assert schedule.get_pickup_day("Grey bin") == "Tuesday"
    assert schedule.get_rhythm_text("Grey bin") == "every week"
    assert schedule.get_pickup_day("Blue bin") == "Tuesday"
    assert schedule.get_rhythm_text("Blue bin") == "every 4 weeks"
    assert schedule.get_pickup_day("Yellow bin") == "Friday"   # not the Saturday of the holiday week


def test_next_pickup_uses_edg_dates(service):
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdg()))
    schedule = service.get_schedule()
    today = date(2026, 11, 5)
    assert schedule.get_next_pickup("Yellow bin", today) == date(2026, 11, 6)
    assert schedule.get_next_pickup("Brown bin", today) == date(2026, 11, 13)
    # the holiday shift from the EDG calendar is kept (Saturday instead of Friday)
    assert schedule.get_next_pickup("Yellow bin", date(2026, 11, 21)) == date(2026, 12, 5)


def test_next_pickup_after_last_edg_date_is_calculated(service):
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdg()))
    assert service.get_schedule().get_next_pickup("Blue bin", date(2026, 12, 9)) == date(2027, 1, 5)


def test_recommendation_shows_next_pickup(service):
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdg()))
    recommendation = service.recommend(ClassificationResult("plastic", 0.9))
    assert recommendation.get_pickup_day() == "Friday"
    assert recommendation.get_rhythm() == "every 2 weeks"


def test_unknown_street_raises_error():
    with pytest.raises(RecommendationError):
        EdgCalendar(session=FakeEdg()).fetch_ics("Nostreet", "1")


def test_house_number_with_letter_is_found():
    edg = FakeEdg()
    EdgCalendar(session=edg).fetch_ics("Sonnenstraße", "96 A")
    assert "forward Sonnenstr. 96 a" in edg.steps


def test_house_number_inside_a_range_is_found():
    from recommendations.edg_calendar import pick_house_number
    assert pick_house_number("38", ["29 -39", "41"]) == ["29 -39"]
    assert pick_house_number("38", ["38 a", "29 -39"]) == ["38 a"]
    assert pick_house_number("40", ["29 -39", "41"]) == []


def test_bin_without_edg_dates_is_not_collected(service):
    # like Sonnenstr. 96 on the EDG website: only grey and yellow bins
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdgNoBrown()))
    assert service.get_schedule().get_pickup_day("Brown bin") == "not collected at this address"
    assert service.get_schedule().get_next_pickup("Brown bin") is None


def test_house_number_with_letters_never_picks_another_building():
    from recommendations.edg_calendar import pick_house_number
    numbers = ["2", "2 a", "2 b - 2 c", "4"]
    assert pick_house_number("2 b-2c", numbers) == ["2 b - 2 c"]
    assert pick_house_number("2b", numbers) == ["2 b - 2 c"]
    assert pick_house_number("2 d", numbers) == []          # not silently "2"


def test_streets_with_roman_numbers():
    from recommendations.edg_calendar import street_letter
    assert street_letter("I. Bickestr.") == "I."
    assert street_letter("II. Rosenterrasse") == "II."
    assert street_letter("Ährenweg") == "Ä"


def test_unknown_house_number_raises_error():
    with pytest.raises(RecommendationError):
        EdgCalendar(session=FakeEdg()).fetch_ics("Sonnenstraße", "7")


def test_container_has_no_next_pickup(service):
    assert service.get_schedule().get_next_pickup("Glass container") is None


def test_wrong_rhythm_raises_error():
    with pytest.raises(RecommendationError):
        CollectionSchedule("Dortmund").set_plan("Grey bin", date(2026, 11, 3), 0)


# ----- whole app: every user gets the dates of their own address -----
def test_scan_uses_the_address_of_the_user():
    from integration.api_gateway import ApiGateway
    gateway = ApiGateway()
    gateway.setup()
    gateway.get_recommendations().set_calendar(EdgCalendar(session=FakeEdg()))
    gateway.register("anna", "anna123", "citizen", "Dortmund", "Sonnenstraße", "96")
    gateway.register("ben", "ben123", "citizen", "Dortmund")          # no address
    anna = gateway.scan(gateway.login("anna", "anna123"), "plastic_bottle.jpg", 2)
    ben = gateway.scan(gateway.login("ben", "ben123"), "plastic_bottle.jpg", 2)
    assert anna.get_pickup_day() == "Friday"
    assert ben.get_pickup_day() == "depends on your address"


def test_scan_still_works_when_edg_is_down(service):
    class BrokenEdg(FakeEdg):
        def get(self, url, params=None, headers=None, timeout=None):
            import requests
            raise requests.ConnectionError("no internet")
    service.set_calendar(EdgCalendar(session=BrokenEdg()))
    recommendation = service.recommend(ClassificationResult("plastic", 0.9), "Sonnenstraße", "96")
    assert recommendation.get_bin_name() == "Yellow bin"
    assert recommendation.get_pickup_day() == "depends on your address"


# like Kampstr. 1 on the EDG website: several bins of the same kind with different days
KAMPSTR_ICS = "\r\n".join(["BEGIN:VCALENDAR"] + [
    "BEGIN:VEVENT\r\nDTSTART;VALUE=DATE:" + day + "\r\nSUMMARY;LANGUAGE=de:" + title + "\r\nEND:VEVENT"
    for title, days in [
        ("Restabfall 1100 l 01-wöchentl.", ["20261109", "20261116", "20261123"]),
        ("Restabfall 60 l 01-wöchentl.", ["20261106", "20261113", "20261120"]),
        ("Restabfall 1100 l 02-wöchentl.", ["20261109", "20261123", "20261207"]),
        ("Bioabfall 240 l 02-wöchentl.", ["20261112", "20261126", "20261210"]),
        ("Altpapier 1100 l 02-wöchentl.", ["20261117", "20261201", "20261215"]),
        ("Altpapier 1100 l 04-wöchentl.", ["20261110", "20261208"]),
        ("Wertstoffe 1100 l 02-wöchentl.", ["20261111", "20261125", "20261209"]),
    ] for day in days] + ["END:VCALENDAR"])


class FakeEdgKampstr(FakeEdg):
    def get(self, url, params=None, headers=None, timeout=None):
        response = super().get(url, params, headers, timeout)
        if "StandortID" in url:
            response = FakeResponse(KAMPSTR_ICS)
        return response


def test_several_bins_of_the_same_kind(service):
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=FakeEdgKampstr()))
    schedule = service.get_schedule()
    today = date(2026, 11, 5)
    assert schedule.get_pickup_day("Grey bin") == "Monday and Friday"
    assert schedule.get_rhythm_text("Grey bin") == "every week"
    assert schedule.get_next_pickup("Grey bin", today) == date(2026, 11, 6)
    assert schedule.get_pickup_day("Blue bin") == "Tuesday"
    assert schedule.get_rhythm_text("Blue bin") == "every 2 weeks"
    assert schedule.get_next_pickup("Blue bin", today) == date(2026, 11, 10)
    assert len(schedule.get_containers("Grey bin")) == 3
    # after the last EDG date the earliest of all grey bins is calculated (Monday 21.12, not Friday 25.12)
    assert schedule.get_next_pickup("Grey bin", date(2026, 12, 20)) == date(2026, 12, 21)


# The real result page of a building with several house numbers (shortened, same HTML as EDG).
# The iCal file of such a building also has the bins of the other house numbers,
# so the dates are read from this page, which shows only the bins of the chosen house number.
BUILDING_PAGE = """<P ID="Adresse">Testweg 2 b-2c</P>
<SPAN ID="TermineClusterR[1100](01-w)"><P ID="LabelR[1100](01-w)">Restabfall</P>
<P ID="TurnusR[1100](01-w)">01-w&ouml;chentl.</P><P ID="TonnenartR[1100](01-w)">1100 l</P>
<LI><P ID="TermineDatumR[1100](01-w)_1">Mi. 09.12.2026 </P></LI>
<LI><P ID="TermineDatumR[1100](01-w)_2">Mi. 16.12.2026 </P></LI>
<LI CLASS="verschoben"><P ID="TermineDatumR[1100](01-w)_3">Di. 22.12.2026 * </P></LI>
<LI><P ID="TermineDatumR[1100](01-w)_4">Mi. 30.12.2026 </P></LI></SPAN>
<SPAN ID="TermineClusterB[0120](02-w)"><P ID="LabelB[0120](02-w)">Bioabfall</P>
<P ID="TurnusB[0120](02-w)">02-w&ouml;chentl.</P><P ID="TonnenartB[0120](02-w)">120 l</P>
<LI><P ID="TermineDatumB[0120](02-w)_1">Fr. 04.12.2026 </P></LI>
<LI><P ID="TermineDatumB[0120](02-w)_2">Fr. 18.12.2026 </P></LI></SPAN>""" + RESULT_PAGE


class FakeEdgBuilding(FakeEdg):
    def post(self, url, data=None, files=None, headers=None, timeout=None):
        response = super().post(url, data, files, headers, timeout)
        if files is not None:
            response = FakeResponse(BUILDING_PAGE)
        return response


def test_only_bins_of_this_house_number_are_used(service):
    fake = FakeEdgBuilding()
    service.set_address("Sonnenstraße", "96", EdgCalendar(session=fake))
    schedule = service.get_schedule()
    assert "calendar" not in fake.steps   # the iCal file of the whole building is not needed
    assert schedule.get_pickup_day("Grey bin") == "Wednesday"
    assert schedule.get_rhythm_text("Grey bin") == "every week"
    assert schedule.get_pickup_day("Brown bin") == "Friday"
    assert schedule.get_pickup_day("Yellow bin") == "not collected at this address"
    assert schedule.get_pickup_day("Blue bin") == "not collected at this address"
    # Tuesday 22.12 instead of Wednesday 23.12 because of Christmas
    assert schedule.get_next_pickup("Grey bin", date(2026, 12, 17)) == date(2026, 12, 22)
