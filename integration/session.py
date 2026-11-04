import uuid
from datetime import datetime, timedelta


class Session:
    DEFAULT_MINUTES = 60

    def __init__(self, account, minutes=DEFAULT_MINUTES):
        self._account = account
        self._minutes = minutes
        self._token = ""
        self._expires_at = None
        self.start()

    def start(self):
        self._token = str(uuid.uuid4())
        self._expires_at = datetime.now() + timedelta(minutes=self._minutes)

    # accessors
    def get_token(self):
        return self._token

    def get_account(self):
        return self._account

    def get_minutes(self):
        return self._minutes

    def get_expires_at(self):
        return self._expires_at

    # mutators
    def set_minutes(self, minutes):
        self._minutes = minutes

    def set_expires_at(self, expires_at):
        self._expires_at = expires_at

    # behaviour
    def is_expired(self):
        return datetime.now() > self._expires_at

    def extend(self):
        # user is still active so the time starts again
        self._expires_at = datetime.now() + timedelta(minutes=self._minutes)

    def end(self):
        self._expires_at = datetime.now()

    def get_minutes_left(self):
        if self.is_expired():
            return 0
        return int((self._expires_at - datetime.now()).total_seconds() // 60)
