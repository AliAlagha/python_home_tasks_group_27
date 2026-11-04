from .errors import ClassificationError


class ClassificationResult:
    def __init__(self, item_name, confidence, min_confidence=0.6):
        if confidence < 0 or confidence > 1:
            raise ClassificationError("confidence must be between 0 and 1")
        self.__item_name = item_name
        self.__confidence = confidence
        self.__min_confidence = min_confidence
        self.__status = ""
        self.update_status()

    def update_status(self):
        if self.__confidence >= self.__min_confidence:
            self.__status = "Success"
        else:
            self.__status = "Uncertain"

    # getters
    def get_item_name(self):
        return self.__item_name

    def get_confidence(self):
        return self.__confidence

    def get_min_confidence(self):
        return self.__min_confidence

    def get_status(self):
        return self.__status

    # setters
    def set_item_name(self, item_name):
        self.__item_name = item_name

    def set_confidence(self, confidence):
        if confidence < 0 or confidence > 1:
            raise ClassificationError("confidence must be between 0 and 1")
        self.__confidence = confidence
        self.update_status()

    def set_min_confidence(self, min_confidence):
        self.__min_confidence = min_confidence
        self.update_status()

    # other methods
    def is_certain(self):
        return self.__status == "Success"

    def get_confidence_percent(self):
        return f"{round(self.__confidence * 100)}%"

    def to_dict(self):
        return {"item_name": self.__item_name, "confidence": self.__confidence, "status": self.__status}

    def __str__(self):
        return f"{self.__item_name} ({self.get_confidence_percent()}, {self.__status})"
