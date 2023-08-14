def load_photo_tab1(file_path):
    image = image_path(file_path)
    img_labelt1.configure(image=image)
    img_labelt1.image = image

    import os.path
    import shutil
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    from PIL import ImageTk, Image
    import db_config
    import pymysql

    def on_tab_select(event):
        global blank_textboxes_t2
        global image_selected
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "All Record":
            if (blank_textboxes_t2 is False) and (image_selected is True):
                load_db()
        elif tab_text == "Add New Record":
            blank_textboxes_t2 = True
            image_selected = False

    def load_db():
        global rows
        global num_rows
        try:
            con = pymysql.connect(host=db_config.DB_SERVER,
                                  user=db_config.DB_USER,
                                  password=db_config.DB_PASS,
                                  database=db_config.DB)

            sql = "SELECT * FROM First_Database.First_table;"
            cursor = con.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            num_rows = cursor.rowcount
            cursor.close()
            con.close()
            loaded_successfully = True

        except pymysql.InternalError as e:
            loaded_successfully = database_error(e)

        except pymysql.OperationalError as e:
            loaded_successfully = database_error(e)

        except pymysql.ProgrammingError as e:
            loaded_successfully = database_error(e)

        except pymysql.DataError as e:
            loaded_successfully = database_error(e)

        except pymysql.IntegrityError as e:
            loaded_successfully = database_error(e)

        except pymysql.NotSupportedError as e:
            loaded_successfully = database_error(e)

        return loaded_successfully

    def database_error(err):
        messagebox.showinfo("Error", err)
        return False

    def image_path(file_path):
        open_image = Image.open(file_path)
        resized_img = open_image.resize((150, 150))
        image = ImageTk.PhotoImage(resized_img)
        return image

    def load_photo_tab1(file_path):
        image = image_path(file_path)
        img_labelt1.configure(image=image)
        img_labelt1.image = image

    def load_photo_tab2(file_path):
        image = image_path(file_path)
        img_labelt2.configure(image=image)

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

    def select_image():
        global image_selected
        global image_file_name
        global file_new_home
        global file_to_copy
        path_to_image = filedialog.askopenfilename(initialdir="/",
                                                   title="Open File",
                                                   filetypes=(
                                                   ("jpeg", "*.jpeg"), ("GIFs", "*.gif"), ("All Files", "*.*")))
        try:
            if path_to_image:
                image_file_name = os.path.basename(path_to_image)
                file_new_home = db_config.PHOTO_DIRECTORY + image_file_name
                file_to_copy = path_to_image
                image_selected = True
                load_photo_tab2(file_to_copy)
        except IOError as err:
            image_selected = False
            messagebox.showinfo("File Error", err)

    def add_record():
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
            insert_into_database(fname_t2.get(), lname_t2.get(), job_t2.get(), image_filename)
        else:
            messagebox.showinfo("File Error", "Please Select an Image")

    def insert_into_database(first_field, family_field, job_field, image_field):
        con = pymysql.connect(host=db_config.DB_SERVER,
                              user=db_config.DB_USER,
                              password=db_config.DB_PASS,
                              database=db_config.DB)
        sql = "INSERT INTO tbl_employees( First Name, Last Name, Job Title, PHOTO) VALUES (∞S, ∞S, ∞S, ∞S)"
        vals = (first_field, family_field, job_field, image_field)
        cursor = con.cursor()
        cursor.execute(sql, vals)
        con.commit()
        cursor.close()
        con.close()
        messagebox.showinfo("Databse", "Record added to Database")

    image_selected = False
    image_filename = None
    file_tocopy = None
    file_newhome = None
    blank_textboxes_t2 = True

    file_name = "default.jpeg"
    path = db_config.PHOTO_DIRECTORY + file_name
    rows = None
    num_rows = None
    row_counter = 0

    form = tk.Tk()
    form.title("Employee Database")

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

    space1 = tk.Label(tab_child1, text="", pady=3, bg="#3a3b3b")
    first_n = tk.Label(tab_child1, text="First Name: ", bg="#3a3b3b")
    last_n = tk.Label(tab_child1, text="Last Name: ", bg="#3a3b3b")
    job_label = tk.Label(tab_child1, text="Job Title: ", bg="#3a3b3b")

    fname_entry = tk.Entry(tab_child1, textvariable=fname_t1)
    lname_entry = tk.Entry(tab_child1, textvariable=lname_t1)
    job_entry = tk.Entry(tab_child1, textvariable=job_t1)

    space1.grid(row=0, column=0, pady=3)
    first_n.grid(row=1, column=0, pady=7)
    last_n.grid(row=2, column=0, pady=7)
    job_label.grid(row=3, column=0, pady=7)

    fname_entry.grid(row=1, column=1, padx=8)
    lname_entry.grid(row=2, column=1, padx=8)
    job_entry.grid(row=3, column=1, padx=8)

    back_btn = tk.Button(tab_child1, text="Back", bg="#3a3b3b", command=scroll_backward)
    forward_btn = tk.Button(tab_child1, text="Forward", bg="#3a3b3b", command=scroll_forward)

    space1 = tk.Label(tab_child1, text="", pady=3, bg="#3a3b3b")
    space1.grid(row=4, column=0, pady=3)

    back_btn.grid(row=5, column=0, columnspan=2)
    forward_btn.grid(row=5, column=2)

    openimg_tab1 = Image.open(path)
    resized_imgt1 = openimg_tab1.resize((150, 150))
    img_t1 = ImageTk.PhotoImage(resized_imgt1)
    img_labelt1 = tk.Label(tab_child1, image=img_t1)
    img_labelt1.grid(row=1, column=2, rowspan=3, pady=15, padx=15)

    'Tab Two'

    space1 = tk.Label(tab_child2, text="", pady=3, bg="#3a3b3b")
    first_n_add = tk.Label(tab_child2, text="First Name: ", bg="#3a3b3b")
    last_n_add = tk.Label(tab_child2, text="Last Name: ", bg="#3a3b3b")
    job_add = tk.Label(tab_child2, text="Job Title: ", bg="#3a3b3b")

    fname_entry_add = tk.Entry(tab_child2, textvariable=fname_t2)
    lname_entry_add = tk.Entry(tab_child2, textvariable=lname_t2)
    job_entry_add = tk.Entry(tab_child2, textvariable=job_t2)

    space1.grid(row=0, column=0, pady=3)
    first_n_add.grid(row=1, column=0, pady=7)
    last_n_add.grid(row=2, column=0, pady=7)
    job_add.grid(row=3, column=0, pady=7)

    fname_entry_add.grid(row=1, column=1, padx=8)
    lname_entry_add.grid(row=2, column=1, padx=8)
    job_entry_add.grid(row=3, column=1, padx=8)

    add_btn = tk.Button(tab_child2, text="Add Record", bg="#3a3b3b", command=add_record)
    add_img = tk.Button(tab_child2, text="Add Image", bg="#3a3b3b", command=select_image)

    space1 = tk.Label(tab_child2, text="", pady=3, bg="#3a3b3b")
    space1.grid(row=4, column=0, pady=3)

    add_btn.grid(row=5, column=0, columnspan=2)
    add_img.grid(row=5, column=2)

    ' Image '
    openimg_tab2 = Image.open(path)
    resized_imgt2 = openimg_tab2.resize((150, 150))
    img_t2 = ImageTk.PhotoImage(resized_imgt2)
    img_labelt2 = tk.Label(tab_child1, image=img_t2)
    img_labelt2.grid(row=1, column=2, rowspan=3, pady=15, padx=15)

    success = load_db()

    if success:
        fname_t1.set(rows[0][1])
        lname_t1.set(rows[0][2])
        job_t1.set(rows[0][3])
        photo_path = db_config.PHOTO_DIRECTORY + rows[0][4]
        load_photo_tab1(photo_path)

    tab_parent.pack(expand=1, fill='both')
    form.mainloop()
