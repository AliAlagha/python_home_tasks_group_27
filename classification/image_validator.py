class ImageValidator:
    def __init__(self, max_size_mb=5):
        self.__max_size_mb = max_size_mb
        self.__allowed_types = []
        self.__checked_count = 0
        self.setup()

    def setup(self):
        # only photos are accepted
        self.__allowed_types = ["jpg", "jpeg", "png"]

    # getters
    def get_max_size_mb(self):
        return self.__max_size_mb

    def get_allowed_types(self):
        return self.__allowed_types

    def get_checked_count(self):
        return self.__checked_count

    # setters
    def set_max_size_mb(self, max_size_mb):
        self.__max_size_mb = max_size_mb

    def set_allowed_types(self, allowed_types):
        self.__allowed_types = allowed_types

    # other methods
    def add_allowed_type(self, file_type):
        if file_type.lower() not in self.__allowed_types:
            self.__allowed_types.append(file_type.lower())

    def get_file_type(self, file_name):
        return file_name.split(".")[-1].lower()

    def is_valid(self, file_name, size_mb):
        self.__checked_count += 1
        if self.get_file_type(file_name) not in self.__allowed_types:
            return False
        return 0 < size_mb <= self.__max_size_mb

    def __str__(self):
        return f"ImageValidator(types={self.__allowed_types}, max={self.__max_size_mb} MB)"
