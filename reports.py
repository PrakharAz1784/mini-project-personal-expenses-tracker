# reports.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import csv

from database import get_connection


# ============================================================
# REPORT MANAGER
# ============================================================

class ReportManager:

    def __init__(self, parent):

        self.parent = parent

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

        self.from_date_var = tk.StringVar()

        self.to_date_var = tk.StringVar()

        self.type_var = tk.StringVar(
            value="All"
        )

        self.category_var = tk.StringVar(
            value="All"
        )

        self.search_var = tk.StringVar()

        self.total_income_var = tk.StringVar(
            value="₹0.00"
        )

        self.total_expense_var = tk.StringVar(
            value="₹0.00"
        )

        self.balance_var = tk.StringVar(
            value="₹0.00"
        )

        self.count_var = tk.StringVar(
            value="0"
        )

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

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
            text="FINANCIAL REPORTS",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1f2937"
        ).pack(
            side="left",
            padx=25,
            pady=15
        )


    # ========================================================
    # FILTERS
    # ========================================================

    def create_filters(self):

        container = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        container.pack(
            fill="x",
            padx=20,
            pady=15
        )

        filters = tk.LabelFrame(
            container,
            text="Report Filters",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=12,
            pady=12
        )

        filters.pack(
            fill="x"
        )


        # ----------------------------------------------------
        # FROM DATE
        # ----------------------------------------------------

        tk.Label(
            filters,
            text="From Date",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=6
        )

        ttk.Entry(
            filters,
            textvariable=self.from_date_var,
            width=15
        ).grid(
            row=1,
            column=0,
            padx=6,
            pady=5
        )


        # ----------------------------------------------------
        # TO DATE
        # ----------------------------------------------------

        tk.Label(
            filters,
            text="To Date",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=6
        )

        ttk.Entry(
            filters,
            textvariable=self.to_date_var,
            width=15
        ).grid(
            row=1,
            column=1,
            padx=6,
            pady=5
        )


        # ----------------------------------------------------
        # TYPE
        # ----------------------------------------------------

        tk.Label(
            filters,
            text="Type",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=6
        )

        ttk.Combobox(
            filters,
            textvariable=self.type_var,
            values=[
                "All",
                "Income",
                "Expense"
            ],
            state="readonly",
            width=14
        ).grid(
            row=1,
            column=2,
            padx=6,
            pady=5
        )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        tk.Label(
            filters,
            text="Category",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=6
        )

        self.category_combo = ttk.Combobox(
            filters,
            textvariable=self.category_var,
            state="readonly",
            width=18
        )

        self.category_combo.grid(
            row=1,
            column=3,
            padx=6,
            pady=5
        )


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        tk.Label(
            filters,
            text="Search",
            bg="white",
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=4,
            sticky="w",
            padx=6
        )

        ttk.Entry(
            filters,
            textvariable=self.search_var,
            width=20
        ).grid(
            row=1,
            column=4,
            padx=6,
            pady=5
        )


        # ----------------------------------------------------
        # GENERATE
        # ----------------------------------------------------

        ttk.Button(
            filters,
            text="🔍 Generate",
            command=self.generate_report
        ).grid(
            row=1,
            column=5,
            padx=10
        )


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        ttk.Button(
            filters,
            text="🔄 Clear",
            command=self.clear_filters
        ).grid(
            row=1,
            column=6,
            padx=5
        )


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    def create_summary(self):

        summary = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        summary.pack(
            fill="x",
            padx=20,
            pady=5
        )


        self.create_card(
            summary,
            "TOTAL INCOME",
            self.total_income_var
        )


        self.create_card(
            summary,
            "TOTAL EXPENSE",
            self.total_expense_var
        )


        self.create_card(
            summary,
            "BALANCE",
            self.balance_var
        )


        self.create_card(
            summary,
            "TRANSACTIONS",
            self.count_var
        )


    def create_card(
        self,
        parent,
        title,
        variable
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=10
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#6b7280"
        ).pack()


        tk.Label(
            card,
            textvariable=variable,
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            pady=4
        )


    # ========================================================
    # TABLE
    # ========================================================

    def create_table(self):

        container = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )


        columns = (
            "ID",
            "Date",
            "Type",
            "Category",
            "Amount",
            "Payment",
            "Description"
        )


        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )


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
            width=110,
            anchor="center"
        )

        self.tree.column(
            "Type",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Category",
            width=140
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
            width=220
        )


        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar = ttk.Scrollbar(
            container,
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


        # ----------------------------------------------------
        # BOTTOM BUTTONS
        # ----------------------------------------------------

        buttons = tk.Frame(
            self.window,
            bg="#f5f7fb"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        ttk.Button(
            buttons,
            text="📄 Export CSV",
            command=self.export_csv
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="📊 Export Excel",
            command=self.export_excel
        ).pack(
            side="left",
            padx=5
        )


    # ========================================================
    # LOAD CATEGORIES
    # ========================================================

    def load_categories(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT category
            FROM transactions
            WHERE category IS NOT NULL
            AND category != ''
            ORDER BY category
        """)

        categories = [
            row["category"]
            for row in cursor.fetchall()
        ]

        connection.close()


        self.category_combo["values"] = (
            ["All"] + categories
        )


    # ========================================================
    # GENERATE REPORT
    # ========================================================

    def generate_report(self):

        # Clear table

        for row in self.tree.get_children():

            self.tree.delete(row)


        query = """
            SELECT
                id,
                date,
                type,
                category,
                amount,
                payment,
                description
            FROM transactions
            WHERE 1 = 1
        """

        parameters = []


        # ----------------------------------------------------
        # FROM DATE
        # ----------------------------------------------------

        from_date = self.from_date_var.get().strip()

        if from_date:

            query += " AND date >= ?"

            parameters.append(
                from_date
            )


        # ----------------------------------------------------
        # TO DATE
        # ----------------------------------------------------

        to_date = self.to_date_var.get().strip()

        if to_date:

            query += " AND date <= ?"

            parameters.append(
                to_date
            )


        # ----------------------------------------------------
        # TYPE
        # ----------------------------------------------------

        transaction_type = self.type_var.get()

        if transaction_type != "All":

            query += " AND type = ?"

            parameters.append(
                transaction_type
            )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        category = self.category_var.get()

        if category and category != "All":

            query += " AND category = ?"

            parameters.append(
                category
            )


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        search = self.search_var.get().strip()

        if search:

            query += """
                AND (
                    category LIKE ?
                    OR payment LIKE ?
                    OR description LIKE ?
                )
            """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value
            ])


        query += """
            ORDER BY date DESC, id DESC
        """


        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        rows = cursor.fetchall()

        connection.close()


        # ----------------------------------------------------
        # ADD TO TABLE
        # ----------------------------------------------------

        total_income = 0

        total_expense = 0


        for row in rows:

            amount = float(
                row["amount"]
            )


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


        # ----------------------------------------------------
        # UPDATE SUMMARY
        # ----------------------------------------------------

        balance = (
            total_income -
            total_expense
        )


        self.total_income_var.set(
            f"₹{total_income:,.2f}"
        )

        self.total_expense_var.set(
            f"₹{total_expense:,.2f}"
        )

        self.balance_var.set(
            f"₹{balance:,.2f}"
        )

        self.count_var.set(
            str(len(rows))
        )


    # ========================================================
    # CLEAR FILTERS
    # ========================================================

    def clear_filters(self):

        self.from_date_var.set("")

        self.to_date_var.set("")

        self.type_var.set(
            "All"
        )

        self.category_var.set(
            "All"
        )

        self.search_var.set(
            ""
        )

        self.generate_report()


    # ========================================================
    # GET TABLE DATA
    # ========================================================

    def get_table_data(self):

        data = []

        for item in self.tree.get_children():

            values = self.tree.item(
                item
            )["values"]

            data.append(values)

        return data


    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv(self):

        data = self.get_table_data()


        if not data:

            messagebox.showwarning(
                "No Data",
                "There is no report data to export."
            )

            return


        filename = filedialog.asksaveasfilename(
            title="Save CSV Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )


        if not filename:

            return


        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )


                writer.writerow([
                    "ID",
                    "Date",
                    "Type",
                    "Category",
                    "Amount",
                    "Payment",
                    "Description"
                ])


                writer.writerows(
                    data
                )


            messagebox.showinfo(
                "Export Successful",
                "CSV report exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


    # ========================================================
    # EXPORT EXCEL
    # ========================================================

    def export_excel(self):

        data = self.get_table_data()


        if not data:

            messagebox.showwarning(
                "No Data",
                "There is no report data to export."
            )

            return


        filename = filedialog.asksaveasfilename(
            title="Save Excel Report",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files", "*.xlsx")
            ]
        )


        if not filename:

            return


        try:

            import openpyxl

            workbook = openpyxl.Workbook()

            worksheet = workbook.active

            worksheet.title = "Financial Report"


            headers = [
                "ID",
                "Date",
                "Type",
                "Category",
                "Amount",
                "Payment",
                "Description"
            ]


            worksheet.append(
                headers
            )


            for row in data:

                worksheet.append(
                    list(row)
                )


            # ------------------------------------------------
            # COLUMN WIDTHS
            # ------------------------------------------------

            widths = {
                "A": 10,
                "B": 15,
                "C": 15,
                "D": 20,
                "E": 18,
                "F": 20,
                "G": 35
            }


            for column, width in widths.items():

                worksheet.column_dimensions[
                    column
                ].width = width


            workbook.save(
                filename
            )


            messagebox.showinfo(
                "Export Successful",
                "Excel report exported successfully."
            )

        except ImportError:

            messagebox.showerror(
                "Missing Package",
                "Please install openpyxl using:\n\n"
                "pip install openpyxl"
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Financial Reports"
    )

    root.geometry(
        "1150x700"
    )

    ReportManager(root)

    root.mainloop()