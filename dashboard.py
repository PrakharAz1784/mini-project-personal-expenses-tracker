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
# COLORS
# ============================================================

BG = "#f5f7fb"
SIDEBAR_BG = "#111827"
DARK_TEXT = "#111827"
GRAY_TEXT = "#6b7280"


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1250x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)

        self.setup_style()

        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(fill="both", expand=True)

        self.create_sidebar()

        self.content = tk.Frame(self.main_container, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

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

        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("TCombobox", padding=5)


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.main_container,
            bg=SIDEBAR_BG,
            width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG, height=100)
        logo_frame.pack(fill="x")

        tk.Label(
            logo_frame, text="💰",
            font=("Segoe UI Emoji", 28),
            bg=SIDEBAR_BG, fg="white"
        ).pack(pady=(15, 0))

        tk.Label(
            logo_frame, text="Expense Tracker",
            font=("Segoe UI", 15, "bold"),
            bg=SIDEBAR_BG, fg="white"
        ).pack()

        tk.Label(
            logo_frame, text="Personal Finance",
            font=("Segoe UI", 9),
            bg=SIDEBAR_BG, fg="#9ca3af"
        ).pack(pady=(0, 10))

        # Navigation
        for text, command in [
            ("🏠  Dashboard", self.show_dashboard),
            ("💸  Expenses", self.show_expenses),
            ("💰  Income", self.show_income),
            ("📊  Charts", self.show_charts),
            ("📋  Reports", self.show_reports),
        ]:
            self.create_nav_button(text, command)

        # Spacer pushes Exit to the bottom
        tk.Frame(self.sidebar, bg=SIDEBAR_BG).pack(fill="both", expand=True)

        self.create_nav_button("❌  Exit", self.exit_application)


    def create_nav_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            bg=SIDEBAR_BG,
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
        button.pack(fill="x")

        return button


    # ========================================================
    # PAGE HELPERS
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    def show_page(self, page_class):

        self.clear_content()
        page_class(self.content)


    # ========================================================
    # DASHBOARD PAGE
    # ========================================================

    def show_dashboard(self):

        self.clear_content()

        # Header
        header = tk.Frame(self.content, bg=BG)
        header.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            header, text="Dashboard",
            font=("Segoe UI", 25, "bold"),
            bg=BG, fg=DARK_TEXT
        ).pack(side="left")

        tk.Button(
            header, text="🔄 Refresh",
            command=self.show_dashboard,
            font=("Segoe UI", 10),
            bg="white", fg="#374151",
            bd=1, relief="solid",
            padx=15, pady=7,
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            header, text=datetime.now().strftime("%d %B %Y"),
            font=("Segoe UI", 10),
            bg=BG, fg=GRAY_TEXT
        ).pack(side="right", padx=15)

        # Stat cards
        self.create_stat_cards()

        # Lower area: monthly summary (left), recent transactions (right)
        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True, padx=25, pady=15)

        left = self.create_panel(
            lower, "Monthly Financial Summary", "left", (0, 10)
        )
        self.create_monthly_table(left)

        right = self.create_panel(
            lower, "Recent Transactions", "right", (10, 0)
        )
        self.create_recent_transactions(right)


    # ========================================================
    # STAT CARDS
    # ========================================================

    def create_stat_cards(self):

        income = get_total_income()
        expense = get_total_expense()
        balance = get_balance()
        monthly_expense = get_current_month_expense()

        savings_rate = ((income - expense) / income) * 100 if income > 0 else 0

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=25, pady=10)

        for icon, title, value, accent in [
            ("💰", "Total Income", f"₹{income:,.2f}", "#16a34a"),
            ("💸", "Total Expenses", f"₹{expense:,.2f}", "#dc2626"),
            ("💵", "Current Balance", f"₹{balance:,.2f}", "#2563eb"),
            ("📅", "This Month", f"₹{monthly_expense:,.2f}", "#9333ea"),
            ("📈", "Savings Rate", f"{savings_rate:.1f}%", "#0891b2"),
        ]:
            self.create_card(cards, icon, title, value, accent)


    def create_card(self, parent, icon, title, value, accent):

        card = tk.Frame(
            parent,
            bg="white", bd=1, relief="solid",
            padx=15, pady=12
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x")

        tk.Label(
            top, text=icon,
            font=("Segoe UI Emoji", 18),
            bg="white"
        ).pack(side="left")

        tk.Label(
            top, text=title,
            font=("Segoe UI", 10, "bold"),
            fg=GRAY_TEXT, bg="white"
        ).pack(side="left", padx=8)

        tk.Label(
            card, text=value,
            font=("Segoe UI", 19, "bold"),
            fg=accent, bg="white"
        ).pack(anchor="w", pady=(10, 2))


    # ========================================================
    # PANELS AND TABLES
    # ========================================================

    def create_panel(self, parent, title, side, padx):
        """White box with a bold title; returns the frame to fill."""

        panel = tk.Frame(parent, bg="white", bd=1, relief="solid")
        panel.pack(side=side, fill="both", expand=True, padx=padx)

        tk.Label(
            panel, text=title,
            font=("Segoe UI", 13, "bold"),
            bg="white", fg=DARK_TEXT
        ).pack(anchor="w", padx=15, pady=15)

        return panel


    def create_table(self, parent, columns, rows):
        """
        columns: list of (name, width, anchor)
        rows:    list of value tuples to insert
        """

        names = [name for name, _, _ in columns]

        tree = ttk.Treeview(parent, columns=names, show="headings")

        for name, width, anchor in columns:
            tree.heading(name, text=name)
            tree.column(name, width=width, anchor=anchor)

        tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for values in rows:
            tree.insert("", "end", values=values)

        return tree


    def create_monthly_table(self, parent):

        # Latest months first, max 8
        data = list(get_monthly_summary())[::-1][:8]

        rows = []

        for row in data:
            income = row["income"] or 0
            expense = row["expense"] or 0

            rows.append((
                row["month"],
                f"₹{income:,.2f}",
                f"₹{expense:,.2f}",
                f"₹{income - expense:,.2f}"
            ))

        self.create_table(
            parent,
            [
                ("Month", 100, "w"),
                ("Income", 120, "e"),
                ("Expense", 120, "e"),
                ("Balance", 120, "e"),
            ],
            rows
        )


    def create_recent_transactions(self, parent):

        rows = [
            (
                t["date"],
                t["type"],
                t["category"],
                f"₹{t['amount']:,.2f}"
            )
            for t in get_recent_transactions(10)
        ]

        self.create_table(
            parent,
            [
                ("Date", 100, "center"),
                ("Type", 90, "center"),
                ("Category", 130, "w"),
                ("Amount", 120, "e"),
            ],
            rows
        )


    # ========================================================
    # OTHER PAGES
    # ========================================================

    def show_expenses(self):
        self.show_page(ExpenseManager)

    def show_income(self):
        self.show_page(IncomeManager)

    def show_charts(self):
        self.show_page(ChartManager)

    def show_reports(self):
        self.show_page(ReportManager)


    # ========================================================
    # EXIT
    # ========================================================

    def exit_application(self):

        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

def start_dashboard():

    root = tk.Tk()
    Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    start_dashboard()