from .classification_result import ClassificationResult
from .image_validator import ImageValidator
from .waste_classifier import WasteClassifier


class ClassificationService:
    def __init__(self, min_confidence=0.6):
        self.__validator = ImageValidator()
        self.__classifier = WasteClassifier()
        self.__min_confidence = min_confidence
        self.__results = []

    def setup(self):
        self.__classifier.load_model()

    # getters
    def get_validator(self):
        return self.__validator

    def get_classifier(self):
        return self.__classifier

    def get_min_confidence(self):
        return self.__min_confidence

    def get_results(self):
        return self.__results

    # setters
    def set_min_confidence(self, min_confidence):
        self.__min_confidence = min_confidence

    # other methods
    def classify(self, file_name, size_mb):
        # check the image first, then let the model guess
        if not self.__validator.is_valid(file_name, size_mb):
            print(f"Image {file_name} is not valid")
            return None
        item_name, confidence = self.__classifier.predict(file_name)
        result = ClassificationResult(item_name, confidence, self.__min_confidence)
        self.__results.append(result)
        return result

    def count_uncertain(self):
        count = 0
        for result in self.__results:
            if not result.is_certain():
                count += 1
        return count

    def __str__(self):
        return f"ClassificationService: {len(self.__results)} images classified, {self.count_uncertain()} uncertain"
