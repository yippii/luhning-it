import csv
import os
import sys
from pathlib import Path
from datetime import datetime

import pygame
import pygame.mixer


# Customer info is a list that stores all customer information
# before user generate the data file, which would then clear it
customerInfo = list()


# Get amount of customer by recursively searching all .csv files in ~/Documents
# If header signature matches, then it would be parsed in the following order

# 1. Retrieve the stripped version (no space or newline)
# of the first column of the last line of the .csv file (Customer ID)

# 2. Only extract digits that are present in the Customer ID
# ** Reason for 2: Adding robustness to the code if the count goes more than one digit **

# CSV file is hardcoded to store in the User Documents folder as it is packaged as an application
# and would not be viable to store it internally inside the Temp folder
# for the executable or in an obscured folder

file_exist = False

for path in Path(os.path.expanduser('~/Documents/')).rglob('*.csv'):
    with open(path, 'r') as file:
        file_exist = True
        if list(csv.reader(file))[0][0] == "Customer ID":
            expected_path = path
            file.seek(0)
            customer_number = int(''
                .join(
                    number for number in
                    list(csv.reader(file))[-1][0].strip()
                    if number.isdigit()
                ))
    file.close()

# If the for loop never ran
if not file_exist:
    customer_number = 0
    expected_path = ""

customer_number += 1

# Music
# goated music by nathan c and nicky m
def escalator_music(filepath: str):

    # Pre-initialize the mixer with a larger buffer to prevent stuttering
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()

    if "__compiled__" in globals():
        filepath = f"{os.path.dirname(sys.executable)}/{filepath}"
        print(
            f"[DEBUG] Audio Subsystem - Detected Nuitka Compiled Application, using {filepath} instead"
        )

    try:
        pygame.mixer_music.set_volume(0.5)  # Adjust volume level (0.0 to 1.0)
        pygame.mixer.music.load(filepath)
        # -1 loops indefinitely.
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"[ERROR] Could not play audio file: {e}")


# Input Error Messages
class GUIError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Called by checkPostalCode()
def parseCSV(file: str) -> list[str]:
    """
    Parse a CSV file and return into a list of rows in a list of CSV values
    """

    with open(
        file=file, mode="r", newline="", encoding="utf-8", errors="replace"
    ) as csv_file:
        # Take the file and separate with |
        csv_data = list(csv.reader(csv_file, delimiter="|"))

        # Remove header
        csv_data.pop(0)

        csv_data = [row[0] for row in csv_data]
        return csv_data


# Called by validateCreditCard()
def luhn_check(numbers: str) -> bool:
    """
    Check if the numbers are valid through the luhn algorithm
    """

    numbers = numbers.strip()

    if not numbers.isdigit():
        return False

    # Initial variable to store the total for the check
    total = 0

    # Luhn algorithm - Step 1: Get last digit
    last_digit = numbers[-1]

    # Luhn algorithm - Step 2: Remove last digit
    numbers = numbers[:-1]

    # Luhn algorithm - Step 3: Loop through all the numbers and double every second digit
    for i, digit in enumerate(reversed(numbers)):
        # Numbers that are doubled
        if i % 2 == 0:
            digit = int(digit) * 2

            # If doubled numbers are more than 9, make them single digit
            if digit > 9:
                string_number = str(digit)
                digit = int(string_number[0]) + int(string_number[1])

            total += digit
        else:
            # Numbers that aren't doubled
            total += int(digit)

    # Luhn algorithm - Step 4: Check with modulo 10 with the excluded last digit
    # If it is 0, then it is valid through the Luhn Algorithm
    return (total + int(last_digit)) % 10 == 0


# Called by main application through option 1
def enterCustomerInfo(
    firstName: str,
    lastName: str,
    city: str,
    postalCode: str,
    credit_card_number: str,
    birth_date: str,
):
    """
    Provide a prompt for users to enter customer information
    """

    global customer_number

    if firstName == "":
        raise GUIError("Please enter your first name")

    if lastName == "":
        raise GUIError("Please enter your last name")

    if city == "":
        raise GUIError("Please enter your city")

    if not validatePostalCode(postalCode):
        raise GUIError("Please enter a valid postal code")

    if not validateCreditCard(credit_card_number):
        raise GUIError("Please enter a valid credit card number")

    try:
        if not validateBirthDate(birth_date):
            # Generic error
            raise GUIError("Please enter a valid birth date\n (YYYY-MM-DD)")
    # Specific error
    except GUIError as e:
        raise e

    # Increment customer number by 1 after completing the operation
    name = f"{customer_number}{firstName.lower()[:2]}{lastName.lower()[:2]}"
    customerInfo.append(
        [
            name,
            firstName.lower().capitalize(),
            lastName.lower().capitalize(),
            city.lower().capitalize(),
            postalCode.upper(),
            credit_card_number,
            birth_date,
        ]
    )
    customer_number += 1
    return None


# Called by enterCustomerInfo()
def validatePostalCode(postal_code: str) -> bool:
    """
    Validate a postal code by comparing and check if it inside the CSV file
    """
    try:
        if "__compiled__" in globals():
            postalCodePath = os.path.dirname(sys.executable) + "/postal_codes.csv"
            print(
                f"[DEBUG] CSV Parse - Detected Nuitka Compiled Application, using {path} instead"
            )
        else:
            postalCodePath = "postal_codes.csv"
        postalCodes = parseCSV(postalCodePath)
    except FileNotFoundError:
        raise GUIError("Please check if postal_codes.csv exists")
    return postal_code[:3].upper() in postalCodes and len(postal_code.replace(" ", "").replace("-", "")) == 6


# Wrapper function to allow better descriptions for both functions
# Called by enterCustomerInfo()
def validateCreditCard(credit_card_number: str) -> bool:
    return luhn_check(credit_card_number)


def validateBirthDate(birth_date: str) -> bool:
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    try:
        # Format
        if len(birth_date) != 10 or birth_date[4] != "-" or birth_date[7] != "-":
            return False

        # Year
        if (
            not birth_date[:4].isdigit()
            or not int(birth_date[:4]) > 0
            or not int(birth_date[:4]) <= current_year
        ):
            raise GUIError(
                "Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect year"
            )

        # Month
        if (
            not birth_date[5:7].isdigit()
            or not int(birth_date[5:7]) > 0
            or not int(birth_date[5:7]) < 13
        ):
            raise GUIError(
                "Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect month"
            )

        # Date
        if (
            not birth_date[8:10].isdigit()
            or not int(birth_date[8:10]) > 0
            or not int(birth_date[8:10]) < 32
        ):
            raise GUIError(
                "Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect date"
            )

        # More than current date
        if (
            int(birth_date[:4]) == current_year
            and int(birth_date[5:7]) > current_month
            or int(birth_date[:4]) == current_year
            and int(birth_date[5:7]) == current_month
            and int(birth_date[8:10]) > current_day
        ):
            raise GUIError(
                "Please enter a valid birth date\n(YYYY-MM-DD)\n\nDate higher than today's date"
            )

        return True
    except ValueError:
        return False
    except GUIError as e:
        raise e


# Called by GUI through notebook1_1
def generateCustomerDataFile(content: list[str], filename: str):
    global expected_path
    if customerInfo:
        # Check if a data file already exists and error if user did not use the same file
        if filename not in str(expected_path) and expected_path != "":
            raise GUIError(f"Seems like you already have an existing data file, please uses \"{str(expected_path).split("/")[-1]}\" or delete the existing file and reopen the application")

        try:
            with open(
                file=filename, mode="a", newline="", encoding="utf-8", errors="replace"
            ) as csv_file:
                # Check if the file is empty
                if os.path.getsize(filename) == 0:
                    csv.writer(csv_file, delimiter=",").writerow(
                        [
                            "Customer ID",
                            "First Name",
                            "Last Name",
                            "City",
                            "Postal Code",
                            "Credit Card Number",
                            "Birth Date",
                        ]
                    )

                csv.writer(csv_file).writerows(content)
                # Update expected path
                expected_path = Path(os.path.expanduser(f"~/Documents/{filename}"))
                content.clear()
        except FileNotFoundError:
            # Create the file if it is not existing previously
            open(
                file=filename, mode="w", newline="", encoding="utf-8", errors="replace"
            ).close()

            # Update expected path as there is a data file created now
            expected_path = Path(os.path.expanduser(f"~/Documents/{filename}"))
    else:
        raise GUIError(
            "Please enter customer information before using this function")


escalator_music("escalator music.ogg")

