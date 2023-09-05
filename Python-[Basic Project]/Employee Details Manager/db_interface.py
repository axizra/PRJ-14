import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image
import pymysql
import db_config
import shutil
import os
import ttkthemes


def load_data():
    try:
        con = pymysql.connect(host=db_config.DB_SERVER, user=db_config.DB_USER,
                              password=db_config.DB_PASS, database=db_config.DB)
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_database.employee_details;")
            return cursor.fetchall()
    except pymysql.Error as e:
        messagebox.showinfo("Database Error", str(e))
        return []


def on_tab_select(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "All Record":
        load_records()
    elif tab_text == "Add New Record":
        load_photo_tab2()


def load_default_image():
    try:
        image_paths = "/Users/axizra/Documents/Python-Data Science[BASIC]/Projects/Employee Details Manager/Sample Photos/default.jpeg"  # Provide the correct absolute path
        image = Image.open(image_paths)
        resized_img = image.resize((150, 150))
        return ImageTk.PhotoImage(resized_img)
    except FileNotFoundError:
        messagebox.showinfo("File Error", "Default image not found.")
        return None


def load_records():
    global row_counter, rows, num_rows
    rows = load_data()
    row_counter = 0
    num_rows = len(rows)
    if rows:
        display_record()


def display_record():
    global row_counter, rows, num_rows
    num_rows = len(rows)
    if 0 <= row_counter < num_rows:
        record = rows[row_counter]
        fname_t1.set(record[0])
        lname_t1.set(record[1])
        job_t1.set(record[2])
        photo_path = db_config.PHOTO_DIRECTORY + record[3]
    else:
        fname_t1.set("")
        lname_t1.set("")
        job_t1.set("")
        photo_path = db_config.PHOTO_DIRECTORY + "default.jpeg"
    load_photo_tab1(photo_path)


def scroll_forward():
    global row_counter
    global num_rows, rows
    num_rows = len(rows)
    if row_counter >= (num_rows - 1):
        messagebox.showinfo("Database Error", " End of Database")
    else:
        row_counter = row_counter + 1
        fname_t1.set(rows[row_counter][0])
        lname_t1.set(rows[row_counter][1])
        job_t1.set(rows[row_counter][2])
        try:
            ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][3]
            load_photo_tab1(ph_path)
        except FileNotFoundError:
            load_photo_tab1(db_config.PHOTO_DIRECTORY + "default.jpeg")


def scroll_backward():
    global row_counter
    global num_rows, rows
    num_rows = len(rows)
    if row_counter == 0:
        messagebox.showinfo("Database Error", " Start of Database")
    else:
        row_counter = row_counter - 1
        fname_t1.set(rows[row_counter][0])
        lname_t1.set(rows[row_counter][1])
        job_t1.set(rows[row_counter][2])
        try:
            ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][3]  # Update the index to 3
            load_photo_tab1(ph_path)  # Update the image
        except FileNotFoundError:
            load_photo_tab1(db_config.PHOTO_DIRECTORY + "default.jpeg")


def image_path(file_path):
    open_image = Image.open(file_path)
    resized_img = open_image.resize((150, 150))
    return ImageTk.PhotoImage(resized_img)


def load_photo_tab1(file_path):
    try:
        image = image_path(file_path)
    except FileNotFoundError:
        image = image_path(db_config.PHOTO_DIRECTORY + "default.jpeg")
    img_labelt1.configure(image=image)
    img_labelt1.image = image


def load_photo_tab2():
    global image_selected, file_to_copy, img_labelt2

    if image_selected and file_to_copy:
        try:
            image = image_path(file_to_copy)
            img_labelt2.configure(image=image)
            img_labelt2.image = image
        except FileNotFoundError:
            messagebox.showinfo("File Error", "Selected image not found.")
    else:
        default_image = load_default_image()
        img_labelt2.configure(image=default_image)
        img_labelt2.image = default_image


def select_image():
    global image_selected, image_file_name, file_new_home, file_to_copy
    path_to_image = filedialog.askopenfilename(initialdir="/", title="Open File",
                                               filetypes=(("jpeg", "*.jpeg"), ("GIFs", "*.gif"), ("All Files", "*.*")))
    try:
        if path_to_image:
            image_file_name = path_to_image.split("/")[-1]
            file_new_home = db_config.PHOTO_DIRECTORY + image_file_name
            file_to_copy = path_to_image
            image_selected = True
            load_photo_tab2()

    except IOError as err:
        image_selected = False
        messagebox.showinfo("File Error", err)

    # Move the selected image to the "Sample Photos" folder
    destination_path = "/Users/axizra/Documents/Python-Data Science[BASIC]/Projects/Employee Details Manager/Sample Photos/"
    new_image_path = os.path.join(destination_path, image_file_name)
    shutil.copy(file_to_copy, new_image_path)


def add_record():
    global image_file_name
    global blank_textboxes_t2
    global file_newhome
    global file_tocopy
    blank_textbox_count = 0
    if fname_t2.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if lname_t2.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if job_t2.get() == "":
        blank_textbox_count = blank_textbox_count + 1
    if blank_textbox_count > 0:
        blank_textboxes_t2 = True
        messagebox.showinfo("Database Error", "Black Text Boxes")
    elif blank_textbox_count == 0:
        blank_textboxes_t2 = False

    if image_selected:
        insert_into_database(fname_t2.get(), lname_t2.get(), job_t2.get(), image_file_name)
    else:
        messagebox.showinfo("File Error", "Please Select an Image")


def insert_into_database(first_field, family_field, job_field, image_field):
    try:
        con = pymysql.connect(host=db_config.DB_SERVER, user=db_config.DB_USER,
                              password=db_config.DB_PASS, database=db_config.DB)
        with con.cursor() as cursor:
            sql = "INSERT INTO employee_details(first_Name, last_Name, job_Title, photo) VALUES (%s, %s, %s, %s)"
            vals = (first_field, family_field, job_field, image_field)
            cursor.execute(sql, vals)
        con.commit()
        messagebox.showinfo("Database", "Record added to Database")
        load_records()
    except pymysql.Error as e:
        messagebox.showinfo("Database Error", str(e))


image_selected = False
image_file_name = None
file_to_copy = None
file_new_home = None
blank_textboxes_t2 = True

rows = None
num_rows = None
row_counter = 0

form = tk.Tk()
form.title("Employee Database")
form.geometry("530x400")

new_width = 530
new_height = 320

# Calculate the x and y coordinates for the window to be centered
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width - new_width) // 2
y = (screen_height - new_height) // 2

form.geometry(f"{new_width}x{new_height}+{x}+{y}")
form.minsize(new_width, new_height)
form.maxsize(new_width, new_height)

tab_parent = ttk.Notebook(form)
tab_child1 = ttk.Frame(tab_parent)
tab_child2 = ttk.Frame(tab_parent)

style = ttkthemes.ThemedStyle(form)
style.set_theme("breeze")
style.configure("TNotebook", titlebackground=style.lookup("TFrame", "background"))

tab_parent.add(tab_child1, text="All Record")
tab_parent.add(tab_child2, text="Add New Record")

' String Variables'
# Tab One
fname_t1 = tk.StringVar()
lname_t1 = tk.StringVar()
job_t1 = tk.StringVar()

# Tab Two
fname_t2 = tk.StringVar()
lname_t2 = tk.StringVar()
job_t2 = tk.StringVar()

# Update the font size and other styling attributes
font_style = ("Helvetica", 14)  # Choose a suitable font and size
label_style = ("Helvetica", 13)  # Font for labels

'Tab One'
fname_label = tk.Label(tab_child1, text="First Name:", font=label_style)
lname_label = tk.Label(tab_child1, text="Last Name:", font=label_style)
job_label = tk.Label(tab_child1, text="Job Title:", font=label_style)

fname_entry = tk.Entry(tab_child1, textvariable=fname_t1, font=label_style)
lname_entry = tk.Entry(tab_child1, textvariable=lname_t1, font=label_style)
job_entry = tk.Entry(tab_child1, textvariable=job_t1, font=label_style)

back_btn = tk.Button(tab_child1, text="Back", command=scroll_backward, font=label_style)
forward_btn = tk.Button(tab_child1, text="Forward", command=scroll_forward, font=label_style)

default_image = load_default_image()
img_labelt1 = tk.Label(tab_child1, image=default_image)
img_labelt1.image = default_image

# Inside Tab One
fname_label.grid(row=0, column=0, pady=7, padx=(30, 0), sticky="e")
lname_label.grid(row=1, column=0, pady=7, padx=(30, 0), sticky="e")
job_label.grid(row=2, column=0, pady=7, padx=(30, 0), sticky="e")

fname_entry.grid(row=0, column=1, padx=(5, 20), pady=7, sticky="w")
lname_entry.grid(row=1, column=1, padx=(5, 20), pady=7, sticky="w")
job_entry.grid(row=2, column=1, padx=(5, 20), pady=7, sticky="w")

back_btn.grid(row=3, column=0, columnspan=2, pady=40, padx=80, sticky="w")
forward_btn.grid(row=3, column=2, pady=10, padx=20, sticky="e")

img_labelt1.grid(row=0, column=2, rowspan=3, pady=15, padx=15, sticky="nswe")

'Tab Two'
fname_label_add = tk.Label(tab_child2, text="First Name:", font=label_style)
lname_label_add = tk.Label(tab_child2, text="Last Name:", font=label_style)
job_label_add = tk.Label(tab_child2, text="Job Title:", font=label_style)

fname_entry_add = tk.Entry(tab_child2, textvariable=fname_t2)
lname_entry_add = tk.Entry(tab_child2, textvariable=lname_t2)
job_entry_add = tk.Entry(tab_child2, textvariable=job_t2)

add_btn = tk.Button(tab_child2, text="Add Record", command=add_record, font=label_style)
add_img = tk.Button(tab_child2, text="Add Image", command=select_image, font=label_style)

default_image = load_default_image()
img_labelt2 = tk.Label(tab_child2, image=default_image)
img_labelt2.image = default_image

# Inside Tab One
fname_label_add.grid(row=0, column=0, pady=7, padx=(30, 0), sticky="e")
lname_label_add.grid(row=1, column=0, pady=7, padx=(30, 0), sticky="e")
job_label_add.grid(row=2, column=0, pady=7, padx=(30, 0), sticky="e")

fname_entry_add.grid(row=0, column=1, padx=(5, 20), pady=7, sticky="w")
lname_entry_add.grid(row=1, column=1, padx=(5, 20), pady=7, sticky="w")
job_entry_add.grid(row=2, column=1, padx=(5, 20), pady=7, sticky="w")

add_btn.grid(row=3, column=0, columnspan=2, pady=40, padx=80, sticky="w")
add_img.grid(row=3, column=2, pady=10, padx=20, sticky="e")

img_labelt2.grid(row=0, column=2, rowspan=3, pady=15, padx=35, sticky="nswe")

tab_parent.pack(expand=1, fill='both')

rows = load_data()
if rows:
    display_record()

form.mainloop()
