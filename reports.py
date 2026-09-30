import csv
import math
from datetime import datetime, date

from models import Expense
from storage import save_data


CATEGORIES = [
    "Food",
    "Travel",
    "Bills",
    "Shopping",
    "Health",
    "Education",
    "Entertainment",
    "Other"
]


def ask_float(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if not math.isfinite(amount):
                print("Enter a valid number.")
                continue

            if amount <= 0:
                print("Amount must be positive.")
                continue

            return amount

        except ValueError:
            print("Enter a valid number.")


def ask_date():
    while True:
        text = input(
            f"Enter date (YYYY-MM-DD) [default {date.today()}]: "
        ).strip()

        if text == "":
            return str(date.today())

        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def ask_month():
    while True:
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")
            return month

        except ValueError:
            print("Invalid month. Use YYYY-MM.")


def ask_category():
    while True:
        print("\nCategories:")

        for number, category in enumerate(CATEGORIES, 1):
            print(f"{number}. {category}")

        try:
            choice = int(input("Choose category: "))

            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]

            print("Choose a valid category number.")

        except ValueError:
            print("Enter a number.")


def get_next_id(expenses):
    if not expenses:
        return 1

    return max(expense.id for expense in expenses) + 1


def get_month_expenses(expenses, month):
    return [
        expense
        for expense in expenses
        if expense.date.startswith(month)
    ]


def add_expense(expenses, budgets):
    amount = ask_float("Enter amount: ")
    category = ask_category()
    expense_date = ask_date()
    note = input("Enter note: ").strip()

    expense = Expense(
        get_next_id(expenses),
        amount,
        category,
        expense_date,
        note
    )

    expenses.append(expense)

    save_data(expenses, budgets)

    print("\nExpense added successfully.")

    check_budget(
        expenses,
        budgets,
        category,
        expense_date[:7]
    )


def list_expenses(expenses):
    month = ask_month()

    month_expenses = get_month_expenses(expenses, month)

    if not month_expenses:
        print("\nNo expenses found for this month.")
        return

    print(f"\nExpenses for {month}")
    print("-" * 75)

    for expense in month_expenses:
        print(
            f"ID: {expense.id} | "
            f"₹{expense.amount:.2f} | "
            f"{expense.category} | "
            f"{expense.date} | "
            f"{expense.note}"
        )

    print("-" * 75)


def category_summary(expenses):
    month = ask_month()

    month_expenses = get_month_expenses(expenses, month)

    if not month_expenses:
        print("\nNo expenses found for this month.")
        return

    summary = {}

    for expense in month_expenses:
        if expense.category not in summary:
            summary[expense.category] = 0

        summary[expense.category] += expense.amount

    total = sum(summary.values())

    print(f"\nCategory Summary for {month}")
    print("-" * 50)

    for category, amount in summary.items():
        percentage = (amount / total) * 100

        print(
            f"{category}: "
            f"₹{amount:.2f} "
            f"({percentage:.2f}%)"
        )

    print("-" * 50)
    print(f"Total: ₹{total:.2f}")


def set_budget(expenses, budgets):
    category = ask_category()
    budget = ask_float("Enter monthly budget: ")

    budgets[category] = budget

    save_data(expenses, budgets)

    print(
        f"\nMonthly budget for {category} "
        f"set to ₹{budget:.2f}."
    )


def check_budget(expenses, budgets, category, month):
    if category not in budgets:
        return

    budget = budgets[category]

    month_expenses = get_month_expenses(expenses, month)

    spent = sum(
        expense.amount
        for expense in month_expenses
        if expense.category == category
    )

    percentage = (spent / budget) * 100

    if percentage >= 100:
        print(
            f"WARNING: {category} budget reached/exceeded!"
        )
        print(
            f"Spent: ₹{spent:.2f} / "
            f"Budget: ₹{budget:.2f}"
        )

    elif percentage >= 80:
        print(
            f"WARNING: {category} budget is at "
            f"{percentage:.2f}%."
        )
        print(
            f"Spent: ₹{spent:.2f} / "
            f"Budget: ₹{budget:.2f}"
        )


def delete_expense(expenses, budgets):
    while True:
        try:
            expense_id = int(input("Enter expense ID to delete: "))
            break

        except ValueError:
            print("Enter a valid ID.")

    for expense in expenses:
        if expense.id == expense_id:
            expenses.remove(expense)
            save_data(expenses, budgets)

            print("\nExpense deleted successfully.")
            return

    print("\nExpense ID not found.")


def export_month(expenses):
    month = ask_month()

    month_expenses = get_month_expenses(expenses, month)

    if not month_expenses:
        print("\nNo expenses found for this month.")
        return

    filename = f"expenses_{month}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "id",
            "amount",
            "category",
            "date",
            "note"
        ])

        for expense in month_expenses:
            writer.writerow([
                expense.id,
                expense.amount,
                expense.category,
                expense.date,
                expense.note
            ])

    print(f"\nExpenses exported to {filename}.")