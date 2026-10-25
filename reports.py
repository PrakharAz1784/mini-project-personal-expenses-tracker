# reports.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import csv

from database import get_connection


# ============================================================
# CONSTANTS
# ============================================================

BG = "#f5f7fb"

HEADERS = [
    "ID", "Date", "Type", "Category", "Amount", "Payment", "Description"
]

EXCEL_COLUMN_WIDTHS = {
    "A": 10, "B": 15, "C": 15, "D": 20, "E": 18, "F": 20, "G": 35
}


# ============================================================
# REPORT MANAGER
# ============================================================

class ReportManager:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Frame(parent, bg=BG)
        self.window.pack(fill="both", expand=True)

        # Filter variables
        self.from_date_var = tk.StringVar()
        self.to_date_var = tk.StringVar()
        self.type_var = tk.StringVar(value="All")
        self.category_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()

        # Summary variables
        self.total_income_var = tk.StringVar(value="₹0.00")
        self.total_expense_var = tk.StringVar(value="₹0.00")
        self.balance_var = tk.StringVar(value="₹0.00")
        self.count_var = tk.StringVar(value="0")

        # UI
        self.create_header()
        self.create_filters()
        self.create_summary()
        self.create_table()

        self.load_categories()
        self.generate_report()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(self.window, bg="#1f2937", height=65)
        header.pack(fill="x")

        tk.Label(
            header, text="FINANCIAL REPORTS",
            font=("Segoe UI", 20, "bold"),
            fg="white", bg="#1f2937"
        ).pack(side="left", padx=25, pady=15)


    # ========================================================
    # FILTERS
    # ========================================================

    def create_filters(self):

        container = tk.Frame(self.window, bg=BG)
        container.pack(fill="x", padx=20, pady=15)

        filters = tk.LabelFrame(
            container,
            text="Report Filters",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=12, pady=12
        )
        filters.pack(fill="x")

        self.category_combo = ttk.Combobox(
            filters, textvariable=self.category_var,
            state="readonly", width=18
        )

        for column, (label, widget) in enumerate([
            ("From Date", ttk.Entry(
                filters, textvariable=self.from_date_var, width=15
            )),
            ("To Date", ttk.Entry(
                filters, textvariable=self.to_date_var, width=15
            )),
            ("Type", ttk.Combobox(
                filters, textvariable=self.type_var,
                values=["All", "Income", "Expense"],
                state="readonly", width=14
            )),
            ("Category", self.category_combo),
            ("Search", ttk.Entry(
                filters, textvariable=self.search_var, width=20
            )),
        ]):
            tk.Label(
                filters, text=label, bg="white", font=("Segoe UI", 10)
            ).grid(row=0, column=column, sticky="w", padx=6)

            widget.grid(row=1, column=column, padx=6, pady=5)

        ttk.Button(
            filters, text="🔍 Generate", command=self.generate_report
        ).grid(row=1, column=5, padx=10)

        ttk.Button(
            filters, text="🔄 Clear", command=self.clear_filters
        ).grid(row=1, column=6, padx=5)


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    def create_summary(self):

        summary = tk.Frame(self.window, bg=BG)
        summary.pack(fill="x", padx=20, pady=5)

        for title, variable in [
            ("TOTAL INCOME", self.total_income_var),
            ("TOTAL EXPENSE", self.total_expense_var),
            ("BALANCE", self.balance_var),
            ("TRANSACTIONS", self.count_var),
        ]:
            self.create_card(summary, title, variable)


    def create_card(self, parent, title, variable):

        card = tk.Frame(
            parent,
            bg="white", bd=1, relief="solid",
            padx=20, pady=10
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            card, text=title,
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#6b7280"
        ).pack()

        tk.Label(
            card, textvariable=variable,
            font=("Segoe UI", 18, "bold"),
            bg="white", fg="#111827"
        ).pack(pady=4)


    # ========================================================
    # TABLE
    # ========================================================

    def create_table(self):

        container = tk.Frame(self.window, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # (name, width, anchor)
        columns = [
            ("ID", 60, "center"),
            ("Date", 110, "center"),
            ("Type", 100, "center"),
            ("Category", 140, "w"),
            ("Amount", 120, "e"),
            ("Payment", 140, "w"),
            ("Description", 220, "w"),
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

        # Bottom buttons
        buttons = tk.Frame(self.window, bg=BG)
        buttons.pack(fill="x", padx=20, pady=(0, 15))

        for text, command in [
            ("📄 Export CSV", self.export_csv),
            ("📊 Export Excel", self.export_excel),
        ]:
            ttk.Button(
                buttons, text=text, command=command
            ).pack(side="left", padx=5)


    # ========================================================
    # DATABASE
    # ========================================================

    def query(self, sql, parameters=()):
        """Run a SELECT and return all rows."""

        connection = get_connection()

        try:
            return connection.execute(sql, parameters).fetchall()
        finally:
            connection.close()


    def load_categories(self):

        rows = self.query("""
            SELECT DISTINCT category
            FROM transactions
            WHERE category IS NOT NULL
            AND category != ''
            ORDER BY category
        """)

        categories = [row["category"] for row in rows]

        self.category_combo["values"] = ["All"] + categories


    # ========================================================
    # GENERATE REPORT
    # ========================================================

    def generate_report(self):

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Build the WHERE conditions from the filters
        conditions = []
        parameters = []

        from_date = self.from_date_var.get().strip()
        if from_date:
            conditions.append("date >= ?")
            parameters.append(from_date)

        to_date = self.to_date_var.get().strip()
        if to_date:
            conditions.append("date <= ?")
            parameters.append(to_date)

        transaction_type = self.type_var.get()
        if transaction_type != "All":
            conditions.append("type = ?")
            parameters.append(transaction_type)

        category = self.category_var.get()
        if category and category != "All":
            conditions.append("category = ?")
            parameters.append(category)

        search = self.search_var.get().strip()
        if search:
            conditions.append("""(
                category LIKE ?
                OR payment LIKE ?
                OR description LIKE ?
            )""")
            parameters.extend([f"%{search}%"] * 3)

        where = " AND ".join(["1 = 1"] + conditions)

        rows = self.query(
            f"""
            SELECT id, date, type, category, amount, payment, description
            FROM transactions
            WHERE {where}
            ORDER BY date DESC, id DESC
            """,
            parameters
        )

        # Fill table and add up totals
        total_income = 0
        total_expense = 0

        for row in rows:
            amount = float(row["amount"])

            if row["type"] == "Income":
                total_income += amount
            else:
                total_expense += amount

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["date"],
                    row["type"],
                    row["category"],
                    f"₹{amount:,.2f}",
                    row["payment"],
                    row["description"]
                )
            )

        # Update summary
        self.total_income_var.set(f"₹{total_income:,.2f}")
        self.total_expense_var.set(f"₹{total_expense:,.2f}")
        self.balance_var.set(f"₹{total_income - total_expense:,.2f}")
        self.count_var.set(str(len(rows)))


    # ========================================================
    # CLEAR FILTERS
    # ========================================================

    def clear_filters(self):

        self.from_date_var.set("")
        self.to_date_var.set("")
        self.type_var.set("All")
        self.category_var.set("All")
        self.search_var.set("")

        self.generate_report()


    # ========================================================
    # EXPORT
    # ========================================================

    def get_table_data(self):

        return [
            self.tree.item(item)["values"]
            for item in self.tree.get_children()
        ]


    def ask_export_file(self, kind, extension):
        """
        Return (data, filename) for an export, or None if there is
        nothing to export or the user cancelled the save dialog.
        """

        data = self.get_table_data()

        if not data:
            messagebox.showwarning(
                "No Data", "There is no report data to export."
            )
            return None

        filename = filedialog.asksaveasfilename(
            title=f"Save {kind} Report",
            defaultextension=extension,
            filetypes=[(f"{kind} Files", f"*{extension}")]
        )

        if not filename:
            return None

        return data, filename


    def export_csv(self):

        result = self.ask_export_file("CSV", ".csv")

        if result is None:
            return

        data, filename = result

        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(HEADERS)
                writer.writerows(data)

            messagebox.showinfo(
                "Export Successful", "CSV report exported successfully."
            )

        except Exception as error:
            messagebox.showerror("Export Error", str(error))


    def export_excel(self):

        result = self.ask_export_file("Excel", ".xlsx")

        if result is None:
            return

        data, filename = result

        try:
            import openpyxl

            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = "Financial Report"

            worksheet.append(HEADERS)

            for row in data:
                worksheet.append(list(row))

            for column, width in EXCEL_COLUMN_WIDTHS.items():
                worksheet.column_dimensions[column].width = width

            workbook.save(filename)

            messagebox.showinfo(
                "Export Successful", "Excel report exported successfully."
            )

        except ImportError:
            messagebox.showerror(
                "Missing Package",
                "Please install openpyxl using:\n\n"
                "pip install openpyxl"
            )

        except Exception as error:
            messagebox.showerror("Export Error", str(error))


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Financial Reports")
    root.geometry("1150x700")

    ReportManager(root)

    root.mainloop()