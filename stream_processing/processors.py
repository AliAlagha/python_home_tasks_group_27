from abc import ABC, abstractmethod

# label from the camera -> material
MATERIALS = {
    "plastic": "PET",
    "bottle": "PET",
    "milk jug": "HDPE",
    "can": "Aluminum",
    "glass": "Glass",
    "paper": "Paper",
    "cardboard": "Paper",
}


class Processor(ABC):

    @abstractmethod
    def process(self, item):
        pass

    # p1 + p2 gives a pipeline
    def __add__(self, other):
        return Pipeline([self, other])

    # p1 | p2 works the same way
    def __or__(self, other):
        return self + other

    def run(self, stream):
        for item in stream:
            item = self.process(item)
            if item is not None:
                yield item


class ConfidenceFilter(Processor):

    def __init__(self, min_confidence=0.7):
        self.min_confidence = min_confidence

    def process(self, item):
        if item.get("confidence", 0) < self.min_confidence:
            return None
        return item


class MaterialTransformer(Processor):

    def process(self, item):
        item["material"] = MATERIALS.get(item["label"], "Unknown")
        return item


class RouteTransformer(Processor):

    def process(self, item):
        if item["material"] == "Unknown":
            item["route"] = "reject"
            return item
        # bbox = [x, y, width, height]
        width = item["bbox"][2]
        height = item["bbox"][3]
        if width * height > 5000:
            item["route"] = item["material"] + "-big"
        else:
            item["route"] = item["material"] + "-small"
        return item


class Pipeline(Processor):

    def __init__(self, steps):
        self.steps = steps

    def process(self, item):
        for step in self.steps:
            item = step.process(item)
            if item is None:
                return None
        return item

    def __add__(self, other):
        return Pipeline(self.steps + [other])
