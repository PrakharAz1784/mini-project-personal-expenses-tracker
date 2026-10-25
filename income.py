# income.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import (
    add_transaction,
    update_transaction,
    delete_transaction,
    get_transactions_by_type
)


# ============================================================
# CONSTANTS
# ============================================================

BG = "#f5f7fb"

INCOME_SOURCES = [
    "Salary", "Freelance", "Business", "Investment", "Bonus",
    "Interest", "Gift", "Refund", "Other"
]

PAYMENT_METHODS = [
    "Cash", "UPI", "Debit Card", "Credit Card", "Bank Transfer", "Cheque"
]

DEFAULT_PAYMENT = "Bank Transfer"


# ============================================================
# INCOME MANAGEMENT
# ============================================================

class IncomeManager:

    def __init__(self, parent):

        self.parent = parent
        self.selected_id = None

        self.window = tk.Frame(parent, bg=BG)
        self.window.pack(fill="both", expand=True)

        # Form variables
        self.date_var = tk.StringVar(value=str(date.today()))
        self.source_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.payment_var = tk.StringVar(value=DEFAULT_PAYMENT)
        self.description_var = tk.StringVar()

        # Build interface
        self.create_header()
        self.create_form()
        self.create_table()

        self.load_income()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(self.window, bg="#1f2937", height=65)
        header.pack(fill="x")

        tk.Label(
            header, text="INCOME MANAGEMENT",
            font=("Segoe UI", 20, "bold"),
            fg="white", bg="#1f2937"
        ).pack(side="left", padx=25, pady=15)


    # ========================================================
    # FORM
    # ========================================================

    def create_form(self):

        container = tk.Frame(self.window, bg=BG)
        container.pack(fill="x", padx=20, pady=20)

        form = tk.LabelFrame(
            container,
            text="Add / Edit Income",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=15, pady=15
        )
        form.pack(fill="x")

        self.date_entry = ttk.Entry(
            form, textvariable=self.date_var, width=20
        )
        self.source_entry = ttk.Combobox(
            form, textvariable=self.source_var,
            values=INCOME_SOURCES, width=18
        )
        self.amount_entry = ttk.Entry(
            form, textvariable=self.amount_var, width=20
        )
        self.payment_entry = ttk.Combobox(
            form, textvariable=self.payment_var,
            values=PAYMENT_METHODS, state="readonly", width=18
        )
        self.description_entry = ttk.Entry(
            form, textvariable=self.description_var, width=25
        )

        for column, (label, widget) in enumerate([
            ("Date", self.date_entry),
            ("Income Source", self.source_entry),
            ("Amount", self.amount_entry),
            ("Payment Method", self.payment_entry),
            ("Description", self.description_entry),
        ]):
            tk.Label(
                form, text=label, font=("Segoe UI", 10), bg="white"
            ).grid(row=0, column=column, sticky="w", padx=8, pady=5)

            widget.grid(row=1, column=column, padx=8, pady=5)

        # Buttons
        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(row=2, column=0, columnspan=5, pady=15)

        for text, command in [
            ("➕ Add Income", self.add_income),
            ("✏ Update", self.update_income),
            ("🗑 Delete", self.delete_income),
            ("🔄 Clear", self.clear_form),
        ]:
            ttk.Button(
                button_frame, text=text, command=command
            ).pack(side="left", padx=5)


    # ========================================================
    # TABLE
    # ========================================================

    def create_table(self):

        container = tk.Frame(self.window, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(
            container, text="Income History",
            font=("Segoe UI", 13, "bold"), bg=BG
        ).pack(anchor="w", pady=(0, 8))

        # (name, width, anchor)
        columns = [
            ("ID", 60, "center"),
            ("Date", 120, "center"),
            ("Source", 160, "w"),
            ("Amount", 130, "e"),
            ("Payment", 150, "w"),
            ("Description", 260, "w"),
        ]

        self.tree = ttk.Treeview(
            container,
            columns=[name for name, _, _ in columns],
            show="headings"
        )

        for name, width, anchor in columns:
            self.tree.heading(name, text=name)
            self.tree.column(name, width=width, anchor=anchor)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.select_income)


    # ========================================================
    # LOAD INCOME
    # ========================================================

    def load_income(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for income in get_transactions_by_type("Income"):
            self.tree.insert(
                "",
                "end",
                values=(
                    income["id"],
                    income["date"],
                    income["category"],
                    f"₹{income['amount']:,.2f}",
                    income["payment"],
                    income["description"]
                )
            )


    # ========================================================
    # HELPERS
    # ========================================================

    def read_form(self):
        """Return (date, source, amount, payment, description) as stripped text."""

        return (
            self.date_var.get().strip(),
            self.source_var.get().strip(),
            self.amount_var.get().strip(),
            self.payment_var.get().strip(),
            self.description_var.get().strip(),
        )


    def parse_amount(self, text, error_message):
        """Return the amount as a positive float, or None after showing an error."""

        try:
            amount = float(text)

            if amount <= 0:
                raise ValueError

            return amount

        except ValueError:
            messagebox.showerror("Invalid Amount", error_message)
            return None


    def run_database(self, function, *args):
        """Call a database function. Returns (ok, result); shows an error if it fails."""

        try:
            return True, function(*args)

        except Exception as error:
            messagebox.showerror("Database Error", str(error))
            return False, None


    def finish(self, success, title, success_message, error_message):
        """Show the result of an update/delete, then reset the form and table."""

        if success:
            messagebox.showinfo(title, success_message)
            self.clear_form()
            self.load_income()
        else:
            messagebox.showerror("Error", error_message)


    # ========================================================
    # ADD INCOME
    # ========================================================

    def add_income(self):

        transaction_date, source, amount, payment, description = (
            self.read_form()
        )

        if not transaction_date:
            messagebox.showwarning("Missing Date", "Please enter a date.")
            return

        if not source:
            messagebox.showwarning(
                "Missing Source", "Please select an income source."
            )
            return

        if not amount:
            messagebox.showwarning(
                "Missing Amount", "Please enter an amount."
            )
            return

        amount = self.parse_amount(
            amount, "Please enter a valid positive amount."
        )

        if amount is None:
            return

        ok, _ = self.run_database(
            add_transaction,
            transaction_date, "Income", source,
            amount, payment, description
        )

        if not ok:
            return

        messagebox.showinfo("Success", "Income added successfully.")

        self.clear_form()
        self.load_income()


    # ========================================================
    # SELECT INCOME
    # ========================================================

    def select_income(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        if not values:
            return

        self.selected_id = values[0]

        self.date_var.set(values[1])
        self.source_var.set(values[2])
        self.amount_var.set(
            str(values[3]).replace("₹", "").replace(",", "")
        )
        self.payment_var.set(values[4])
        self.description_var.set(values[5])


    # ========================================================
    # UPDATE INCOME
    # ========================================================

    def update_income(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select Income",
                "Please select an income record to update."
            )
            return

        transaction_date, source, amount, payment, description = (
            self.read_form()
        )

        if not transaction_date or not source:
            messagebox.showwarning(
                "Missing Information",
                "Please enter date and income source."
            )
            return

        amount = self.parse_amount(amount, "Please enter a valid amount.")

        if amount is None:
            return

        ok, success = self.run_database(
            update_transaction,
            self.selected_id, transaction_date, "Income",
            source, amount, payment, description
        )

        if not ok:
            return

        self.finish(
            success,
            "Updated",
            "Income updated successfully.",
            "Income could not be updated."
        )


    # ========================================================
    # DELETE INCOME
    # ========================================================

    def delete_income(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select Income",
                "Please select an income record to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this income?"
        )

        if not confirm:
            return

        ok, success = self.run_database(delete_transaction, self.selected_id)

        if not ok:
            return

        self.finish(
            success,
            "Deleted",
            "Income deleted successfully.",
            "Income could not be deleted."
        )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_id = None

        self.date_var.set(str(date.today()))
        self.source_var.set("")
        self.amount_var.set("")
        self.payment_var.set(DEFAULT_PAYMENT)
        self.description_var.set("")

        # Clear table selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Income Management")
    root.geometry("1100x650")

    IncomeManager(root)

    root.mainloop()