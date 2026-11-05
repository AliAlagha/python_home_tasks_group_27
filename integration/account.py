import hashlib
from datetime import datetime


class Account:
    ROLES = ["citizen", "municipality"]

    def __init__(self, username, password, role="citizen", region_name="Dortmund", street="", house_number=""):
        self._username = username
        self._password_hash = ""
        self._role = role
        self._region_name = region_name
        self._street = street                  # address is needed for the collection dates
        self._house_number = str(house_number)
        self._created_at = datetime.now()
        self._scan_count = 0
        self.set_password(password)

    # accessors
    def get_username(self):
        return self._username

    def get_role(self):
        return self._role

    def get_region_name(self):
        return self._region_name

    def get_street(self):
        return self._street

    def get_house_number(self):
        return self._house_number

    def get_created_at(self):
        return self._created_at

    def get_scan_count(self):
        return self._scan_count

    # mutators
    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        # only the hash is saved, never the password
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    def set_role(self, role):
        if role in Account.ROLES:
            self._role = role

    def set_region_name(self, region_name):
        self._region_name = region_name

    def set_address(self, street, house_number):
        self._street = street
        self._house_number = str(house_number)

    # behaviour
    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self._password_hash

    def is_municipality(self):
        return self._role == "municipality"

    def add_scan(self):
        self._scan_count += 1

    def show(self):
        print("{} ({}, {}) - {} scans".format(self._username, self._role, self._region_name, self._scan_count))
