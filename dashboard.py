# dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import (
    get_total_income,
    get_total_expense,
    get_balance,
    get_current_month_expense,
    get_recent_transactions,
    get_monthly_summary,
)

from expenses import ExpenseManager
from income import IncomeManager
from charts import ChartManager
from reports import ReportManager


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Personal Expense Tracker"
        )

        self.root.geometry(
            "1250x750"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg="#f5f7fb"
        )

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.setup_style()

        # ----------------------------------------------------
        # MAIN CONTAINER
        # ----------------------------------------------------

        self.main_container = tk.Frame(
            self.root,
            bg="#f5f7fb"
        )

        self.main_container.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.create_sidebar()

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        self.content = tk.Frame(
            self.main_container,
            bg="#f5f7fb"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SHOW DASHBOARD
        # ----------------------------------------------------

        self.show_dashboard()


    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=8
        )

        style.configure(
            "TCombobox",
            padding=5
        )


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.main_container,
            bg="#111827",
            width=230
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )


        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo_frame = tk.Frame(
            self.sidebar,
            bg="#111827",
            height=100
        )

        logo_frame.pack(
            fill="x"
        )


        tk.Label(
            logo_frame,
            text="💰",
            font=("Segoe UI Emoji", 28),
            bg="#111827",
            fg="white"
        ).pack(
            pady=(15, 0)
        )


        tk.Label(
            logo_frame,
            text="Expense Tracker",
            font=("Segoe UI", 15, "bold"),
            bg="#111827",
            fg="white"
        ).pack()


        tk.Label(
            logo_frame,
            text="Personal Finance",
            font=("Segoe UI", 9),
            bg="#111827",
            fg="#9ca3af"
        ).pack(
            pady=(0, 10)
        )


        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        self.create_nav_button(
            "🏠  Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "💸  Expenses",
            self.show_expenses
        )

        self.create_nav_button(
            "💰  Income",
            self.show_income
        )

        self.create_nav_button(
            "📊  Charts",
            self.show_charts
        )

        self.create_nav_button(
            "📋  Reports",
            self.show_reports
        )


        # ----------------------------------------------------
        # SPACER
        # ----------------------------------------------------

        spacer = tk.Frame(
            self.sidebar,
            bg="#111827"
        )

        spacer.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        self.create_nav_button(
            "❌  Exit",
            self.exit_application
        )


    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            bg="#111827",
            fg="#d1d5db",
            activebackground="#374151",
            activeforeground="white",
            bd=0,
            relief="flat",
            anchor="w",
            padx=25,
            pady=13,
            cursor="hand2"
        )

        button.pack(
            fill="x"
        )

        return button


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()


    # ========================================================
    # DASHBOARD PAGE
    # ========================================================

    def show_dashboard(self):

        self.clear_content()

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.content,
            bg="#f5f7fb"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )


        tk.Label(
            header,
            text="Dashboard",
            font=("Segoe UI", 25, "bold"),
            bg="#f5f7fb",
            fg="#111827"
        ).pack(
            side="left"
        )


        tk.Button(
            header,
            text="🔄 Refresh",
            command=self.show_dashboard,
            font=("Segoe UI", 10),
            bg="white",
            fg="#374151",
            bd=1,
            relief="solid",
            padx=15,
            pady=7,
            cursor="hand2"
        ).pack(
            side="right"
        )


        today = datetime.now().strftime(
            "%d %B %Y"
        )


        tk.Label(
            header,
            text=today,
            font=("Segoe UI", 10),
            bg="#f5f7fb",
            fg="#6b7280"
        ).pack(
            side="right",
            padx=15
        )


        # ----------------------------------------------------
        # STAT CARDS
        # ----------------------------------------------------

        self.create_stat_cards()


        # ----------------------------------------------------
        # LOWER AREA
        # ----------------------------------------------------

        lower = tk.Frame(
            self.content,
            bg="#f5f7fb"
        )

        lower.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )


        # ----------------------------------------------------
        # LEFT: MONTHLY SUMMARY
        # ----------------------------------------------------

        left = tk.Frame(
            lower,
            bg="white",
            bd=1,
            relief="solid"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )


        tk.Label(
            left,
            text="Monthly Financial Summary",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )


        self.create_monthly_table(
            left
        )


        # ----------------------------------------------------
        # RIGHT: RECENT TRANSACTIONS
        # ----------------------------------------------------

        right = tk.Frame(
            lower,
            bg="white",
            bd=1,
            relief="solid"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )


        tk.Label(
            right,
            text="Recent Transactions",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )


        self.create_recent_transactions(
            right
        )


    # ========================================================
    # STAT CARDS
    # ========================================================

    def create_stat_cards(self):

        income = get_total_income()

        expense = get_total_expense()

        balance = get_balance()

        monthly_expense = get_current_month_expense()


        # Savings rate

        if income > 0:

            savings_rate = (
                (income - expense)
                / income
            ) * 100

        else:

            savings_rate = 0


        cards = tk.Frame(
            self.content,
            bg="#f5f7fb"
        )

        cards.pack(
            fill="x",
            padx=25,
            pady=10
        )


        self.create_card(
            cards,
            "💰",
            "Total Income",
            f"₹{income:,.2f}",
            "#16a34a"
        )


        self.create_card(
            cards,
            "💸",
            "Total Expenses",
            f"₹{expense:,.2f}",
            "#dc2626"
        )


        self.create_card(
            cards,
            "💵",
            "Current Balance",
            f"₹{balance:,.2f}",
            "#2563eb"
        )


        self.create_card(
            cards,
            "📅",
            "This Month",
            f"₹{monthly_expense:,.2f}",
            "#9333ea"
        )


        self.create_card(
            cards,
            "📈",
            "Savings Rate",
            f"{savings_rate:.1f}%",
            "#0891b2"
        )


    # ========================================================
    # STAT CARD
    # ========================================================

    def create_card(
        self,
        parent,
        icon,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        top = tk.Frame(
            card,
            bg="white"
        )

        top.pack(
            fill="x"
        )


        tk.Label(
            top,
            text=icon,
            font=("Segoe UI Emoji", 18),
            bg="white"
        ).pack(
            side="left"
        )


        tk.Label(
            top,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#6b7280",
            bg="white"
        ).pack(
            side="left",
            padx=8
        )


        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 19, "bold"),
            fg=accent,
            bg="white"
        ).pack(
            anchor="w",
            pady=(10, 2)
        )


    # ========================================================
    # MONTHLY TABLE
    # ========================================================

    def create_monthly_table(
        self,
        parent
    ):

        columns = (
            "Month",
            "Income",
            "Expense",
            "Balance"
        )


        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings"
        )


        for column in columns:

            tree.heading(
                column,
                text=column
            )


        tree.column(
            "Month",
            width=100
        )

        tree.column(
            "Income",
            width=120,
            anchor="e"
        )

        tree.column(
            "Expense",
            width=120,
            anchor="e"
        )

        tree.column(
            "Balance",
            width=120,
            anchor="e"
        )


        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        data = get_monthly_summary()


        # Show latest months first

        data = list(data)[::-1]


        for row in data[:8]:

            income = row["income"] or 0

            expense = row["expense"] or 0

            balance = income - expense


            tree.insert(
                "",
                "end",
                values=(
                    row["month"],
                    f"₹{income:,.2f}",
                    f"₹{expense:,.2f}",
                    f"₹{balance:,.2f}"
                )
            )


    # ========================================================
    # RECENT TRANSACTIONS
    # ========================================================

    def create_recent_transactions(
        self,
        parent
    ):

        columns = (
            "Date",
            "Type",
            "Category",
            "Amount"
        )


        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings"
        )


        for column in columns:

            tree.heading(
                column,
                text=column
            )


        tree.column(
            "Date",
            width=100,
            anchor="center"
        )

        tree.column(
            "Type",
            width=90,
            anchor="center"
        )

        tree.column(
            "Category",
            width=130
        )

        tree.column(
            "Amount",
            width=120,
            anchor="e"
        )


        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        transactions = get_recent_transactions(
            10
        )


        for transaction in transactions:

            amount = transaction["amount"]

            tree.insert(
                "",
                "end",
                values=(
                    transaction["date"],
                    transaction["type"],
                    transaction["category"],
                    f"₹{amount:,.2f}"
                )
            )


    # ========================================================
    # EXPENSE PAGE
    # ========================================================

    def show_expenses(self):

        self.clear_content()

        ExpenseManager(
            self.content
        )


    # ========================================================
    # INCOME PAGE
    # ========================================================

    def show_income(self):

        self.clear_content()

        IncomeManager(
            self.content
        )


    # ========================================================
    # CHARTS PAGE
    # ========================================================

    def show_charts(self):

        self.clear_content()

        ChartManager(
            self.content
        )


    # ========================================================
    # REPORTS PAGE
    # ========================================================

    def show_reports(self):

        self.clear_content()

        ReportManager(
            self.content
        )


    # ========================================================
    # EXIT
    # ========================================================

    def exit_application(self):

        answer = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if answer:

            self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

def start_dashboard():

    root = tk.Tk()

    Dashboard(
        root
    )

    root.mainloop()


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    start_dashboard()