import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
import mysql
from mysql.connector import Error
import pymysql
import random

ctk.set_appearance_mode("System")

connect_bar = None
used_ids = set()
global name, address, email, random_id
name = address = email = random_id =None


DB_SERVER = "localhost"
DB_USER = "root"
DB_PASS = "crest008"
DB = "cms"


class login_user():
    def __init__(self, login):
        self.login = login
        self.login.title("Login")
        win_width = 590
        win_height = 240
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.login.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.login.minsize(win_width, win_height)
        self.login.maxsize(win_width, win_height)


        def congrats_win():
            win = ctk.CTk()

            win_width = 200
            win_height = 150
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()
            x = (screen_width - win_width) // 2
            y = (screen_height - win_height) // 2
            win.geometry(f"{win_width}x{win_height}+{x}+{y}")
            win.minsize(win_width, win_height)
            win.maxsize(win_width, win_height)


            win.mainloop()

        def generate_unique_random_id(used_ids):
            while True:
                random_id = random.randint(10000, 99999)
                if random_id not in used_ids:
                    used_ids.add(random_id)
                    return random_id


        def add_credentials(name, address, email, used_ids):
            customer_id = generate_unique_random_id(used_ids)
            try:
                con = pymysql.connect(host=DB_SERVER, user=DB_USER, password=DB_PASS, database=DB)
                with con.cursor() as cursor:
                    sql = "INSERT INTO customer_details( id, name, address, email) VALUES(%s, %s, %s, %s)"
                    vals = (customer_id, name, address, email)
                    cursor.execute(sql, vals)
                con.commit()
                if name and address and email and used_ids:
                    congrats_win()
                elif not name or address or email or used_ids:
                    messagebox.showinfo("Invalid", "Please enter all the details")
            except pymysql.Error as e:
                messagebox.showinfo("Database Error", str(e))


        gif_path = "hi.gif"
        gif_image = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]

        gif_label = ctk.CTkLabel(master=self.login, image=gif_frames[0], text="")
        gif_label.place(x=350)

        def update_gif_frame(frame_index):
            gif_label.configure(image=gif_frames[frame_index])
            self.login.after(100, update_gif_frame, (frame_index + 1) % len(gif_frames))

        update_gif_frame(1)



        name_label = ctk.CTkLabel(master=self.login, text="Full Name: ",font=('Times',20), text_color="black")
        name = ctk.CTkEntry(master=self.login, width=212, height=30,font=('Times',16),
                             corner_radius=20, fg_color="#979593", border_color="#565455", text_color="black" )

        name_label.place(x=35, y=30)
        name.place(x=140, y=30)


        address_label = ctk.CTkLabel(master=self.login, text="Address: ",font=('Times',20), text_color="black")
        address = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16),
                              fg_color = "#979593", border_color = "#565455", text_color="black" )

        address_label.place(x=35, y=80)
        address.place(x=140, y=80)

        email_label = ctk.CTkLabel(master=self.login, text="E-mail: ",font=('Times',20), text_color="black")
        email = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16),
                             fg_color="#979593", border_color="#565455", text_color="black"   )

        email_label.place(x=35, y=130)
        email.place(x=140, y=130)


        confirm_btn = ctk.CTkButton(master=self.login, text="Confirm",font=('Times',19),height=32,
                                    corner_radius=22, text_color="black", border_width=2, border_color="#565455",
                                    fg_color="#979593", hover_color="#747273",
                                    command=lambda: add_credentials(name.get(), address.get(), email.get(), used_ids))
        confirm_btn.place(x=140, y=185)

        connect_bar = ctk.CTkProgressBar(master=self.login, orientation="horizontal",
                                                   progress_color="#979593", border_color="#a2a49c",
                                                   border_width=1,
                                                   width=win_width, height=5, mode="indeterminate")
        connect_bar.configure(determinate_speed=0.1, indeterminate_speed=2.5)
        connect_bar.pack()

        def start():
            connect_bar.configure(mode="determinate")
            connect_bar.set(0)

            def update_progress(progress):
                connect_bar.set(progress)
                self.login.update_idletasks()

            def fill_progress(progress):
                if progress <= 100:
                    update_progress(progress)
                    self.login.after(2, fill_progress, progress + 1)
                else:
                    connect_bar.stop()
                    connect_bar.destroy()

            self.login.after(1000, fill_progress, 1)

        def not_start():
            connect_bar.configure(mode="determinate")

            def switch_to_indeterminate():
                connect_bar.configure(mode="indeterminate")
                connect_bar.start()
                self.login.after(5000, show_error)

            self.login.after(500, switch_to_indeterminate)

        def show_error():
            connect_bar.stop()
            messagebox.showinfo("Error", "Please check your internet connection")
            connect_bar.destroy()
            self.login.title("No connection")

        def progress_start():
            global connect_bar, conn
            try:
                conn = mysql.connector.connect(host=DB_SERVER,
                                               database=DB,
                                               user=DB_USER,
                                               password=DB_PASS)

                if conn.is_connected():
                    start()
            except Error:
                not_start()

        progress_start()





login  = ctk.CTk()
login_user = login_user(login)
login.configure(fg_color="#e0dfdf")
login.resizable(False,False)
login.mainloop()


