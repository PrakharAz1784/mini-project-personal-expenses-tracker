# expenses.py

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

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills", "Entertainment",
    "Education", "Health", "Travel", "Rent", "Groceries", "Other"
]

PAYMENT_METHODS = [
    "Cash", "UPI", "Debit Card", "Credit Card", "Bank Transfer"
]


# ============================================================
# EXPENSE WINDOW
# ============================================================

class ExpenseManager:

    def __init__(self, parent):

        self.parent = parent
        self.selected_id = None

        self.window = tk.Frame(parent, bg=BG)
        self.window.pack(fill="both", expand=True)

        # Form variables
        self.date_var = tk.StringVar(value=str(date.today()))
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.payment_var = tk.StringVar(value="UPI")
        self.description_var = tk.StringVar()

        # Build UI
        self.create_header()
        self.create_form()
        self.create_table()

        self.load_expenses()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(self.window, bg="#1f2937", height=65)
        header.pack(fill="x")

        tk.Label(
            header, text="EXPENSE MANAGEMENT",
            font=("Segoe UI", 20, "bold"),
            bg="#1f2937", fg="white"
        ).pack(side="left", padx=25, pady=15)


    # ========================================================
    # FORM
    # ========================================================

    def create_form(self):

        form_container = tk.Frame(self.window, bg=BG)
        form_container.pack(fill="x", padx=20, pady=20)

        form = tk.LabelFrame(
            form_container,
            text="Add / Edit Expense",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=15, pady=15
        )
        form.pack(fill="x")

        self.date_entry = ttk.Entry(
            form, textvariable=self.date_var, width=20
        )
        self.category_entry = ttk.Combobox(
            form, textvariable=self.category_var,
            values=CATEGORIES, width=18
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
            ("Category", self.category_entry),
            ("Amount", self.amount_entry),
            ("Payment Method", self.payment_entry),
            ("Description", self.description_entry),
        ]):
            tk.Label(
                form, text=label, bg="white", font=("Segoe UI", 10)
            ).grid(row=0, column=column, sticky="w", padx=8, pady=5)

            widget.grid(row=1, column=column, padx=8, pady=5)

        # Buttons
        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(row=2, column=0, columnspan=5, pady=15)

        for text, command in [
            ("➕ Add Expense", self.add_expense),
            ("✏ Update", self.update_expense),
            ("🗑 Delete", self.delete_expense),
            ("🔄 Clear", self.clear_form),
        ]:
            ttk.Button(
                button_frame, text=text, command=command
            ).pack(side="left", padx=5)


    # ========================================================
    # TABLE
    # ========================================================

    def create_table(self):

        table_container = tk.Frame(self.window, bg=BG)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(
            table_container, text="Expense History",
            font=("Segoe UI", 13, "bold"), bg=BG
        ).pack(anchor="w", pady=(0, 8))

        # (name, width, anchor)
        columns = [
            ("ID", 60, "center"),
            ("Date", 120, "center"),
            ("Category", 150, "w"),
            ("Amount", 120, "e"),
            ("Payment", 140, "w"),
            ("Description", 250, "w"),
        ]

        self.tree = ttk.Treeview(
            table_container,
            columns=[name for name, _, _ in columns],
            show="headings"
        )

        for name, width, anchor in columns:
            self.tree.heading(name, text=name)
            self.tree.column(name, width=width, anchor=anchor)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_container, orient="vertical", command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.select_expense)


    # ========================================================
    # LOAD EXPENSES
    # ========================================================

    def load_expenses(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for expense in get_transactions_by_type("Expense"):
            self.tree.insert(
                "",
                "end",
                values=(
                    expense["id"],
                    expense["date"],
                    expense["category"],
                    f"₹{expense['amount']:,.2f}",
                    expense["payment"],
                    expense["description"]
                )
            )


    # ========================================================
    # HELPERS
    # ========================================================

    def read_form(self):
        """Return (date, category, amount, payment, description) as stripped text."""

        return (
            self.date_var.get().strip(),
            self.category_var.get().strip(),
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
            self.load_expenses()
        else:
            messagebox.showerror("Error", error_message)


    # ========================================================
    # ADD EXPENSE
    # ========================================================

    def add_expense(self):

        transaction_date, category, amount, payment, description = (
            self.read_form()
        )

        if not transaction_date:
            messagebox.showwarning("Missing Date", "Please enter a date.")
            return

        if not category:
            messagebox.showwarning(
                "Missing Category", "Please select a category."
            )
            return

        if not amount:
            messagebox.showwarning(
                "Missing Amount", "Please enter an amount."
            )
            return

        amount = self.parse_amount(
            amount, "Please enter a valid positive number."
        )

        if amount is None:
            return

        ok, _ = self.run_database(
            add_transaction,
            transaction_date, "Expense", category,
            amount, payment, description
        )

        if not ok:
            return

        messagebox.showinfo("Success", "Expense added successfully.")

        self.clear_form()
        self.load_expenses()


    # ========================================================
    # SELECT EXPENSE
    # ========================================================

    def select_expense(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        if not values:
            return

        self.selected_id = values[0]

        self.date_var.set(values[1])
        self.category_var.set(values[2])
        self.amount_var.set(
            str(values[3]).replace("₹", "").replace(",", "")
        )
        self.payment_var.set(values[4])
        self.description_var.set(values[5])


    # ========================================================
    # UPDATE EXPENSE
    # ========================================================

    def update_expense(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select Expense", "Please select an expense to update."
            )
            return

        transaction_date, category, amount, payment, description = (
            self.read_form()
        )

        if not transaction_date or not category:
            messagebox.showwarning(
                "Missing Information", "Please enter date and category."
            )
            return

        amount = self.parse_amount(amount, "Please enter a valid amount.")

        if amount is None:
            return

        ok, success = self.run_database(
            update_transaction,
            self.selected_id, transaction_date, "Expense",
            category, amount, payment, description
        )

        if not ok:
            return

        self.finish(
            success,
            "Updated",
            "Expense updated successfully.",
            "Expense could not be updated."
        )


    # ========================================================
    # DELETE EXPENSE
    # ========================================================

    def delete_expense(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select Expense", "Please select an expense to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        ok, success = self.run_database(delete_transaction, self.selected_id)

        if not ok:
            return

        self.finish(
            success,
            "Deleted",
            "Expense deleted successfully.",
            "Expense could not be deleted."
        )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_id = None

        self.date_var.set(str(date.today()))
        self.category_var.set("")
        self.amount_var.set("")
        self.payment_var.set("UPI")
        self.description_var.set("")

        # Remove table selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Expense Management")
    root.geometry("1100x650")

    ExpenseManager(root)

    root.mainloop()