from stream_processing.processors import ConfidenceFilter, MaterialTransformer, RouteTransformer
from stream_processing.sensor_stream import SensorStream, camera

items = [
    {"id": 1, "label": "bottle", "confidence": 0.92, "bbox": [10, 20, 50, 120]},
    {"id": 2, "label": "can", "confidence": 0.81, "bbox": [5, 5, 30, 50]},
    {"id": 3, "label": "glass", "confidence": 0.4, "bbox": [0, 0, 60, 90]},
    {"id": 4, "label": "milk jug", "confidence": 0.88, "bbox": [20, 10, 80, 100]},
    {"id": 5, "label": "banana", "confidence": 0.77, "bbox": [0, 0, 20, 15]},
    {"id": 6, "label": "cardboard", "confidence": 0.99, "bbox": [0, 0, 200, 150]},
]


def main():
    pipeline = ConfidenceFilter(0.7) + MaterialTransformer() + RouteTransformer()

    print("From the list:")
    for item in pipeline.run(SensorStream(items)):
        print(item["id"], item["label"], "->", item["route"])

    # same steps written with |
    pipeline2 = ConfidenceFilter(0.7) | MaterialTransformer() | RouteTransformer()

    print("From the camera:")
    for item in pipeline2.run(camera(8)):
        print(item["id"], item["label"], "->", item["route"])


if __name__ == "__main__":
    main()
