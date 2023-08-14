import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image
import pymysql
import db_config


def load_data():
    try:
        con = pymysql.connect(host=db_config.DB_SERVER, user=db_config.DB_USER,
                              password=db_config.DB_PASS, database=db_config.DB)
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM First_Database.First_table;")
            return cursor.fetchall()
    except pymysql.Error as e:
        messagebox.showinfo("Database Error", e)
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
        image_paths= db_config.PHOTO_DIRECTORY + "default.jpeg"
        image = Image.open(image_paths)
        resized_img = image.resize((150, 150))
        return ImageTk.PhotoImage(resized_img)
    except FileNotFoundError:
        messagebox.showinfo("File Error", "Default image not found.")
        return None


def load_records():
    global row_counter, rows
    rows = load_data()
    row_counter = 0
    if rows:
        display_record()


def display_record():
    global row_counter, rows, num_rows
    num_rows = len(rows)
    if 0 <= row_counter < num_rows:
        record = rows[row_counter]
        fname_t1.set(record[1])
        lname_t1.set(record[2])
        job_t1.set(record[3])
        photo_path = db_config.PHOTO_DIRECTORY + record[4]
    else:
        fname_t1.set("")
        lname_t1.set("")
        job_t1.set("")
        photo_path = db_config.PHOTO_DIRECTORY + "default.jpeg"
    load_photo_tab1(photo_path)


def scroll_forward():
    global row_counter
    global num_rows
    if row_counter >= (num_rows - 1):
        messagebox.showinfo("Database Error", " End of Database")
    else:
        row_counter = row_counter + 1
        fname_t1.set(rows[row_counter][1])
        lname_t1.set(rows[row_counter][2])
        job_t1.set(rows[row_counter][3])
        try:
            ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][4]
            load_photo_tab1(ph_path)
        except FileNotFoundError:
            load_photo_tab1(db_config.PHOTO_DIRECTORY + "default.jpeg")


def scroll_backward():
    global row_counter
    global num_rows
    if row_counter == (num_rows + 1):
        messagebox.showinfo("Database Error", " End of Database")
    else:
        row_counter = row_counter - 1
        fname_t1.set(rows[row_counter][1])
        lname_t1.set(rows[row_counter][2])
        job_t1.set(rows[row_counter][3])
        try:
            ph_path = db_config.PHOTO_DIRECTORY + rows[row_counter][4]
            load_photo_tab1(ph_path)
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
    image = load_default_image()
    img_labelt2.configure(image=image)
    img_labelt2.image = image


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
            sql = "INSERT INTO tbl_employees(First_Name, Last_Name, Job_Title, PHOTO) VALUES (%s, %s, %s, %s)"
            vals = (first_field, family_field, job_field, image_field)
            cursor.execute(sql, vals)
        con.commit()
        messagebox.showinfo("Database", "Record added to Database")
    except pymysql.Error as e:
        messagebox.showinfo("Database Error", e)


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
new_height = 400

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

tab_parent.bind("<<NotebookTabChanged>>", on_tab_select)
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

'Tab One'
fname_label = tk.Label(tab_child1, text="First Name:")
lname_label = tk.Label(tab_child1, text="Last Name:")
job_label = tk.Label(tab_child1, text="Job Title:")

fname_entry = tk.Entry(tab_child1, textvariable=fname_t1)
lname_entry = tk.Entry(tab_child1, textvariable=lname_t1)
job_entry = tk.Entry(tab_child1, textvariable=job_t1)

fname_label.grid(row=0, column=0, pady=7)
lname_label.grid(row=1, column=0, pady=7)
job_label.grid(row=2, column=0, pady=7)

fname_entry.grid(row=0, column=1, padx=8)
lname_entry.grid(row=1, column=1, padx=8)
job_entry.grid(row=2, column=1, padx=8)

back_btn = tk.Button(tab_child1, text="Back", command=scroll_backward)
forward_btn = tk.Button(tab_child1, text="Forward", command=scroll_forward)

back_btn.grid(row=3, column=0, columnspan=2, pady=10)
forward_btn.grid(row=3, column=2, pady=10)

img_labelt1 = tk.Label(tab_child1, image=None)
img_labelt1.grid(row=0, column=2, rowspan=3, pady=15, padx=15)

'Tab Two'
fname_label_add = tk.Label(tab_child2, text="First Name:")
lname_label_add = tk.Label(tab_child2, text="Last Name:")
job_label_add = tk.Label(tab_child2, text="Job Title:")

fname_entry_add = tk.Entry(tab_child2, textvariable=fname_t2)
lname_entry_add = tk.Entry(tab_child2, textvariable=lname_t2)
job_entry_add = tk.Entry(tab_child2, textvariable=job_t2)

fname_label_add.grid(row=0, column=0, pady=7)
lname_label_add.grid(row=1, column=0, pady=7)
job_label_add.grid(row=2, column=0, pady=7)

fname_entry_add.grid(row=0, column=1, padx=8)
lname_entry_add.grid(row=1, column=1, padx=8)
job_entry_add.grid(row=2, column=1, padx=8)

add_btn = tk.Button(tab_child2, text="Add Record", command=add_record)
add_img = tk.Button(tab_child2, text="Add Image", command=select_image)

add_btn.grid(row=3, column=0, columnspan=2, pady=10)
add_img.grid(row=3, column=2, pady=10)

img_labelt2 = tk.Label(tab_child2, image=None)
img_labelt2.grid(row=0, column=2, rowspan=3, pady=15, padx=15)

tab_parent.pack(expand=1, fill='both')

rows = load_data()
if rows:
    display_record()

form.mainloop()
