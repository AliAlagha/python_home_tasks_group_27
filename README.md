# AI-Powered Waste Sorting and Recycling Assistant

## Presentation Link

Video: https://drive.google.com/file/d/1TWZ1_cvZAp1UbBfu4kM-dm4uV7JWMXZ9/view?usp=sharing

## Team Overview

| Member | Student ID | Subsystem |
|---|---|---|
| Amirhossein Owji | 7227410 | AI waste classification |
| Mahshid Jafari | 7227434 | Recycling recommendations |
| Ali Alagha | 7226045 | History and statistics, User interface and integration |

## How to Start

A MySQL server must be running for the web API tests.

```bash
pip install -r requirements.txt
mysql -u root < web_api/database.sql
python main.py
python -m pytest
```
