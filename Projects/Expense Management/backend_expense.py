from expense_main import *
import numpy as np


# Function to add an expense
def add_expense(expenses, category, amount):
    if category in expenses:
        expenses[category] += amount
    else:
        expenses[category] = amount


# Function to deduct an expense
def deduct_expense(expenses, category, amount):
    if category in expenses:
        expenses[category] -= amount
        if expenses[category] < 0:
            expenses[category] = 0


# Function to update an expense
def update_expense(expenses, category, amount):
    if category in expenses:
        expenses[category] = amount


# Function to sort expenses
def sort_expenses(expenses):
    sorted_values = dict(sorted(expenses.values))  # Sort the values
    sorted_dict = {}
    print(sorted_values)
    for i in sorted_values:
        for k in expenses.keys():
            if expenses[k] == i:
                sorted_dict[k] = expenses[k]
    print(sorted_dict)


def sort_expense(expenses):
    keys = list(expenses.keys())
    values = list(expenses.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    print(sorted_dict)


def sort_expense1(expenses):
    print(sorted(expenses.values))


# Function to export expenses to a file
def export_expenses(expenses, filename):
    with open(filename, 'w') as file:
        file.write("Category,Amount\n")
        for category, amount in expenses.items():
            file.write(f"{category},{amount}\n")


def load_expenses(filename):
    global expenses
    expenses = {}

    with open(filename, 'r') as file:
        lines = file.readlines()[1:]  # Skip header row
        for line in lines:
            values = line.strip().split(':')
            if len(values) >= 2:
                category, amount = values[0], float(values[1])
                expenses[category] = amount

    return expenses
