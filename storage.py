import json
from models import Expense


def save_data(expenses, budgets):
    data = {
        "expenses": [expense.to_dict() for expense in expenses],
        "budgets": budgets
    }

    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            expenses = [Expense.from_dict(item) for item in data]
            return expenses, {}

        expenses = [
            Expense.from_dict(item)
            for item in data.get("expenses", [])
        ]

        budgets = data.get("budgets", {})

        return expenses, budgets

    except FileNotFoundError:
        return [], {}

    except json.JSONDecodeError:
        with open("expenses.json", "r") as file:
            corrupted_data = file.read()

        with open("expenses.bak.json", "w") as backup_file:
            backup_file.write(corrupted_data)

        print("\nWarning: expenses.json was corrupted.")
        print("Backup created as expenses.bak.json.")
        print("Starting with fresh data.\n")

        return [], {}

    except (KeyError, TypeError, ValueError):
        with open("expenses.json", "r") as file:
            corrupted_data = file.read()

        with open("expenses.bak.json", "w") as backup_file:
            backup_file.write(corrupted_data)

        print("\nWarning: expenses.json contains invalid data.")
        print("Backup created as expenses.bak.json.")
        print("Starting with fresh data.\n")

        return [], {}