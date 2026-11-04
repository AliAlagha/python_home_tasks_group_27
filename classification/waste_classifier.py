class WasteClassifier:
    def __init__(self, model_name="watersplash/waste-classification"):
        self.__model_name = model_name
        self.__labels = []
        self.__is_loaded = False
        self.__prediction_count = 0

    def load_model(self):
        # the real ViT model is in our capstone project
        # here we only load the labels it knows
        self.__labels = ["battery", "biological", "glass", "cardboard", "clothes",
                         "metal", "paper", "plastic", "shoes", "trash"]
        self.__is_loaded = True

    # getters
    def get_model_name(self):
        return self.__model_name

    def get_labels(self):
        return self.__labels

    def get_prediction_count(self):
        return self.__prediction_count

    # setters
    def set_model_name(self, model_name):
        self.__model_name = model_name
        self.__is_loaded = False  # new model has to be loaded again

    # other methods
    def is_loaded(self):
        return self.__is_loaded

    def predict(self, file_name):
        self.__prediction_count += 1
        # fake prediction, we search the label in the file name
        for label in self.__labels:
            if label in file_name.lower():
                return label, 0.9
        return "trash", 0.4

    def __str__(self):
        return f"WasteClassifier({self.__model_name}, loaded={self.__is_loaded}, {len(self.__labels)} labels)"
