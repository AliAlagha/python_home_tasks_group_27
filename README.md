# AI-Powered Waste Sorting and Recycling Assistant

## Presentation Link

Video: https://drive.google.com/file/d/1GSH7Z3qS5UTvWmRkjlLXRY0kqqes1lxq/view?usp=sharing

Speaker: Ali Alagha

## Team Overview

| Member | Student ID | Subsystem |
|---|---|---|
| Amirhossein Owji | 7227410 | AI waste classification |
| Mahshid Jafari | 7227434 | Recycling recommendations |
| Ali Alagha | 7226045 | History and statistics, User interface and integration |

## How to Start

```bash
pip install -r requirements.txt
python main.py
```

## System Design

### AI waste classification (Amirhossein Owji)

```mermaid
classDiagram
    class ClassificationService {
        -validator : ImageValidator
        -classifier : WasteClassifier
        -min_confidence : float
        -results : list
        +__init__(min_confidence: float)
        +setup()
        +get_validator() ImageValidator
        +get_classifier() WasteClassifier
        +get_min_confidence() float
        +get_results() list
        +set_min_confidence(min_confidence: float)
        +classify(file_name: str, size_mb: float) ClassificationResult
        +count_uncertain() int
        +__str__() str
    }
    class ImageValidator {
        -max_size_mb : float
        -allowed_types : list
        -checked_count : int
        +__init__(max_size_mb: float)
        +setup()
        +get_max_size_mb() float
        +get_allowed_types() list
        +get_checked_count() int
        +set_max_size_mb(max_size_mb: float)
        +set_allowed_types(allowed_types: list)
        +add_allowed_type(file_type: str)
        +get_file_type(file_name: str) str
        +is_valid(file_name: str, size_mb: float) bool
        +__str__() str
    }
    class WasteClassifier {
        -model_name : str
        -labels : list
        -is_loaded : bool
        -prediction_count : int
        +__init__(model_name: str)
        +load_model()
        +get_model_name() str
        +get_labels() list
        +get_prediction_count() int
        +set_model_name(model_name: str)
        +is_loaded() bool
        +predict(file_name: str) tuple
        +__str__() str
    }
    class ClassificationResult {
        -item_name : str
        -confidence : float
        -min_confidence : float
        -status : str
        +__init__(item_name: str, confidence: float, min_confidence: float)
        +update_status()
        +get_item_name() str
        +get_confidence() float
        +get_min_confidence() float
        +get_status() str
        +set_item_name(item_name: str)
        +set_confidence(confidence: float)
        +set_min_confidence(min_confidence: float)
        +is_certain() bool
        +get_confidence_percent() str
        +to_dict() dict
        +__str__() str
    }
    ClassificationService "1" *-- "1" ImageValidator : validator
    ClassificationService "1" *-- "1" WasteClassifier : classifier
    ClassificationService "1" o-- "0..*" ClassificationResult : results
```

### Recycling recommendations (Mahshid Jafari)

```mermaid
classDiagram
    class RecommendationService {
        #region_name : str
        #rules : dict
        #schedule : CollectionSchedule
        #history : list
        +__init__(region_name: str)
        +load_rules()
        +get_region_name() str
        +set_region_name(region_name: str)
        +get_rules() dict
        +get_schedule() CollectionSchedule
        +get_history() list
        +add_rule(rule: RecyclingRule)
        +remove_rule(item_name: str)
        +get_rule_count() int
        +find_rules_by_category(category: str) list
        +recommend(result: ClassificationResult) Recommendation
    }
    class RecyclingRule {
        #item_name : str
        #category : str
        #bin_name : str
        #tip : str
        +__init__(item_name: str, category: str, bin_name: str, tip: str)
        +get_item_name() str
        +set_item_name(item_name: str)
        +get_category() str
        +set_category(category: str)
        +get_bin_name() str
        +set_bin_name(bin_name: str)
        +get_tip() str
        +set_tip(tip: str)
        +is_recyclable() bool
        +has_tip() bool
        +show()
    }
    class CollectionSchedule {
        #region_name : str
        #pickup_days : dict
        +__init__(region_name: str)
        +load_default_days()
        +get_region_name() str
        +set_region_name(region_name: str)
        +get_pickup_days() dict
        +set_pickup_day(bin_name: str, day: str)
        +get_pickup_day(bin_name: str) str
        +is_pickup_today(bin_name: str) bool
        +show()
    }
    class Recommendation {
        #rule : RecyclingRule
        #region_name : str
        #pickup_day : str
        #created_at : datetime
        +__init__(rule: RecyclingRule, region_name: str, pickup_day: str)
        +get_rule() RecyclingRule
        +set_rule(rule: RecyclingRule)
        +get_region_name() str
        +set_region_name(region_name: str)
        +get_pickup_day() str
        +set_pickup_day(pickup_day: str)
        +get_created_at() datetime
        +get_category() str
        +get_bin_name() str
        +to_dict() dict
        +show()
    }
    RecommendationService "1" o-- "0..*" RecyclingRule : rules
    RecommendationService "1" *-- "1" CollectionSchedule : schedule
    RecommendationService "1" o-- "0..*" Recommendation : history
    Recommendation "0..*" --> "1" RecyclingRule : rule
```

### History and statistics (Ali Alagha)

```mermaid
classDiagram
    class Dashboard {
        #service : StatisticsService
        #region_filter : str
        #date_filter : int
        #user : User
        +__init__(service: StatisticsService, region_filter: str, date_filter: int)
        +reset_filters()
        +get_region_filter() str
        +set_region_filter(region_filter: str)
        +get_date_filter() int
        +set_date_filter(days: int)
        +get_user() User
        +login(user: User, password: str) bool
        +logout()
        +is_logged_in() bool
        +filter_data() DataFrame
        +show_charts() dict
        +export_csv(path: str)
    }
    class User {
        #user_id : int
        #username : str
        #password_hash : str
        #region_name : str
        #last_login : datetime
        +__init__(user_id: int, username: str, password: str, region_name: str)
        +get_user_id() int
        +get_username() str
        +set_username(username: str)
        +get_password_hash() str
        +set_password(password: str)
        +get_region_name() str
        +set_region_name(region_name: str)
        +get_last_login() datetime
        +check_password(password: str) bool
        +update_last_login()
        +show()
    }
    class StatisticsService {
        #records : list
        +__init__()
        +load_records(rows: list)
        +get_records() list
        +set_records(records: list)
        +get_scan_count() int
        +add_record(record: ScanRecord)
        +clear()
        +get_records_by_region(region_name: str) list
        +get_regions() list
        +get_dataframe() DataFrame
        +get_totals(df: DataFrame) dict
        +get_recycle_rate(df: DataFrame) float
        +get_most_common_items(df: DataFrame, n: int) dict
        +show_history()
    }
    class ScanRecord {
        #scan_id : int
        #region_name : str
        #category : str
        #item_name : str
        #scan_date : date
        +__init__(scan_id: int, region_name: str, category: str, item_name: str, scan_date: date)
        +get_scan_id() int
        +get_region_name() str
        +set_region_name(region_name: str)
        +get_category() str
        +set_category(category: str)
        +get_item_name() str
        +set_item_name(item_name: str)
        +get_scan_date() date
        +set_scan_date(scan_date: date)
        +is_recyclable() bool
        +is_from_today() bool
        +to_dict() dict
        +show()
    }
    Dashboard "0..*" --> "1" StatisticsService : service
    Dashboard "0..*" --> "0..1" User : logged in user
    StatisticsService "1" o-- "0..*" ScanRecord : records
```

### User interface and integration (Ali Alagha)

```mermaid
classDiagram
    class ApiGateway {
        #accounts : dict
        #sessions : dict
        #classification : ClassificationService
        #recommendations : RecommendationService
        #statistics : StatisticsService
        +__init__()
        +setup()
        +get_accounts() dict
        +get_classification() ClassificationService
        +get_recommendations() RecommendationService
        +get_statistics() StatisticsService
        +register(username: str, password: str, role: str, region_name: str) Account
        +login(username: str, password: str) str
        +logout(token: str)
        +get_account(token: str) Account
        +get_user_count() int
        +scan(token: str, file_name: str, size_mb: float) Recommendation
        +dashboard(token: str) dict
    }
    class Account {
        +ROLES : list$
        #username : str
        #password_hash : str
        #role : str
        #region_name : str
        #created_at : datetime
        #scan_count : int
        +__init__(username: str, password: str, role: str, region_name: str)
        +get_username() str
        +get_role() str
        +get_region_name() str
        +get_created_at() datetime
        +get_scan_count() int
        +set_username(username: str)
        +set_password(password: str)
        +set_role(role: str)
        +set_region_name(region_name: str)
        +check_password(password: str) bool
        +is_municipality() bool
        +add_scan()
        +show()
    }
    class Session {
        +DEFAULT_MINUTES : int$
        #account : Account
        #minutes : int
        #token : str
        #expires_at : datetime
        +__init__(account: Account, minutes: int)
        +start()
        +get_token() str
        +get_account() Account
        +get_minutes() int
        +get_expires_at() datetime
        +set_minutes(minutes: int)
        +set_expires_at(expires_at: datetime)
        +is_expired() bool
        +extend()
        +end()
        +get_minutes_left() int
    }
    ApiGateway "1" o-- "0..*" Account : accounts
    ApiGateway "1" *-- "0..*" Session : sessions
    Session "0..*" --> "1" Account : account
```
