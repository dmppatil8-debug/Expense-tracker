from storage import load_data

from reports import (
    add_expense,
    list_expenses,
    category_summary,
    set_budget,
    delete_expense,
    export_month
)


expenses, budgets = load_data()


while True:
    print("\n========== EXPENSE TRACKER ==========")
    print("1. Add expense")
    print("2. List expenses")
    print("3. Category summary")
    print("4. Set monthly budget")
    print("5. Delete expense")
    print("6. Export month to CSV")
    print("7. Quit")

    choice = input("Choose an option: ").strip()

    try:
        choice = int(choice)

        if choice == 1:
            add_expense(expenses, budgets)

        elif choice == 2:
            list_expenses(expenses)

        elif choice == 3:
            category_summary(expenses)

        elif choice == 4:
            set_budget(expenses, budgets)

        elif choice == 5:
            delete_expense(expenses, budgets)

        elif choice == 6:
            export_month(expenses)

        elif choice == 7:
            print("Goodbye!")
            break

        else:
            print("Choose a number from 1 to 7.")

    except Exception as error:
        print(f"Something went wrong: {error}")