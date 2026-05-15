import os.path
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

import sys
import sv_ttk

import backend


# GUI
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Tkinter Window Title
        self.title("Customer System")

        # Unresizable
        self.resizable(False, False)

        # Put the window in the middle
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (700 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.geometry(f"{700}x{600}+{x}+{y - 50}")

        # Force focus
        self.focus_force()

        # All UI Elements
        self._build_ui()

        # Press esc to exit
        self.bind("<Escape>", self._on_escape)

    def _build_ui(self):
        # Segoe UI Font
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI Variable",
                               size=15, weight="normal")

        # Tab creation
        self.notebook1 = ttk.Notebook(self)
        self.notebook1.place(x=0, y=0, width=700, height=600)
        self._tab_notebook1_0 = tk.Frame(self.notebook1)
        self.notebook1.add(self._tab_notebook1_0,
                           text="Enter Customer Information")
        self._tab_notebook1_1 = tk.Frame(self.notebook1)
        self.notebook1.add(self._tab_notebook1_1,
                           text="Generate Customer File")

        # Entry creations
        self.firstNameLabel = tk.Label(
            self._tab_notebook1_0, text="First Name")
        self.firstNameLabel.place(x=56, y=42)

        self.firstName = ttk.Entry(self._tab_notebook1_0)
        self.firstName.place(x=176, y=32, width=448, height=50)

        self.lastNameLabel = tk.Label(self._tab_notebook1_0, text="Last Name")
        self.lastNameLabel.place(x=56, y=112)

        self.lastName = ttk.Entry(self._tab_notebook1_0)
        self.lastName.place(x=176, y=102, width=448, height=50)

        self.cityLabel = tk.Label(self._tab_notebook1_0, text="City")
        self.cityLabel.place(x=56, y=182)

        self.city = ttk.Entry(self._tab_notebook1_0)
        self.city.place(x=176, y=172, width=448, height=50)

        self.postalCodeLabel = tk.Label(
            self._tab_notebook1_0, text="Postal Code")
        self.postalCodeLabel.place(x=56, y=252)

        self.postalCode = ttk.Entry(self._tab_notebook1_0)
        self.postalCode.place(x=176, y=242, width=448, height=50)

        self.creditCardNumberLabel = tk.Label(
            self._tab_notebook1_0, text="Card Number")
        self.creditCardNumberLabel.place(x=56, y=322)

        self.creditCardNumber = ttk.Entry(self._tab_notebook1_0)
        self.creditCardNumber.place(x=176, y=312, width=448, height=50)

        self.birthDateLabel = tk.Label(
            self._tab_notebook1_0, text="Birth Date\n (YYYY-MM-DD)")
        self.birthDateLabel.place(x=40, y=380)

        self.birthDate = ttk.Entry(self._tab_notebook1_0)
        self.birthDate.place(x=176, y=382, width=448, height=50)

        # Button creation
        self.submitButton = ttk.Button(
            self._tab_notebook1_0,
            text="Submit",
            default="active",
            takefocus=False,
            command=self._confirm_button_action,
            style="Accent.TButton"
        )
        self.submitButton.place(x=176, y=452, width=448, height=30)

        self.generateCustomerInfoButton = ttk.Button(
            self._tab_notebook1_1,
            text="Generate Customer File",
            takefocus=False,
            command=self._generate_button_action,
            style="Accent.TButton"
        )
        self.generateCustomerInfoButton.place(
            x=125, y=100, width=448, height=100)

        self.customerInfoLocationTipLabel = ttk.Label(self._tab_notebook1_1,
                                                      text="Customer Info Location:\n ~/Documents/customer_info.csv")
        self.customerInfoLocationTipLabel.place(x=125, y=200, width=448, height=50)

    # Methods

    # Verify if an entry is empty
    @staticmethod
    def _validate_empty(self, content):
        return content != ""

    # Handler to handle esc button pressed, should exit application
    @staticmethod
    def _on_escape(event=None):
        sys.exit(0)

    # Button handler for the confirm button to submit form
    def _confirm_button_action(self):
        try:
            backend.enterCustomerInfo(
                self.firstName.get().strip(),
                self.lastName.get().strip(),
                self.city.get().strip(),
                self.postalCode.get().strip(),
                self.creditCardNumber.get().strip(),
                self.birthDate.get().strip()
            )
        except backend.GUIError as e:
            messagebox.showerror(title="Error", message=f"{e}")
        else:
            self.firstName.delete(0, "end")
            self.lastName.delete(0, "end")
            self.city.delete(0, "end")
            self.postalCode.delete(0, "end")
            self.creditCardNumber.delete(0, "end")
            self.birthDate.delete(0, "end")

    # Button handler for the generate data file button
    def _generate_button_action(self):
        try:
            backend.generateCustomerDataFile(
                backend.customerInfo, os.path.expanduser("~/Documents/customer_info.csv"))
        except backend.GUIError as e:
            messagebox.showerror(title="Error", message=f"{e}")


if __name__ == "__main__":
    app = GUI()
    sv_ttk.set_theme("dark")
    app.mainloop()

