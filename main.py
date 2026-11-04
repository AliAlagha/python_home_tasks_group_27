# the code of every homework is in its own branch, see README.md

BRANCHES = {
    "HomeworkAssignment001": "Object Oriented Concepts",
    "HomeworkAssignment002": "Real-Time Data Processing",
    "HomeworkAssignment003": "Web APIs & Database Access Layers",
    "HomeworkAssignment004": "Exception Handling and Unit Tests",
}


def main():
    print("AI-Powered Waste Sorting and Recycling Assistant - group 27")
    print("Switch to a branch to see a homework:")
    for branch in BRANCHES:
        print("  git checkout " + branch + "   (" + BRANCHES[branch] + ")")


if __name__ == "__main__":
    main()
