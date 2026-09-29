# 💰 Personal Expense Tracker

A GUI-based Personal Expense Tracker developed using Python, Tkinter, and SQLite. 
The application helps users manage their income and expenses, analyze spending 
patterns, visualize financial data, and generate financial reports.

## 📌 Project Overview

Managing personal finances manually can be difficult because transaction records 
may become disorganized and it can be difficult to understand spending patterns.

The Personal Expense Tracker provides a simple desktop application where users can 
record their income and expenses, view their financial summary, analyze spending 
through charts, and generate reports.

## ✨ Features

### 💸 Expense Management
- Add new expenses
- Edit existing expenses
- Delete expenses
- View expense records
- Categorize expenses
- Store payment method and description

### 💵 Income Management
- Add income records
- Edit income records
- Delete income records
- View income records
- Store income source and payment details

### 📊 Dashboard
The dashboard displays:
- Total Income
- Total Expenses
- Current Balance
- Monthly Expenses
- Savings Rate
- Monthly Financial Summary
- Recent Transactions

### 📈 Data Visualization
The application provides charts for:
- Expense distribution by category
- Income vs Expense
- Expense trends over time

### 📄 Reports
Users can:
- Filter transactions by date
- Filter by transaction type
- Filter by category
- Search transactions
- Export reports to CSV
- Export reports to Excel

## 🧠 Intelligent Analytics

The project is designed to be extended beyond basic expense tracking with 
intelligent financial analysis features such as:

- Unusual Spending Detection
- Expense Forecasting
- Smart Budget Recommendations
- Month-to-Month Spending Comparison
- Actionable Financial Insights

These features aim to convert historical transaction data into useful information 
for better financial planning.

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Tkinter | Graphical User Interface |
| SQLite | Database management |
| Matplotlib | Charts and visualization |
| OpenPyXL | Excel report generation |
| CSV | Report export |

## 📁 Project Structure

```text
Personal-Expense-Tracker/
│
├── main.py
├── dashboard.py
├── database.py
├── expenses.py
├── income.py
├── charts.py
├── reports.py
│
├── database/
│   └── expenses.db
│
└── README.md
