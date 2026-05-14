import csv
import os
import subprocess


# Input Error Messages
class GUIError(Exception):
    def __init__(self, message):
        super().__init__(message)


customerInfo = list()


# Get line count to get amount of customer
try:
    customer_info_file = open(
        file="customer_info.csv",
        mode="r",
        newline="",
        encoding="utf-8",
        errors="replace",
    )
except FileNotFoundError:
    customer_info_file = open(
        "customer_info.csv", mode="w+", newline="", encoding="utf-8", errors="replace"
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
    firstName: str, lastName: str, city: str, postalCode: str, credit_card_number: str
):
    """
    Provide a prompt for users to enter customer information
    """

    global customer_number

    clearScreen()

    # Create or read file
    try:
        customer_info_file = open(
            file="customer_info.csv",
            mode="r",
            newline="",
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        customer_info_file = open(
            "customer_info.csv",
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
        postalCodes = parseCSV("postal_codes.csv")
    except FileNotFoundError:
        raise GUIError("Please check if postal_codes.csv exists")
    return postal_code[:3].upper() in postalCodes


# Wrapper function to allow better descriptions for both functions
# Called by enterCustomerInfo()
def validateCreditCard(credit_card_number: str) -> bool:
    return luhn_check(credit_card_number)


# Called by GUI through notebook1_1
def generateCustomerDataFile(content: list[str], filename: str):
    if customerInfo:
        try:
            with open(
                file=filename, mode="a", newline="", encoding="utf-8", errors="replace"
            ) as csv_file:
                if os.path.getsize(filename) == 0:
                    csv.writer(csv_file, delimiter="|").writerow(
                        [
                            "Customer ID",
                            "First Name",
                            "Last Name",
                            "City",
                            "Postal Code",
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

