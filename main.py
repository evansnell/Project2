import os
import csv
import sys
from PyQt6.QtWidgets import QApplication
from logic import VotingApp

def main():
    app = QApplication(sys.argv)
    window = VotingApp()
    window.show()

    exit_code = app.exec() # create key when app closes
    print('Program closed... ', end='')

    csv_file = VotingApp.csv_file
    votes = {}

    # make dictionary of voting data
    if os.path.isfile(csv_file):
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            next(reader) # skipper header
            for row in reader:
                candidate, _id, _zip, age = row
                votes.setdefault(candidate, []).append(int(age))

    # determine info for output
    total_votes = sum(len(ages) for ages in votes.values())
    if total_votes > 0:
        print("Votes are in!\n")
        print(f"{total_votes} votes recorded")

        # output average age of voters for each candidate
        for candidate, ages in votes.items():
            avg_age = sum(ages) / len(ages)
            print(f"The average age of voters for {candidate} is {avg_age:.0f} y/o")

        # output leading candidate and by how much
        leader, leader_ages = max(votes.items(), key=lambda kv: len(kv[1]))
        pct = len(leader_ages) / total_votes * 100
        if pct == 50.0:
            print(f"There is no leading candidate: votes are perfectly split 50/50")
        else:
            print(f"The leading candidate: {leader} with {pct:.0f}% of votes!")
    else:
        print("No votes have been recorded.")

    sys.exit(exit_code) # key made from closing app now ends the program after all the outputs are finished

if __name__ == '__main__':
    main()
