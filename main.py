import os
import csv
import sys
from PyQt6.QtWidgets import QApplication
from logic import VotingApp

def main():
    app = QApplication(sys.argv)
    window = VotingApp()
    window.show()
    exit_code = app.exec()
    print('Program closed... ', end='')

    csv_file = VotingApp.csv_file
    votes = {}

    if os.path.isfile(csv_file):
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                candidate, _id, _zip, age = row
                votes.setdefault(candidate, []).append(int(age))

    total_votes = sum(len(ages) for ages in votes.values())
    if total_votes > 0:
        print("Votes are in!\n")
        print(f"{total_votes} votes recorded")

        for candidate, ages in votes.items():
            avg_age = sum(ages) / len(ages)
            print(f"The average age of voters for {candidate} is {avg_age:.2f} y/o")

        leader, leader_ages = max(votes.items(), key=lambda kv: len(kv[1]))
        pct = len(leader_ages) / total_votes * 100
        if pct == 50.0:
            print(f"There is no leading candidate: votes are perfectly split 50/50")
        else:
            print(f"The leading candidate: {leader} with {pct:.2f}% of votes!")
    else:
        print("No votes have been recorded.")

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
