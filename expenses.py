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
# EXPENSE WINDOW
# ============================================================

class ExpenseManager:

    def __init__(self, parent):

        self.parent = parent
        self.selected_id = None

        self.window = tk.Frame(
            parent,
            bg="#f5f7fb"
        )

        self.window.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.date_var = tk.StringVar(
            value=str(date.today())
        )

        self.category_var = tk.StringVar()

        self.amount_var = tk.StringVar()

        self.payment_var = tk.StringVar(
            value="UPI"
        )

        self.description_var = tk.StringVar()

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.create_header()
        self.create_form()
        self.create_table()

        self.load_expenses()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.window,
            bg="#1f2937",
            height=65
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="EXPENSE MANAGEMENT",
            font=("Segoe UI", 20, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            side="left",
            padx=25,
            pady=15
        )


    # ========================================================
    # FORM
    # ========================================================

    def create_form(self):

        form_container = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        form_container.pack(
            fill="x",
            padx=20,
            pady=20
        )

        form = tk.LabelFrame(
            form_container,
            text="Add / Edit Expense",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )

        form.pack(
            fill="x"
        )


        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Date",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=5
        )

        self.date_entry = ttk.Entry(
            form,
            textvariable=self.date_var,
            width=20
        )

        self.date_entry.grid(
            row=1,
            column=0,
            padx=8,
            pady=5
        )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Category",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=8,
            pady=5
        )

        self.category_entry = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Education",
                "Health",
                "Travel",
                "Rent",
                "Groceries",
                "Other"
            ],
            width=18
        )

        self.category_entry.grid(
            row=1,
            column=1,
            padx=8,
            pady=5
        )


        # ----------------------------------------------------
        # AMOUNT
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Amount",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=8,
            pady=5
        )

        self.amount_entry = ttk.Entry(
            form,
            textvariable=self.amount_var,
            width=20
        )

        self.amount_entry.grid(
            row=1,
            column=2,
            padx=8,
            pady=5
        )


        # ----------------------------------------------------
        # PAYMENT
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Payment Method",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=8,
            pady=5
        )

        self.payment_entry = ttk.Combobox(
            form,
            textvariable=self.payment_var,
            values=[
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Bank Transfer"
            ],
            state="readonly",
            width=18
        )

        self.payment_entry.grid(
            row=1,
            column=3,
            padx=8,
            pady=5
        )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Description",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=4,
            sticky="w",
            padx=8,
            pady=5
        )

        self.description_entry = ttk.Entry(
            form,
            textvariable=self.description_var,
            width=25
        )

        self.description_entry.grid(
            row=1,
            column=4,
            padx=8,
            pady=5
        )


        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            form,
            bg="white"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=5,
            pady=15
        )


        ttk.Button(
            button_frame,
            text="➕ Add Expense",
            command=self.add_expense
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            button_frame,
            text="✏ Update",
            command=self.update_expense
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            button_frame,
            text="🗑 Delete",
            command=self.delete_expense
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            button_frame,
            text="🔄 Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )


    # ========================================================
    # TABLE
    # ========================================================

    def create_table(self):

        table_container = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )


        title = tk.Label(
            table_container,
            text="Expense History",
            font=("Segoe UI", 13, "bold"),
            bg="#f5f7fb"
        )

        title.pack(
            anchor="w",
            pady=(0, 8)
        )


        columns = (
            "ID",
            "Date",
            "Category",
            "Amount",
            "Payment",
            "Description"
        )


        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )


        # ----------------------------------------------------
        # TABLE HEADINGS
        # ----------------------------------------------------

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )


        self.tree.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "Date",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Category",
            width=150
        )

        self.tree.column(
            "Amount",
            width=120,
            anchor="e"
        )

        self.tree.column(
            "Payment",
            width=140
        )

        self.tree.column(
            "Description",
            width=250
        )


        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )


        # Select transaction
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_expense
        )


    # ========================================================
    # LOAD EXPENSES
    # ========================================================

    def load_expenses(self):

        # Clear existing rows

        for row in self.tree.get_children():

            self.tree.delete(row)


        # Get expenses from database

        expenses = get_transactions_by_type(
            "Expense"
        )


        # Add rows

        for expense in expenses:

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
    # ADD EXPENSE
    # ========================================================

    def add_expense(self):

        transaction_date = self.date_var.get().strip()

        category = self.category_var.get().strip()

        amount = self.amount_var.get().strip()

        payment = self.payment_var.get().strip()

        description = self.description_var.get().strip()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not transaction_date:

            messagebox.showwarning(
                "Missing Date",
                "Please enter a date."
            )

            return


        if not category:

            messagebox.showwarning(
                "Missing Category",
                "Please select a category."
            )

            return


        if not amount:

            messagebox.showwarning(
                "Missing Amount",
                "Please enter an amount."
            )

            return


        try:

            amount = float(amount)

            if amount <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid positive number."
            )

            return


        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        try:

            add_transaction(
                transaction_date,
                "Expense",
                category,
                amount,
                payment,
                description
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return


        messagebox.showinfo(
            "Success",
            "Expense added successfully."
        )


        self.clear_form()

        self.load_expenses()


    # ========================================================
    # SELECT EXPENSE
    # ========================================================

    def select_expense(self, event=None):

        selected = self.tree.selection()

        if not selected:

            return


        item = self.tree.item(
            selected[0]
        )


        values = item["values"]


        if not values:

            return


        self.selected_id = values[0]


        # Date

        self.date_var.set(
            values[1]
        )


        # Category

        self.category_var.set(
            values[2]
        )


        # Amount

        amount = str(
            values[3]
        )

        amount = (
            amount
            .replace("₹", "")
            .replace(",", "")
        )

        self.amount_var.set(
            amount
        )


        # Payment

        self.payment_var.set(
            values[4]
        )


        # Description

        self.description_var.set(
            values[5]
        )


    # ========================================================
    # UPDATE EXPENSE
    # ========================================================

    def update_expense(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Expense",
                "Please select an expense to update."
            )

            return


        transaction_date = self.date_var.get().strip()

        category = self.category_var.get().strip()

        amount = self.amount_var.get().strip()

        payment = self.payment_var.get().strip()

        description = self.description_var.get().strip()


        if not transaction_date or not category:

            messagebox.showwarning(
                "Missing Information",
                "Please enter date and category."
            )

            return


        try:

            amount = float(amount)

            if amount <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount."
            )

            return


        try:

            success = update_transaction(
                self.selected_id,
                transaction_date,
                "Expense",
                category,
                amount,
                payment,
                description
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return


        if success:

            messagebox.showinfo(
                "Updated",
                "Expense updated successfully."
            )

            self.clear_form()

            self.load_expenses()

        else:

            messagebox.showerror(
                "Error",
                "Expense could not be updated."
            )


    # ========================================================
    # DELETE EXPENSE
    # ========================================================

    def delete_expense(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Expense",
                "Please select an expense to delete."
            )

            return


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )


        if not confirm:

            return


        try:

            success = delete_transaction(
                self.selected_id
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return


        if success:

            messagebox.showinfo(
                "Deleted",
                "Expense deleted successfully."
            )

            self.clear_form()

            self.load_expenses()

        else:

            messagebox.showerror(
                "Error",
                "Expense could not be deleted."
            )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_id = None

        self.date_var.set(
            str(date.today())
        )

        self.category_var.set(
            ""
        )

        self.amount_var.set(
            ""
        )

        self.payment_var.set(
            "UPI"
        )

        self.description_var.set(
            ""
        )

        # Remove table selection

        for item in self.tree.selection():

            self.tree.selection_remove(item)


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Expense Management"
    )

    root.geometry(
        "1100x650"
    )

    ExpenseManager(root)

    root.mainloop()