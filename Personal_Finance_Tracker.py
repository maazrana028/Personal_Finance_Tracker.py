import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF

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
    category = input("Enter category (e.g., food, rent, entertainment): ")
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

# Export report to CSV
def export_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Report exported to {filename}")

# Export report to PDF
def export_to_pdf(df, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.cell(200, 10, txt="Monthly Financial Report", ln=True, align="C")

    # Add table headers
    pdf.cell(40, 10, txt="Type", border=1)
    pdf.cell(40, 10, txt="Category", border=1)
    pdf.cell(40, 10, txt="Amount", border=1)
    pdf.cell(40, 10, txt="Date", border=1)
    pdf.cell(40, 10, txt="Description", border=1)
    pdf.ln()

    # Add table rows
    for index, row in df.iterrows():
        pdf.cell(40, 10, txt=row['type'], border=1)
        pdf.cell(40, 10, txt=row['category'], border=1)
        pdf.cell(40, 10, txt=str(row['amount']), border=1)
        pdf.cell(40, 10, txt=row['date'], border=1)
        pdf.cell(40, 10, txt=row['description'], border=1)
        pdf.ln()

    # Save the PDF
    pdf.output(filename)
    print(f"Report exported to {filename}")

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
        plt.ylabel("Amount ($)")
        plt.show()

    # Export options
    export_choice = input("Do you want to export the report? (csv/pdf/none): ").lower()
    if export_choice == "csv":
        export_to_csv(df, f"monthly_report_{month}.csv")
    elif export_choice == "pdf":
        export_to_pdf(df, f"monthly_report_{month}.pdf")
    elif export_choice == "none":
        print("Report not exported.")
    else:
        print("Invalid choice. Report not exported.")

# Main menu
def main():
    create_table()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Monthly Report")
        print("4. Exit")
        print("--------------------------------------------------------------------------")
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
