import csv

number = int()
customerInfo = list()

def printMenu() -> None:
    """
    Print the menu options for the Customer System
    """
    print('''
          Customer and Sales System\n
          1. Enter Customer Information\n
          2. Generate Customer data file\n
          3. Report on total Sales (Not done in this part)\n
          4. Check for fraud in sales data (Not done in this part)\n
          9. Quit\n
          Enter menu option (1-9)
          ''')
    

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

    # Initial variable to store the total for the check
    total = 0

    # Luhn algorithm - Step 1: Get last digit
    last_digit = numbers[-1]

    # Luhn algorithm - Step 2: Remove last digit
    numbers = numbers[:-1]

    # Luhn algorithm - Step 3: Loop through all the numbers and double every second digit
    for i, number in enumerate(reversed(numbers)):
        # Numbers that are doubled
        if i % 2 == 0:
            number = int(number) * 2

            # If doubled numbers are more than 9, make them single digit
            if number > 9:
                string_number = str(number)
                number = int(string_number[0]) + int(string_number[1])

            total += number
        else:
            # Numbers that aren't doubled
            total += int(number)

    # Luhn algorithm - Step 4: Check with modulo 10 with the excluded last digit
    # If it is 0, then it is valid through the Luhn Algorithm
    return (total + int(last_digit)) % 10 == 0


def enterCustomerInfo() -> None:
    """
    Provide a prompt for users to enter customer information
    """
    global number

    firstName = input("Please enter first name: ")
    lastName = input("Please enter last name: ")
    city = input("Please enter city: ")

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

    name = f"{number}{firstName[:2]}{lastName[:2]}"

    customerInfo.append([credit_card_number])



def validatePostalCode(postal_code: str) -> bool:
    postalCodes = parseCSV("postal_codes.csv")
    return postal_code[:3].upper() in postalCodes


def validateCreditCard(credit_card_number: str) -> bool:
    return luhn_check(credit_card_number)


def generateCustomerDataFile(content: list[str], filename: str, location: str) -> None:
    with open(file=filename, mode='w', newline='', encoding='utf-8', errors='replace') as csv_file:
        csv.writer(csv_file).writerows(content)


# Do not edit any of these variables
userInput = ""
enterCustomerOption = "1"
generateCustomerOption = "2"
exitCondition = "9"

# More variables for the main may be declared in the space below
#TODO: Move this to the function for checking postal codes after done making it


while userInput != exitCondition:
    printMenu()                 # Printing out the main menu
    userInput = input()        # User selection from the menu

    if userInput == enterCustomerOption:
        # Only the line below may be edited based on the parameter list and how you design the method return
        # Any necessary variables may be added to this if section, but nowhere else in the code
        enterCustomerInfo()

    elif userInput == generateCustomerOption:
        # Only the line below may be edited based on the parameter list and how you design the method return
        generateCustomerDataFile()

    else:
        print("Please type in a valid option (A number from 1-9)")

#Exits once the user types
print("Program Terminated")