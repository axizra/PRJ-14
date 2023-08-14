import tkinter as tk
from tkinter import filedialog, messagebox
import math
from tkinter import *

# Create the Tkinter window
form = tk.Tk()
form.title("Student Database [GUI]")
form.config(bg="#8b451d")

new_width = 645
new_height = 500

# Get the screen width and height
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x = math.floor((screen_width - 800) / 2)  # Adjust 800 to the desired width of the window
y = math.floor((screen_height - 600) / 2)  # Adjust 600 to the desired height of the window

# Set the window's position and size
form.geometry(f"800x600+{x}+{y}")

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
                for line in lines:
                    values = line.strip().split(':')
                    if len(values) >= 2:
                        key, value = values[0], values[1].strip()
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                        student[key] = value
            messagebox.showinfo("Success", "Student details imported successfully!")
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
    elif not name or student_class or address or contact:
        messagebox.showinfo("Invalid", "Please enter the details")
        return

    names_fn()
    message.config(text=check_student())
    details_entry.destroy()

    # Update the dropdown menu after saving the data
    show_dropdown()



def show_student_details(*args):
    global student
    selected_name = clicked.get()
    if selected_name == "None":
        return

    selected_student = None
    for student_id, student_data in student.items():
        if student_data["Name"] == selected_name:
            selected_student = student_data
            break

    if selected_student:
        student_info_text = ""
        for key, value in selected_student.items():
            student_info_text += f"{key}: {value}\n"
        show_menu(f"Details of {selected_name}", student_info_text)



def title_showmenu():
    global name
    global title_no_name, title_name
    if not name:
        return "Invalid"
    else:
        name_show = str(name)
        return "Details of " + name_show


def show_menu(title, student_info_text):
    global nameEntry
    global title_no_name, title_name
    global no_data, student_info_label1
    showmenu = tk.Toplevel(form)
    showmenu.title(title)

    new_width = 350
    new_height = 350

    # Calculate the x and y coordinates for the window to be centered
    screen_width = form.winfo_screenwidth()
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2  # Set the y-coordinate to 0 to position the window at the top

    # Set the window's position and size
    showmenu.geometry(f"{new_width}x{new_height}+{x}+{y}")
    showmenu.minsize(new_width, new_height)
    showmenu.maxsize(new_width, new_height)

    student_info_label = tk.Label(showmenu, font=("Times New Roman", 23, "bold"), text=student_info_text, bg="#4a411d")
    student_info_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Center the labels within the cell
    showmenu.grid_rowconfigure(0, weight=1)
    showmenu.grid_rowconfigure(1, weight=1)
    showmenu.grid_columnconfigure(0, weight=1)
    showmenu.grid_columnconfigure(1, weight=1)

    showmenu.config(bg="#4a411d")
    showmenu.mainloop()




def clear_student():
    global student
    student.clear()




def check_student():
    global student
    if not student:
        return "Currently, there are no existing student records"
    else:
        return "List of Students with Stored Details:\n" + "\n" + numbered_names()


def numbered_names():
    names_num = [f"{i + 1}. {name}" for i, name in enumerate(names_fn())]
    return "\n".join(names_num)


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

    nameLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Name: ", justify='center',
                         bg="#4a411d")
    nameEntry = tk.Entry(details_entry, bg="#6f6b5c")

    classLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Class: ", justify='center',
                          bg="#4a411d")
    classEntry = tk.Entry(details_entry, bg="#6f6b5c")

    addressLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Address :", justify='center',
                            bg="#4a411d")
    addressEntry = tk.Entry(details_entry, bg="#6f6b5c")

    contactLabel = tk.Label(details_entry, font=("Times New Roman", 14, "bold"), text="Contact :", justify='center',
                            bg="#4a411d")
    contactEntry = tk.Entry(details_entry, bg="#6f6b5c")

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

    details_entry.config(bg="#4a411d")

    return details_entry

name_no = []


def names_fn():
    global student, name_no
    name_no = [f"{student[id]['Name']}" for id in student]
    return name_no

def show_dropdown(*args):
    global clicked
    if not name_no:
        drop['menu'].delete(0, 'end')
        drop['menu'].add_command(label="None", command=tk._setit(clicked, "None"))
        clicked.set("Show")
    else:
        drop['menu'].delete(0, 'end')
        for name in name_no:
            drop['menu'].add_command(label=name, command=tk._setit(clicked, name))
        clicked.set("Show")
'-----------------------------------------------------------------------------------------------------------------------'

'Main Menu'

form.minsize(new_width, new_height)
form.maxsize(new_width, new_height)

space1 = tk.Label(form, bg="#4a411d")
message = tk.Label(form, font=("Times New Roman", 22, "bold"), text=check_student(), fg="#d9d4cc", bg="#4a411d")

space1.grid(row=1, column=0)
message.grid(row=4, column=0, columnspan=6, padx=10, pady=15, sticky="nsew")

enter_button = tk.Button(form, text="Enter", command=entry_details, bg="#4a411d")
display_button = tk.Button(form, text="Show", command=show_student_details, bg="#4a411d")
clear_button = tk.Button(form, text="Clear", command=clear_student, bg="#4a411d")



# Add an empty label to the left of the buttons to center them
empty_label_left = tk.Label(form, bg="#4a411d")
empty_label_left.grid(row=6, column=0)

# Place the buttons in the center columns (column=1, column=2, column=3)
enter_button.grid(row=6, column=1, padx=25, pady=25)
clear_button.grid(row=6, column=3, padx=25, pady=25)

# Add an empty label to the right of the buttons to center them
empty_label_right = tk.Label(form, bg="#4a411d")
empty_label_right.grid(row=6, column=4)



clicked = tk.StringVar()
clicked.set("Show")
drop = tk.OptionMenu(form, clicked, "None")
drop.grid(row=6, column=2, padx=25, pady=25)

clicked.trace('w', show_dropdown)
drop.bind("<ButtonRelease-1>", lambda event: show_menu(title_showmenu(), student_info_text))


# Configure column widths to center the buttons
form.grid_columnconfigure(0, weight=1)
form.grid_columnconfigure(1, weight=1)
form.grid_columnconfigure(2, weight=1)
form.grid_columnconfigure(3, weight=1)
form.grid_columnconfigure(4, weight=1)


menuBar = tk.Menu(form)
Items = tk.Menu(menuBar)
Items.add_command(label="New", command="")
Items.add_command(label="Import", command=import_file)
Items.add_command(label="Export", command=save_file)
Items.add_command(label="Update", command="")
Items.add_command(label="Exit", command=form.quit)
menuBar.add_cascade(label="File", menu=Items)
form.config(menu=menuBar, bg="#4a411d")

form.resizable(False, False)
form.mainloop()
