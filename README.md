# AI-Powered Waste Sorting and Recycling Assistant

Capstone project group 27, Topic 2. A web app where anyone can photograph a waste item and learn how to dispose of it. An AI model sorts the item as recyclable, compostable or landfill, the app adds local recycling advice for the user's region, and municipalities get a dashboard showing what people throw away and how much is recycled.

## Team

| Member | Student ID | Subsystem |
|---|---|---|
| Amirhossein Owji | 7227410 | AI waste classification |
| Mahshid Jafari | 7227434 | Recycling recommendations |
| Ali Alagha | 7226045 | History and statistics, User interface and integration |

## Where is the code?

The `main` branch only has this overview. Every homework is in its own branch, with its own README, class diagrams and instructions how to run it.

| Branch | Homework | What is inside |
|---|---|---|
| [HomeworkAssignment001](https://github.com/AliAlagha/python_home_tasks_group_27/tree/HomeworkAssignment001) | 1. Object Oriented Concepts | The classes of the 4 subsystems (`classification/`, `recommendations/`, `history_statistics/`, `integration/`) and `main.py` that runs them together |
| [HomeworkAssignment002](https://github.com/AliAlagha/python_home_tasks_group_27/tree/HomeworkAssignment002) | 2. Real-Time Data Processing | `stream_processing/`: conveyor belt stream with an abstract base class, `+` / `\|` pipelines, an iterator and generators |
| [HomeworkAssignment003](https://github.com/AliAlagha/python_home_tasks_group_27/tree/HomeworkAssignment003) | 3. Web APIs & Database Access Layers | `web_api/`: Flask app that reads the scan history from MySQL as a web page and JSON |
| [HomeworkAssignment004](https://github.com/AliAlagha/python_home_tasks_group_27/tree/HomeworkAssignment004) | 4. Exception Handling and Unit Tests | The subsystems from HA1 and the Flask app from HA3 with an error class for each subsystem, and 30 tests in `tests/` |

To get a homework on your computer:

```bash
git clone https://github.com/AliAlagha/python_home_tasks_group_27.git
cd python_home_tasks_group_27
git checkout HomeworkAssignment001
```

## Structure of this branch

```
python_home_tasks_group_27/
├── README.md          this overview
├── main.py            prints the list of homework branches
├── requirements.txt   no packages needed here, every branch has its own
└── .gitignore
```

```bash
python main.py
```
