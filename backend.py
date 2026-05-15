import csv
import os
import sys
import subprocess
from datetime import datetime

import pygame
import pygame.mixer

# Music playback
def escalator_music(filepath: str):
    pygame.mixer.init()
    if "__compiled__" in globals():
        filepath = f"{os.path.dirname(sys.executable)}/{filepath}"
        print(f"[DEBUG] Audio Subsystem - Detected Nuitka Compiled Application, using {filepath} instead")
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

# Input Error Messages
class GUIError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Customer info is a list that stores all customer information
# before user generate the data file, which would then clear it
customerInfo = list()


# Get line count to get amount of customer

# Stores in the User Documents folder as it is packaged as an application
# and would not be viable to store it internally inside the Temp folder
# for the executable or in an obscured folder
try:
    customer_info_file = open(
        file=os.path.expanduser("~/Documents/customer_info.csv"),
        mode="r",
        newline="",
        encoding="utf-8",
        errors="replace",
    )
except FileNotFoundError:
    customer_info_file = open(
        os.path.expanduser("~/Documents/customer_info.csv"), mode="w+", newline="", encoding="utf-8", errors="replace"
    )
customer_number = sum(1 for line in customer_info_file)
customer_number += 1 if customer_number == 0 else 0
customer_info_file.close()


# Called by main application
def printMenu() -> None:
    """
    Print the menu options for the Customer System
    """

    clearScreen()

    print("""
          Customer and Sales System\n
          1. Enter Customer Information\n
          2. Generate Customer data file\n
          3. Report on total Sales (Not done in this part)\n
          4. Check for fraud in sales data (Not done in this part)\n
          9. Quit\n
          Enter menu option (1-9)
          """)


# Called by printMenu() and enterCustomerInfo()
def clearScreen() -> None:
    """
    Helper function to clear screen on terminal
    """
    subprocess.call(["cls" if os.name == "nt" else "clear"])


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
    firstName: str, lastName: str, city: str, postalCode: str, credit_card_number: str, birth_date: str
):
    """
    Provide a prompt for users to enter customer information
    """

    global customer_number

    clearScreen()

    # Create or read file
    try:
        customer_info_file = open(
            file=os.path.expanduser("~/Documents/customer_info.csv"),
            mode="r",
            newline="",
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        customer_info_file = open(
            os.path.expanduser("~/Documents/customer_info.csv"),
            mode="w+",
            newline="",
            encoding="utf-8",
            errors="replace",
        )

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
            birth_date
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
            path = os.path.dirname(sys.executable)+"/postal_codes.csv"
            print(f"[DEBUG] CSV Parse - Detected Nuitka Compiled Application, using {path} instead")
        else:
            path = "postal_codes.csv"
        postalCodes = parseCSV(path)
    except FileNotFoundError:
        raise GUIError("Please check if postal_codes.csv exists")
    return postal_code[:3].upper() in postalCodes


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
        if (len(birth_date) != 10
            or birth_date[4] != '-'
            or birth_date[7] != '-'
        ):
            return False

        # Year
        if (not birth_date[:4].isdigit()
            or not int(birth_date[:4])>0
            or not int(birth_date[:4])<=current_year
        ):
            raise GUIError("Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect year")

        # Month
        if (not birth_date[5:7].isdigit()
            or not int(birth_date[5:7])>0
            or not int(birth_date[5:7])<13
        ):
            raise GUIError("Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect month")

        # Date
        if (not birth_date[8:10].isdigit()
            or not int(birth_date[8:10])>0
            or not int(birth_date[8:10])<32
        ):
            raise GUIError("Please enter a valid birth date\n(YYYY-MM-DD)\n\nIncorrect date")

       # More than current date
        if (int(birth_date[:4]) == current_year
            and int(birth_date[5:7]) > current_month

            or int(birth_date[:4]) == current_year
            and int(birth_date[5:7]) == current_month
            and int(birth_date[8:10]) > current_day
        ):
            raise GUIError("Please enter a valid birth date\n(YYYY-MM-DD)\n\nDate higher than today's date")

        return True
    except ValueError:
        return False
    except GUIError as e:
        raise e


# Called by GUI through notebook1_1
def generateCustomerDataFile(content: list[str], filename: str):
    if customerInfo:
        try:
            with open(
                file=filename, mode="a", newline="", encoding="utf-8", errors="replace"
            ) as csv_file:
                if os.path.getsize(filename) == 0:
                    csv.writer(csv_file, delimiter=",").writerow(
                        [
                            "Customer ID",
                            "First Name",
                            "Last Name",
                            "City",
                            "Postal Code",
                            "Credit Card Number",
                            "Birth Date"
                        ]
                    )

                csv.writer(csv_file).writerows(content)
                content.clear()
        except FileNotFoundError:
            open(
                file=filename, mode="w", newline="", encoding="utf-8", errors="replace"
            ).close()
    else:
        raise GUIError(
            "Please enter customer information before using this function")


escalator_music("escalator music.mp3")