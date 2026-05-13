# Throughout this project, the use of data structures are not permitted
# Minimal built in functions are to be used and the majority of functions must be
# created yourself

# More packages may be imported in the space below if approved by your instructor
import csv

def printMenu():
    print('''
    Customer and Sales System\n
       1. Enter Customer Information\n
       2. Generate Customer data file\n
       3. Report on total Sales (Not done in this part)\n
       4. Check for fraud in sales data (Not done in this part)\n
       9. Quit\n
       Enter menu option (1-9)
          ''')
    

def parseCSV(file):
    with open(file=file, mode='r', newline='', encoding='utf-8', errors='replace') as csv_file:
        # Take the file and separate with |
        csv_data = list(csv.reader(csv_file, delimiter="|"))

        # Remove header
        csv_data.pop(0)

        csv_data = [row[0] for row in csv_data]
        return csv_data


def luhn_check(numbers):
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


'''
    This function is to be edited to achieve the task.
    It is your decision to make this function a procedural or functional type
    You may place as many or as few parameters as needed
    This function may also be broken down further depending on your algorithm/approach
'''
def enterCustomerInfo():
    first_name_valid = False
    last_name_valid = False
    postal_code_valid = False
    credit_card_valid = False
    date_of_birth_valid = False

    while first_name_valid == False:
        FirstName = input("Enter customer's first name\n: ")
        if FirstName.strip() == "":
             print("Invalid first name. Please try again.")
        elif " " in FirstName:
             print("Invalid first name. Please try again.")
        else:
             first_name_valid = True

    while last_name_valid == False:
        LastName = input("Enter customer's last name\n: ")
        if LastName.strip() == "":
            print("Invalid last name. Please try again.")
        elif " " in LastName:
            print("Invalid last name. Please try again.")
        else:
            last_name_valid = True

    #City = input("Enter customer's city\n: ") - Do we need this?

    while date_of_birth_valid == False:
        DateOfBirth = input("Enter customer's date of birth (YYYY-MM-DD)\n: ")
        if len(DateOfBirth) != 10:
            print("Invalid date of birth. Please try again.")
        elif DateOfBirth[4] != '-' or DateOfBirth[7] != '-':
            print("Invalid date of birth. Please try again.")
        else:
            date_of_birth_valid = True

    Adress = input("Enter customer's address\n: ")
    #idk what to do with address rn

    while postal_code_valid == False:
        PostalCode = input("Enter customer's postal code\n: ")
        if len(PostalCode) < 3:
            print("Invalid postal code. Please try again.")
        elif validatePostalCode(PostalCode, postalCodes) == False:
            print("Invalid postal code. Please try again.")
        else:
            postal_code_valid = True

    while credit_card_valid == False:
        CreditCardNumber = input("Enter customer's credit card number\n: ")
        if len(CreditCardNumber) < 9:
            print("Invalid credit card number. Please try again.")
        #elif validateCreditCard(CreditCardNumber) == False:
            #print("Invalid credit card number. Please try again.")
        else:
            credit_card_valid = True

'''
    This function is to be edited to achieve the task.
    It is your decision to make this function a procedural or functional type
    You may place as many or as few parameters as needed
    This function may also be broken down further depending on your algorithm/approach
'''
def validatePostalCode(postal_code, valid_list):
    # Rules: Min 3 chars, and first 3 must match the provided CSV list.
    if len(postal_code) < 3:
        return False
    
    prefix = postal_code[:3].upper()
    return prefix in valid_list

'''
    This function is to be edited to achieve the task.
    It is your decision to make this function a procedural or functional type
    You may place as many or as few parameters as needed
    This function may also be broken down further depending on your algorithm/approach
'''
def validateCreditCard():
    pass    # Remove this pass statement and add your own code below

'''
    This function is to be edited to achieve the task.
    It is your decision to make this function a procedural or functional type
    You may place as many or as few parameters as needed
    This function may also be broken down further depending on your algorithm/approach
'''
def generateCustomerDataFile():
    pass    # Remove this pass statement and add your own code below

####################################################################
#       ADDITIONAL METHODS MAY BE ADDED BELOW IF NECESSARY         #
####################################################################




####################################################################
#                            MAIN PROGRAM                          #
#           DO NOT EDIT ANY CODE EXCEPT WHERE INDICATED            #
####################################################################

# Do not edit any of these variables
userInput = ""
enterCustomerOption = "1"
generateCustomerOption = "2"
exitCondition = "9"

# More variables for the main may be declared in the space below
#TODO: Move this to the function for checking postal codes after done making it
postalCodes = parseCSV("postal_codes.csv")

while userInput != exitCondition:
    printMenu()                 # Printing out the main menu
    userInput = input(": ")   # User selection from the menu

    if userInput == enterCustomerOption:
        # Only the line below may be editted based on the parameter list and how you design the method return
        # Any necessary variables may be added to this if section, but nowhere else in the code
        enterCustomerInfo()

    elif userInput == generateCustomerOption:
        # Only the line below may be editted based on the parameter list and how you design the method return
        generateCustomerDataFile()

    else:
        print("Please type in a valid option (A number from 1-9)")

#Exits once the user types
print("Program Terminated")
