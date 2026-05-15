# luhning-it

---

# Customer Information & Sales System (Luhn Algorithm)

## 📋 Business Overview

This project is a robust, modular Python application designed to manage customer data and validate sensitive information. The system focuses on ensuring data integrity through custom validation rules for Canadian postal codes and credit card numbers using the **Luhn Algorithm**.

## 🚀 Features

* **Unique ID Generation:** Automatically generates a unique identifier for every customer (e.g., `1wism`, `2wism`, `3jodo`).
* **Postal Code Validation:** Cross-references the first three characters of a postal code against a localized database (`postal_codes.csv`).
* **Credit Card Validation:** Implements the **Luhn Algorithm** to detect accidental data entry errors.
* **Data Export:** Generates a sanitized CSV output file containing all validated customer records.

---

## 🛠️ The Luhn Algorithm Implementation

The core of the security validation is the Luhn Algorithm, a checksum formula used to validate various identification numbers.

### Logic Flow:

1. **Reverse:** The credit card string is reversed.
2. **Sum Odd Positions:** Sum the digits in the 1st, 3rd, 5th, etc., positions ($sum_1$).
3. **Process Even Positions:**
* Multiply digits in the 2nd, 4th, 6th, etc., positions by 2.
* If the result is $> 9$, sum the two digits of the result (e.g., $16 \rightarrow 1 + 6 = 7$).
* Sum these partial values ($sum_2$).


4. **Final Check:** If $(sum_1 + sum_2) \pmod{10} == 0$, the card is valid.

---

## 📂 Project Structure

* `main.py`: The driver of the application containing the menu interface.
* `postal_codes.csv`: Reference file for Canadian postal regions.

---

## 📝 Validation Rules

### ID Generation Pattern

The system generates IDs based on the sequence and name:
`[Sequence Number][First 2 of First Name][First 2 of Last Name]`

* *Example:* Will Smith (1st entry) → `1wism`
* *Example:* Will Smith (2nd entry) → `2wism`

---

## ⚙️ Installation & Usage
* Go to GitHub Actions and retrieve the latest version of artifacts for the appropriate operating system.
