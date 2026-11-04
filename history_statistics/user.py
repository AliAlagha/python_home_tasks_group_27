import hashlib
from datetime import datetime


class User:
    def __init__(self, user_id, username, password, region_name="All"):
        self._user_id = user_id
        self._username = username
        self._region_name = region_name
        self._last_login = None
        self.set_password(password)

    # getters and setters

    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_password_hash(self):
        return self._password_hash

    def set_password(self, password):
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    def get_region_name(self):
        return self._region_name

    def set_region_name(self, region_name):
        self._region_name = region_name

    def get_last_login(self):
        return self._last_login

    # methods

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self._password_hash

    def update_last_login(self):
        self._last_login = datetime.now()

    def show(self):
        print("User", self._user_id, ":", self._username, "| region:", self._region_name)
