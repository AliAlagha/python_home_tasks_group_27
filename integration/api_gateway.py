from classification.classification_service import ClassificationService
from classification.errors import ClassificationError
from history_statistics.scan_record import ScanRecord
from history_statistics.statistics_service import StatisticsService
from recommendations.recommendation_service import RecommendationService

from .account import Account
from .errors import IntegrationError
from .session import Session


class ApiGateway:

    def __init__(self):
        self._accounts = {}
        self._sessions = {}
        self._classification = ClassificationService()
        self._recommendations = RecommendationService()
        self._statistics = StatisticsService()

    def setup(self):
        self._classification.setup()
        self._recommendations.load_rules()

    # accessors
    def get_accounts(self):
        return self._accounts

    def get_classification(self):
        return self._classification

    def get_recommendations(self):
        return self._recommendations

    def get_statistics(self):
        return self._statistics

    # behaviour
    def register(self, username, password, role="citizen", region_name="Dortmund", street="", house_number=""):
        if username in self._accounts:
            raise IntegrationError("username {} is already taken".format(username), 409)
        account = Account(username, password, role, region_name, street, house_number)
        self._accounts[username] = account
        return account

    def login(self, username, password):
        account = self._accounts.get(username)
        if account is None or not account.check_password(password):
            raise IntegrationError("wrong username or password", 401)
        session = Session(account)
        self._sessions[session.get_token()] = session
        return session.get_token()

    def logout(self, token):
        if token in self._sessions:
            self._sessions[token].end()
            del self._sessions[token]

    def get_account(self, token):
        session = self._sessions.get(token)
        if session is None or session.is_expired():
            raise IntegrationError("please log in first", 401)
        session.extend()
        return session.get_account()

    def get_user_count(self):
        return len(self._accounts)

    # one scan goes through the 3 other subsystems: classification -> recommendation -> history
    def scan(self, token, file_name, size_mb):
        account = self.get_account(token)

        # the error from the classification is sent on as an API error
        try:
            result = self._classification.classify(file_name, size_mb)
        except ClassificationError as error:
            raise IntegrationError(str(error), 422)
        recommendation = self._recommendations.recommend(result, account.get_street(), account.get_house_number())

        scan_id = self._statistics.get_scan_count() + 1
        record = ScanRecord(scan_id, account.get_region_name(), recommendation.get_category(), result.get_item_name())
        self._statistics.add_record(record)
        account.add_scan()
        return recommendation

    def dashboard(self, token):
        account = self.get_account(token)
        if not account.is_municipality():
            raise IntegrationError("only municipality users can see the dashboard", 403)
        df = self._statistics.get_dataframe()
        return {
            "scans": len(df),
            "waste_composition": self._statistics.get_totals(df),
            "recycling_rate": self._statistics.get_recycle_rate(df),
        }
