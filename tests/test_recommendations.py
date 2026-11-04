import pytest

from classification.classification_result import ClassificationResult
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


def test_uncertain_result_goes_to_black_bin(service):
    recommendation = service.recommend(ClassificationResult("plastic", 0.3))
    assert recommendation.get_rule().get_bin_name() == "Black bin"


def test_unknown_category_raises_error():
    with pytest.raises(RecommendationError):
        RecyclingRule("pizza box", "Burnable", "Black bin")


def test_recommend_without_rules_raises_error():
    with pytest.raises(RecommendationError):
        RecommendationService().recommend(ClassificationResult("plastic", 0.9))


def test_plastic_pickup_is_on_monday(service):
    recommendation = service.recommend(ClassificationResult("plastic", 0.9))
    assert recommendation.get_pickup_day() == "Monday"


def test_wrong_pickup_day_raises_error(service):
    with pytest.raises(RecommendationError):
        service.get_schedule().set_pickup_day("Yellow bin", "Funday")
