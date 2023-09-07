from backend_expense import *


# Main program
def main():
    # Expense Dictionary
    global expenses
    expenses = {}

    # User Interaction Loop
    while True:
        print("----- Expense Tracker -----")
        print("1. Add an expense")
        print("2. Deduct an expense")
        print("3. Update an expense")
        print("4. Sort expenses")
        print("5. Export expenses")
        print("6. Import expenses from file")
        print("7. Show expenses")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            category = input("Enter the category: ")
            amount = float(input("Enter the amount: "))
            add_expense(expenses, category, amount)
            print("Expense added successfully!\n")

        elif choice == '2':
            category = input("Enter the category: ")
            amount = float(input("Enter the amount: "))
            deduct_expense(expenses, category, amount)
            print("Expense deducted successfully!\n")

        elif choice == '3':
            category = input("Enter the category: ")
            amount = float(input("Enter the new amount: "))
            update_expense(expenses, category, amount)
            print("Expense updated successfully!\n")

        elif choice == '4':
            max_key_length = max(len(key) for key in expenses.keys())  # Get the maximum key length

            for key, value in expenses.items():
                print(f"{key:>{max_key_length}} : {value}")


        elif choice == '5':
            filename = input("Enter the filename to export: ")
            export_expenses(expenses, filename)
            print("Expenses exported successfully!\n")

        elif choice == '6':
            filename = input("Enter the filename to import expenses from: ")
            expenses = load_expenses(filename)
            print("Expenses imported successfully!\n")


        elif choice == '7':
            for key, value in expenses.items():
                print(key, ":", value)

        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.\n")


# Run the main program
if __name__ == "__main__":
    main()
