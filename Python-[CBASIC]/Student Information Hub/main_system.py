import tkinter as tk
from tkinter import filedialog, messagebox
import math
from tkinter import *

# Create the Tkinter window
form = tk.Tk()
form.title("Student Database")

new_width = 645
new_height = 300

# Get the screen width and height
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x = (screen_width - new_width) // 2
y = (screen_height - new_height) // 2

# Set the window's position and size
form.geometry(f"{new_width}x{new_height}+{x}+{y}")

filename = ""
student = {}
name, student_class, address, contact = "", "", "", ""
classEntry, addressEntry, contactEntry, details_entry, nameEntry = None, None, None, None, None
no_data, student_info_label = None, None
student_info_text = ""


def save_file():
    global filename
    save_text = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if save_text:
        if save_text:
            for key, value in student.items():
                save_text.write(f"{key}: {value}\n")
        save_text.close()
        messagebox.showinfo("Success", "Student details saved successfully")
    else:
        messagebox.showinfo("Error", "Cancelled")


def import_file():
    global filename, student
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Open File",
                                          filetypes=(("Text Files", "*.txt"), ("All Files", ".*")))

    try:
        if filename:
            student = {}
            with open(filename, 'r') as file:
                lines = file.readlines()
                current_student = {}
                for line in lines:
                    values = line.strip().split(':')
                    if len(values) >= 2:
                        key, value = values[0], values[1].strip()
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                        current_student[key] = value
                student[len(student) + 1] = current_student  # Assign current_student under a unique ID
            messagebox.showinfo("Success", "Student details imported successfully!")
            update_name_dropdown()
            message.config(text=check_student())
        elif not filename:
            messagebox.showinfo("Cancel", "You Clicked Cancel")
    except IOError:
        messagebox.showinfo("Error", "Could not open file")


def save_data():
    global name, student_class, address, contact, student
    name = nameEntry.get()
    student_class = classEntry.get()
    address = addressEntry.get()
    contact = contactEntry.get()
    if name and student_class and address and contact:
        student_id = len(student) + 1
        student[student_id] = {
            "Name": name,
            "Class": student_class,
            "Address": address,
            "Contact": contact
        }
        update_name_dropdown()
        clicked.set(name)
    elif not name or student_class or address or contact:
        messagebox.showinfo("Invalid", "Please enter the details")
        return

    names_fn()
    message.config(text=check_student())
    details_entry.destroy()
    update_name_dropdown()


def update_name_dropdown():
    global name_dropdown, student_names, clicked
    student_names = ["None"] + [student_data["Name"] for student_id, student_data in student.items()]
    clicked.set(student_names[0])
    name_dropdown['menu'].delete(0, 'end')
    for name in student_names:
        name_dropdown['menu'].add_command(label=name, command=tk._setit(clicked, name))


def show_student_details():
    selected_name = clicked.get()
    if selected_name == "None":
        messagebox.showinfo("No Details", "No details are available for display.")
        return

    selected_student = next((student_data for student_id, student_data in student.items()
                             if student_data["Name"] == selected_name), None)

    if selected_student:
        student_info_text = "\n".join([f"{key}: {value}" for key, value in selected_student.items()])
        show_menu(f"Details of {selected_name}", student_info_text)
        clicked.set(selected_name)
        update_name_dropdown()


def show_menu(title, content):
    showmenu = tk.Toplevel(form)
    showmenu.title(title)

    new_width = 250
    new_height = 250

    # Calculate the x and y coordinates for the window to be centered
    screen_width = form.winfo_screenwidth()
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2  # Set the y-coordinate to 0 to position the window at the top

    # Set the window's position and size
    showmenu.geometry(f"{new_width}x{new_height}+{x}+{y}")
    showmenu.minsize(new_width, new_height)
    showmenu.maxsize(new_width, new_height)

    student_info_label = tk.Label(showmenu, font=("Times New Roman", 23, "bold"), text=content)
    student_info_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Center the labels within the cell
    showmenu.grid_rowconfigure(0, weight=1)
    showmenu.grid_rowconfigure(1, weight=1)
    showmenu.grid_columnconfigure(0, weight=1)
    showmenu.grid_columnconfigure(1, weight=1)

    showmenu.mainloop()


def title_showmenu():
    global name
    global title_no_name, title_name
    if not name:
        return "Invalid"
    else:
        name_show = str(name)
        return "Details of " + name_show


def clear_student():
    global student
    student.clear()
    message.config(text="Currently, there are no existing student records")
    update_name_dropdown()


def check_student():
    global student
    if not student:
        return "Currently, there are no existing student records"
    else:
        return "List of Students with Stored Details:\n" + "\n".join(numbered_names())


def numbered_names():
    global student
    names_num = [f"{i + 1}. {student_data['Name']}" for i, student_data in enumerate(student.values())]
    return names_num


name_no = []


def names_fn():
    global student
    name_no = [student_data['Name'] for student_data in student.values()]
    return name_no


def entry_details():
    global classEntry, addressEntry, contactEntry, details_entry, nameEntry
    details_entry = tk.Toplevel(form)
    details_entry.title("Student Details Entry")

    new_width = 250
    new_height = 275

    # Calculate the x and y coordinates for the window to be centered
    screen_width = form.winfo_screenwidth()
    screen_height = form.winfo_screenheight()
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2

    # Set the window's position and size
    details_entry.geometry(f"{new_width}x{new_height}+{x}+{y}")
    details_entry.minsize(new_width, new_height)
    details_entry.maxsize(new_width, new_height)

    nameLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Name: ", justify='center')
    nameEntry = tk.Entry(details_entry)

    classLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Class: ", justify='center')
    classEntry = tk.Entry(details_entry)

    addressLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Address :", justify='center')
    addressEntry = tk.Entry(details_entry)

    contactLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Contact :", justify='center')
    contactEntry = tk.Entry(details_entry)

    nameLabel.pack(fill=tk.BOTH, padx=6, pady=1)
    nameEntry.pack(padx=6, pady=1)

    classLabel.pack(fill=tk.BOTH, padx=6, pady=1)
    classEntry.pack(padx=6, pady=1)

    addressLabel.pack(fill=tk.BOTH, padx=6, pady=1)
    addressEntry.pack(padx=6, pady=1)

    contactLabel.pack(fill=tk.BOTH, padx=6, pady=1)
    contactEntry.pack(padx=6, pady=1)

    savebtn = tk.Button(details_entry, text="Save", command=save_data)
    savebtn.pack(padx=15, pady=10)

    return details_entry


def exit_main():
    clear_student()
    form.quit()


'-----------------------------------------------------------------------------------------------------------------------'

'Main Menu'

form.minsize(new_width, new_height)
form.maxsize(new_width, new_height)

space1 = tk.Label(form)
message = tk.Label(form, font=("Times New Roman", 22, "bold"), text=check_student())

space1.grid(row=1, column=0)
message.grid(row=4, column=0, columnspan=6, padx=10, pady=15, sticky="nsew")

enter_button = tk.Button(form, text="Enter", command=entry_details)
clear_button = tk.Button(form, text="Clear", command=clear_student)

# Add an empty label to the left of the buttons to center them
empty_label_left = tk.Label(form)
empty_label_left.grid(row=6, column=0)

# Place the buttons in the center columns (column=1, column=2, column=3)
enter_button.grid(row=6, column=1, padx=25, pady=25)
clear_button.grid(row=6, column=3, padx=25, pady=25)

student_names = [student_data["Name"] for student_id, student_data in student.items()]
student_names.insert(0, "None")
clicked = tk.StringVar()
clicked.set(student_names[0])  # Set default value to "None"
name_dropdown = tk.OptionMenu(form, clicked, *student_names)
name_dropdown.configure(fg="black")
name_dropdown.grid(row=6, column=2, padx=25, pady=25)

# Create the "Show Details" button
show_details_button = tk.Button(form, text="Show Details", command=show_student_details)
show_details_button.grid(row=7, column=2, padx=25, pady=25)

# Configure column widths to center the buttons
form.grid_columnconfigure(0, weight=1)
form.grid_columnconfigure(1, weight=1)
form.grid_columnconfigure(2, weight=1)
form.grid_columnconfigure(3, weight=1)
form.grid_columnconfigure(4, weight=1)

menuBar = tk.Menu(form)
Items = tk.Menu(menuBar)
Items.add_command(label="Import", command=import_file)
Items.add_command(label="Export", command=save_file)
Items.add_command(label="Exit", command=exit_main)
menuBar.add_cascade(label="File", menu=Items)
form.config(menu=menuBar)

form.mainloop()
