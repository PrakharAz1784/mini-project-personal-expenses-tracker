# charts.py

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import (
    get_expenses_by_category,
    get_monthly_summary
)


# ============================================================
# CONSTANTS
# ============================================================

BG = "#f5f7fb"


# ============================================================
# CHART MANAGER
# ============================================================

class ChartManager:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True)

        self.create_header()
        self.create_controls()

        self.chart_area = tk.Frame(self.frame, bg="white")
        self.chart_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.show_category_chart()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(self.frame, bg="#1f2937", height=65)
        header.pack(fill="x")

        tk.Label(
            header, text="FINANCIAL CHARTS",
            font=("Segoe UI", 20, "bold"),
            fg="white", bg="#1f2937"
        ).pack(side="left", padx=25, pady=15)


    # ========================================================
    # CHART CONTROLS
    # ========================================================

    def create_controls(self):

        controls = tk.Frame(self.frame, bg=BG)
        controls.pack(fill="x", padx=20, pady=15)

        for text, command, side in [
            ("Expense by Category", self.show_category_chart, "left"),
            ("Income vs Expense", self.show_monthly_chart, "left"),
            ("Expense Trend", self.show_expense_trend, "left"),
            ("Refresh", self.refresh_chart, "right"),
        ]:
            ttk.Button(
                controls, text=text, command=command
            ).pack(side=side, padx=5)


    # ========================================================
    # HELPERS
    # ========================================================

    def clear_chart(self):

        for widget in self.chart_area.winfo_children():
            widget.destroy()


    def create_figure(self, figsize, title):
        """Return a new (figure, axes) pair with the chart title set."""

        figure = plt.Figure(figsize=figsize, dpi=100)
        ax = figure.add_subplot(111)

        ax.set_title(title, fontsize=15, fontweight="bold", pad=20)

        return figure, ax


    def display_chart(self, figure):

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def show_no_data(self, message):

        tk.Label(
            self.chart_area,
            text=message,
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#6b7280"
        ).pack(expand=True)


    # ========================================================
    # EXPENSE BY CATEGORY
    # ========================================================

    def show_category_chart(self):

        self.clear_chart()

        data = get_expenses_by_category()

        if not data:
            self.show_no_data("No expense data available.")
            return

        categories = [row["category"] for row in data]
        amounts = [row["total"] for row in data]

        figure, ax = self.create_figure(
            (9, 5), "Expense Distribution by Category"
        )

        ax.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )

        self.display_chart(figure)


    # ========================================================
    # MONTHLY INCOME VS EXPENSE
    # ========================================================

    def show_monthly_chart(self):

        self.clear_chart()

        data = get_monthly_summary()

        if not data:
            self.show_no_data("No monthly data available.")
            return

        months = [row["month"] for row in data]
        income = [row["income"] or 0 for row in data]
        expenses = [row["expense"] or 0 for row in data]

        figure, ax = self.create_figure((10, 5), "Monthly Income vs Expense")

        x = range(len(months))
        width = 0.35

        # Income and expense bars sit side by side for each month
        ax.bar([i - width / 2 for i in x], income, width=width, label="Income")
        ax.bar([i + width / 2 for i in x], expenses, width=width, label="Expense")

        ax.set_xticks(list(x))
        ax.set_xticklabels(months, rotation=45)

        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")

        ax.legend()
        ax.grid(axis="y", alpha=0.25)

        self.display_chart(figure)


    # ========================================================
    # EXPENSE TREND
    # ========================================================

    def show_expense_trend(self):

        self.clear_chart()

        data = get_monthly_summary()

        if not data:
            self.show_no_data("No expense data available.")
            return

        months = [row["month"] for row in data]
        expenses = [row["expense"] or 0 for row in data]

        figure, ax = self.create_figure((10, 5), "Monthly Expense Trend")

        ax.plot(months, expenses, marker="o", linewidth=2)

        ax.set_xlabel("Month")
        ax.set_ylabel("Expenses (₹)")

        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.25)

        self.display_chart(figure)


    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_chart(self):

        self.show_category_chart()


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Financial Charts")
    root.geometry("1100x700")

    ChartManager(root)

    root.mainloop()