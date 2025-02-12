import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
def create_table():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add a transaction
def add_transaction():
    transaction_type = input("Enter type (income/expense): ").lower()
    category = input("Enter category (e.g., food, rent, entertainment or traveling): ")
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description (optional): ")

    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (type, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (transaction_type, category, amount, date, description))
    conn.commit()
    conn.close()
    print("Transaction added successfully!")

# View all transactions
def view_transactions():
    conn = sqlite3.connect("finance_tracker.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    print(df)

# Generate monthly report
def generate_monthly_report():
    month = input("Enter month (YYYY-MM): ")
    conn = sqlite3.connect("finance_tracker.db")
    df = pd.read_sql_query(f"SELECT * FROM transactions WHERE strftime('%Y-%m', date) = '{month}'", conn)
    conn.close()

    if df.empty:
        print("No transactions found for this month.")
        return

    # Calculate total income and expenses
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expenses = df[df['type'] == 'expense']['amount'].sum()
    savings = total_income - total_expenses

    print(f"\nMonthly Report for {month}:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Savings: ${savings:.2f}")

    # Visualize expenses by category
    expenses = df[df['type'] == 'expense']
    if not expenses.empty:
        expenses_by_category = expenses.groupby('category')['amount'].sum()
        expenses_by_category.plot(kind='bar', title=f"Expenses by Category for {month}")
        plt.xlabel("Category")
        plt.ylabel("Amount (GBP £:)")
        plt.show()

# Main menu
def main():
    create_table()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Monthly Report")
        print("4. Exit")
        print( "----------------------------------------------------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            generate_monthly_report()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main()