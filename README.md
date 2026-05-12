# luhning-it

---

# Customer Information & Sales System (Luhn Algorithm)

## 📋 Business Overview

This project is a robust, modular Python application designed for a Canadian retail company to manage customer data and validate sensitive information. The system focuses on ensuring data integrity through custom validation rules for Canadian postal codes and credit card numbers using the **Luhn Algorithm**.

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

* `Main.java` / `main.py`: The driver of the application containing the menu interface.
* `Customer`: Class/Module handling customer attributes and ID generation logic.
* `Validator`: Contains static methods for Postal Code file checking and the Luhn Algorithm.
* `postal_codes.csv`: Reference file for Canadian postal regions.

---

## 📝 Requirements & Validation Rules

### Customer Input

| Field | Requirement | Validation Rule |
| --- | --- | --- |
| **First/Last Name** | String | Required |
| **Postal Code** | String | Min 3 chars; Must exist in `postal_codes.csv` |
| **Credit Card** | String | Min 9 digits; Must pass Luhn Check |

### ID Generation Pattern

The system generates IDs based on the sequence and name:
`[Sequence Number][First 2 of First Name][First 2 of Last Name]`

* *Example:* Will Smith (1st entry) → `1wism`
* *Example:* Will Smith (2nd entry) → `2wism`

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/luhn-customer-system.git

```


2. **Ensure `postal_codes.csv` is in the root directory.**
3. **Run the application:**

```bash
    javac Main.java && java Main  # For Java
    python main.py                # For Python
    ```
4.  **Exporting Data:** Choose option `2` in the menu to save your data to a custom `.csv` file.

---

## 🛠️ Technical Standards
*   **Modularity:** Logic is separated into distinct functions to allow concurrent development and easier testing.
*   **Documentation:** All methods include Javadoc/Docstring style headers explaining inputs, outputs, and dependencies.
*   **Error Handling:** Includes checks for file availability and invalid keyboard inputs.

---
*Note: This project was developed as part of a technical assignment to demonstrate proficiency in data validation and modular software design.*

```
