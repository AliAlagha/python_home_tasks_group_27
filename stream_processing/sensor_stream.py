class SensorStream:

    def __init__(self, items):
        self.items = items
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item


# fake camera, gives one item at a time
def camera(count):
    labels = ["bottle", "can", "banana", "glass", "cardboard"]
    confidences = [0.9, 0.85, 0.75, 0.5, 0.95]
    for i in range(count):
        yield {
            "id": i + 1,
            "label": labels[i % 5],
            "confidence": confidences[i % 5],
            "bbox": [0, 0, 40 + i * 10, 60 + i * 10],
        }
