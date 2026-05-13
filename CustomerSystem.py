import csv
import os
import subprocess
import time

customerInfo = list()

# Get line count to get amount of customer
try:
    customer_info_file = open(file="customer_info.csv", mode='r', newline='', encoding='utf-8', errors='replace')
except FileNotFoundError:
    customer_info_file = open("customer_info.csv", mode='w+', newline='', encoding='utf-8', errors='replace')

customer_number = sum(1 for line in customer_info_file)

customer_number += 1 if customer_number == 0 else 0

customer_info_file.close()


def printMenu() -> None:
    """
    Print the menu options for the Customer System
    """

    clearScreen()

    print('''
          Customer and Sales System\n
          1. Enter Customer Information\n
          2. Generate Customer data file\n
          3. Report on total Sales (Not done in this part)\n
          4. Check for fraud in sales data (Not done in this part)\n
          9. Quit\n
          Enter menu option (1-9)
          ''')


def clearScreen() -> None:
    """
    Helper function to clear screen on terminal
    """
    subprocess.call(["cls" if os.name == "nt" else "clear"])


def parseCSV(file: str) -> list[str]:
    """
    Parse a CSV file and return into a list of rows in a list of CSV values
    """

    with open(file=file, mode='r', newline='', encoding='utf-8', errors='replace') as csv_file:
        # Take the file and separate with |
        csv_data = list(csv.reader(csv_file, delimiter="|"))

        # Remove header
        csv_data.pop(0)

        csv_data = [row[0] for row in csv_data]
        return csv_data


def luhn_check(numbers: str) -> bool:
    """
    Check if the numbers are valid through the luhn algorithm
    """

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

def enterCustomerInfo() -> None:
    """
    Provide a prompt for users to enter customer information
    """

    global customer_number

    clearScreen()

    # Create or read file
    try:
        customer_info_file = open(file="customer_info.csv", mode='r', newline='', encoding='utf-8', errors='replace')
    except FileNotFoundError:
        customer_info_file = open("customer_info.csv", mode='w+', newline='', encoding='utf-8', errors='replace')

    print(f"Customer number: {customer_number}")

    while True:
        firstName = input("Please enter first name: ")
        if firstName != "":
            break
        else:
            print("Please enter your first name")

    while True:
        lastName = input("Please enter last name: ")
        if lastName != "":
            break
        else:
            print("Please enter your last name")

    while True:
        city = input("Please enter city: ")
        if city != "":
            break
        else:
            print("Please enter your city")

    while True:
        postalCode = input("Please enter postal code: ")
        if validatePostalCode(postalCode):
            break
        else:
            print("Please enter a valid postal code")

    while True:
        credit_card_number = input("Please enter credit card number: ")
        if validateCreditCard(credit_card_number):
            break
        else:
            print("Please enter a valid credit card number")

    # Increment customer number by 1 after completing the operation
    name = f"{customer_number}{firstName.lower()[:2]}{lastName.lower()[:2]}"
    customerInfo.append([name, firstName.lower().capitalize(), lastName.lower().capitalize(), city.lower().capitalize(), postalCode.upper(), credit_card_number])
    customer_number += 1


def validatePostalCode(postal_code: str) -> bool:
    postalCodes = parseCSV("postal_codes.csv")
    return postal_code[:3].upper() in postalCodes


def validateCreditCard(credit_card_number: str) -> bool:
    return luhn_check(credit_card_number)


def generateCustomerDataFile(content: list[str], filename: str) -> None:
    if customerInfo:
        try:
            with open(file=filename, mode='a', newline='', encoding='utf-8', errors='replace') as csv_file:
                if os.path.getsize(filename) == 0:
                    csv.writer(csv_file, delimiter='|').writerow(["Customer ID", "First Name", "Last Name", "City", "Postal Code"])

                csv.writer(csv_file).writerows(content)
                content.clear()
        except FileNotFoundError:
            open(file=filename, mode='w', newline='', encoding='utf-8', errors='replace').close()
    else:
        print("Please enter customer information before using this function")
        time.sleep(1)

# Do not edit any of these variables
userInput = ""
enterCustomerOption = "1"
generateCustomerOption = "2"
exitCondition = "9"

while userInput != exitCondition:
    printMenu()
    userInput = input("-> ")

    if userInput == enterCustomerOption:
        enterCustomerInfo()

    elif userInput == generateCustomerOption:
        generateCustomerDataFile(customerInfo, "customer_info.csv")

    elif userInput == exitCondition:
        break

    else:
        print("\nPlease type in a valid option (A number from 1-9)")
        time.sleep(1)

#Exits once the user types
print("Program Terminated")
