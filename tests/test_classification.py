import pytest

from classification.classification_result import ClassificationResult
from classification.classification_service import ClassificationService
from classification.errors import ClassificationError
from classification.image_validator import ImageValidator
from classification.waste_classifier import WasteClassifier


def test_text_file_is_not_valid():
    assert ImageValidator().is_valid("notes.txt", 1) is False


def test_predict_without_model_raises_error():
    with pytest.raises(ClassificationError):
        WasteClassifier().predict("plastic_bottle.jpg")


def test_predict_plastic_bottle():
    classifier = WasteClassifier()
    classifier.load_model()
    assert classifier.predict("plastic_bottle.jpg") == ("plastic", 0.9)


def test_low_confidence_is_uncertain():
    result = ClassificationResult("trash", 0.4)
    assert result.get_status() == "Uncertain"


def test_wrong_confidence_raises_error():
    with pytest.raises(ClassificationError):
        ClassificationResult("plastic", 1.5)


def test_service_raises_error_for_wrong_file():
    service = ClassificationService()
    service.setup()
    with pytest.raises(ClassificationError):
        service.classify("notes.txt", 1)
