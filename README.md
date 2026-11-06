# AI-Powered Waste Sorting and Recycling Assistant

## Presentation Link

Video: https://drive.google.com/file/d/1HCmXsQDjeA85FPR-J9T7TQv1VIAuEAvy/view?usp=sharing

## Team Overview

| Member | Student ID | Subsystem |
|---|---|---|
| Amirhossein Owji | 7227410 | AI waste classification |
| Mahshid Jafari | 7227434 | Recycling recommendations |
| Ali Alagha | 7226045 | History and statistics, User interface and integration |

## Project Information

A Flask app that reads the scan history from a MySQL database and shows it as a web page and as JSON.

| Route | Output |
|---|---|
| `/` | Scan history table |
| `/api/scans` | Scan history as JSON |
| `/api/scans?region=Dortmund` | Scans of one region |
| `/api/scans/<id>` | One scan as JSON |
| `/api/statistics` | Waste composition, recycling rate and most common items |

## How to Start

A MySQL server must be running.

```bash
pip install -r requirements.txt
mysql -u root < web_api/database.sql
python -m web_api.app
```

Then open http://127.0.0.1:5001

The app connects as `root` with no password. Use `DB_HOST`, `DB_USER`, `DB_PASSWORD` or `DB_NAME` to change it:

```bash
DB_PASSWORD=secret python -m web_api.app
```
