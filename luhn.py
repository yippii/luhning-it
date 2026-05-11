import sys

def luhn_check(numbers: str) -> bool:
    """
    Check if the numbers are valid through the luhn algorithm
    """

    # Initial variable to store the total for the check
    total = 0

    # Get rid of space or dashes
    valid_numbers = [int(number) for number in numbers if number.isdigit()]

    # Luhn algorithm - Step 1: Get last digit and remove it (skipped)
    last_digit = valid_numbers.pop()
    
    # Luhn algorithm - Step 2: Reverse the remaining numbers as it is relative
    # from the last digit
    valid_numbers.reverse()

    # Luhn algorithm - Step 3: Loop through all the numbers and double every second digit
    for i in range(len(valid_numbers)):
        # Numbers that are doubled
        if i % 2 == 0:
            valid_numbers[i] = valid_numbers[i] * 2

            # If doubled numbers are more than 9, make them single digit
            if valid_numbers[i] > 9:
                string_number = str(valid_numbers[i])
                valid_numbers[i] = int(string_number[0]) + int(string_number[1])

            total += valid_numbers[i]
        else:
            # Numbers that aren't doubled
            total += valid_numbers[i]

    # Luhn algorithm - Step 4: Check with modulo 10 with the excluded last digit
    # If it is 0, then it is valid through the Luhn Algorithm
    return (total + int(last_digit)) % 10 == 0


def customerInfo():
    pass


def generateData():
    pass


def reportSales():
    pass


def fraudDataCheck():
    pass


def main():
    print("Customer and Sales System")
    try:
        while True:
            print("1. Enter Customer Information")
            print("2. Generate Customer data file")
            print("3. Report on total Sales")
            print("4. Check for fraud in sales data")
            print("5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                customerInfo()
            elif choice == 2:
                generateData()
            elif choice == 3:
                reportSales()
            elif choice == 4:
                fraudDataCheck()
            elif choice == 5:
                sys.exit(0)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        main()
