import os
import csv
from PyQt6.QtWidgets import QMainWindow
from gui import Ui_VotingApp

def id_already_exists(voter_id: str, filename: str = "voting_data.csv"):
    """Return True if voter_id already appears in column 'id' of CSV"""
    if not os.path.isfile(filename):
        return False

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[1] == voter_id:
                return True
    return False

class VotingApp(QMainWindow):
    """Main application window for the Voting app"""
    csv_file = 'voting_data.csv'

    def __init__(self):
        super().__init__()
        self.ui = Ui_VotingApp()
        self.ui.setupUi(self)

        # ensures CSV file exists with header
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                csv.writer(f).writerow(['candidate', 'id', 'zip', 'age', ])
        else:
            with open(self.csv_file, 'r', newline='') as f:
                rows = list(csv.reader(f))

        # button functionality
        self.ui.submit_button.clicked.connect(self.submit)

        # corrects display initialization
        self.ui.info_label.setText('')

    def submit(self):
        """Verifies inputs until correct, updates display message, saves data in CSV, then clears inputs for next voter"""
        id = self.ui.id_input.toPlainText().strip()
        zip = self.ui.zip_input.toPlainText().strip()
        age = self.ui.age_input.toPlainText().strip()

        if self.ui.option1_radioButton.isChecked(): candidate = self.ui.option1_radioButton.text()
        elif self.ui.option2_radioButton.isChecked(): candidate = self.ui.option2_radioButton.text()
        else: candidate = None

        # handle making uniform error messages
        def error(msg):
            """intakes error message depending on which invalid input called it,
            turns info_label red, then sets info_label to the error message"""
            self.ui.info_label.setStyleSheet("color: red")
            self.ui.info_label.setText(msg)

        # id validation
        valid_id = True if id.isdigit() and len(id) == 8 else False
        if valid_id is False:
            return error("Invalid ID\nMust be 8 digit integer")
        # zip validation
        valid_zip = True if zip.isdigit() and len(zip) == 5 else False
        if valid_zip is False:
            return error("Invalid Zip\nMust be 5 digit integer")
        # age validation
        valid_age = True if age.isdigit() and 18 <= int(age) <= 115 else False
        if not age.isdigit():
            return error("Invalid Age\nMust be a positive integer")
        if int(age) < 18:
            return error("Invalid Age\nMust be 18 or older")
        if int(age) > 115: # 115 is the age of the oldest person alive right now
            return error("Invalid Age\nToo high - Not real")
        # check that a candidate is selected
        if candidate is None and valid_id and valid_zip and valid_age:
            self.ui.info_label.setStyleSheet(None)
            return self.ui.info_label.setText("Pick a candidate")

        # verify id is unique
        if id_already_exists(id, self.csv_file):
            return error("Already voted with this ID")

        # --- if inputs have made it past this point, they are valid ---

        # append row to csv
        with open(self.csv_file, 'a', newline='') as f:
            csv.writer(f).writerow([candidate, id, zip, age])

        # clear/reset display for next voter
        self.ui.info_label.setStyleSheet(None)
        self.ui.info_label.setText("Vote Submitted!")
        self.ui.id_input.clear()
        self.ui.zip_input.clear()
        self.ui.age_input.clear()
        self.ui.option1_radioButton.setAutoExclusive(False)
        self.ui.option1_radioButton.setChecked(False)
        self.ui.option2_radioButton.setAutoExclusive(True)
        self.ui.option2_radioButton.setAutoExclusive(False)
        self.ui.option1_radioButton.setChecked(False)
        self.ui.option2_radioButton.setAutoExclusive(True)
