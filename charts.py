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
# CHART MANAGER
# ============================================================

class ChartManager:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(
            parent,
            bg="#f5f7fb"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.create_header()

        self.create_controls()

        self.chart_area = tk.Frame(
            self.frame,
            bg="white"
        )

        self.chart_area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.show_category_chart()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.frame,
            bg="#1f2937",
            height=65
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="FINANCIAL CHARTS",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1f2937"
        ).pack(
            side="left",
            padx=25,
            pady=15
        )


    # ========================================================
    # CHART CONTROLS
    # ========================================================

    def create_controls(self):

        controls = tk.Frame(
            self.frame,
            bg="#f5f7fb"
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=15
        )


        ttk.Button(
            controls,
            text="Expense by Category",
            command=self.show_category_chart
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            controls,
            text="Income vs Expense",
            command=self.show_monthly_chart
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            controls,
            text="Expense Trend",
            command=self.show_expense_trend
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            controls,
            text="Refresh",
            command=self.refresh_chart
        ).pack(
            side="right",
            padx=5
        )


    # ========================================================
    # CLEAR CHART
    # ========================================================

    def clear_chart(self):

        for widget in self.chart_area.winfo_children():

            widget.destroy()


    # ========================================================
    # DISPLAY FIGURE
    # ========================================================

    def display_chart(self, figure):

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_area
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # ========================================================
    # EXPENSE BY CATEGORY
    # ========================================================

    def show_category_chart(self):

        self.clear_chart()

        data = get_expenses_by_category()


        # ----------------------------------------------------
        # NO DATA
        # ----------------------------------------------------

        if not data:

            self.show_no_data(
                "No expense data available."
            )

            return


        categories = [
            row["category"]
            for row in data
        ]

        amounts = [
            row["total"]
            for row in data
        ]


        # ----------------------------------------------------
        # CREATE FIGURE
        # ----------------------------------------------------

        figure = plt.Figure(
            figsize=(9, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)


        ax.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )


        ax.set_title(
            "Expense Distribution by Category",
            fontsize=15,
            fontweight="bold",
            pad=20
        )


        figure.tight_layout()

        self.display_chart(
            figure
        )


    # ========================================================
    # MONTHLY INCOME VS EXPENSE
    # ========================================================

    def show_monthly_chart(self):

        self.clear_chart()

        data = get_monthly_summary()


        # ----------------------------------------------------
        # NO DATA
        # ----------------------------------------------------

        if not data:

            self.show_no_data(
                "No monthly data available."
            )

            return


        months = [
            row["month"]
            for row in data
        ]

        income = [
            row["income"] or 0
            for row in data
        ]

        expenses = [
            row["expense"] or 0
            for row in data
        ]


        # ----------------------------------------------------
        # CREATE FIGURE
        # ----------------------------------------------------

        figure = plt.Figure(
            figsize=(10, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)


        x = range(
            len(months)
        )

        width = 0.35


        income_positions = [
            i - width / 2
            for i in x
        ]

        expense_positions = [
            i + width / 2
            for i in x
        ]


        ax.bar(
            income_positions,
            income,
            width=width,
            label="Income"
        )


        ax.bar(
            expense_positions,
            expenses,
            width=width,
            label="Expense"
        )


        ax.set_xticks(
            list(x)
        )

        ax.set_xticklabels(
            months,
            rotation=45
        )


        ax.set_title(
            "Monthly Income vs Expense",
            fontsize=15,
            fontweight="bold",
            pad=20
        )


        ax.set_xlabel(
            "Month"
        )

        ax.set_ylabel(
            "Amount (₹)"
        )


        ax.legend()

        ax.grid(
            axis="y",
            alpha=0.25
        )


        figure.tight_layout()

        self.display_chart(
            figure
        )


    # ========================================================
    # EXPENSE TREND
    # ========================================================

    def show_expense_trend(self):

        self.clear_chart()

        data = get_monthly_summary()


        # ----------------------------------------------------
        # NO DATA
        # ----------------------------------------------------

        if not data:

            self.show_no_data(
                "No expense data available."
            )

            return


        months = [
            row["month"]
            for row in data
        ]

        expenses = [
            row["expense"] or 0
            for row in data
        ]


        # ----------------------------------------------------
        # CREATE FIGURE
        # ----------------------------------------------------

        figure = plt.Figure(
            figsize=(10, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)


        ax.plot(
            months,
            expenses,
            marker="o",
            linewidth=2
        )


        ax.set_title(
            "Monthly Expense Trend",
            fontsize=15,
            fontweight="bold",
            pad=20
        )


        ax.set_xlabel(
            "Month"
        )

        ax.set_ylabel(
            "Expenses (₹)"
        )


        ax.tick_params(
            axis="x",
            rotation=45
        )


        ax.grid(
            True,
            alpha=0.25
        )


        figure.tight_layout()

        self.display_chart(
            figure
        )


    # ========================================================
    # NO DATA MESSAGE
    # ========================================================

    def show_no_data(self, message):

        label = tk.Label(
            self.chart_area,
            text=message,
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#6b7280"
        )

        label.pack(
            expand=True
        )


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

    root.title(
        "Financial Charts"
    )

    root.geometry(
        "1100x700"
    )

    ChartManager(root)

    root.mainloop()