import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

ctk.set_appearance_mode("System")


DB_SERVER = "localhost"
DB_USER = "root"
DB_PASS = "crest008"
DB = "Credentials"


class login_user():
    def __init__(self, login):
        self.login = login
        self.login.title("Login")



        win_width = 860
        win_height = 482
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.login.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.login.minsize(win_width, win_height)
        self.login.maxsize(win_width, win_height)



        fname_label = ctk.CTkLabel(master=self.login, text="Name: ",font=('Times',20))
        fname = ctk.CTkEntry(master=self.login, width=212, height=30,font=('Times',16),
                             corner_radius=20)

        fname_label.place(x=45, y=35)
        fname.place(x=140, y=35)

        surname_label = ctk.CTkLabel(master=self.login, text="Surname: ",font=('Times',20))
        surname = ctk.CTkEntry(master=self.login, width=212, height=30,font=('Times',16), corner_radius=20)

        surname_label.place(x=45, y=90)
        surname.place(x=140, y=90)

        gender_label = ctk.CTkLabel(master=self.login, text="Gender: ",font=('Times',20))
        gender = ctk.CTkSegmentedButton(master=self.login, values=["Male", "Female", "Other"],
                                        width=200, height=30, corner_radius=20,font=('Times',15))
        gender.set("Nothing")

        gender_label.place(x=45, y=145)
        gender.place(x=140, y=145)

        address_label = ctk.CTkLabel(master=self.login, text="Address: ",font=('Times',20))
        address = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16))

        address_label.place(x=45, y=195)
        address.place(x=140, y=195)



        email_label = ctk.CTkLabel(master=self.login, text="E-mail: ",font=('Times',20))
        email = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16))
        email_label.place(x=45, y=245)
        email.place(x=140, y=245)


        contact_label = ctk.CTkLabel(master=self.login, text="Phone: ",font=('Times',20))
        contact = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16))
        contact_label.place(x=45,y=295)
        contact.place(x=140, y=295)



        confirm_btn = ctk.CTkButton(master=self.login, text="Confirm",font=('Times',18), corner_radius=20)
        confirm_btn.place(x=130, y=355)

        gif_area = ctk.CTkFrame(master=self.login, height=win_height, width=320)
        gif_area.place(x=400)

        gif_path = "drifter.gif"
        gif_image = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]

        gif_label = ctk.CTkLabel(master=self.login, image=gif_frames[0], text="")
        gif_label.place(x=400)

        def update_gif_frame(frame_index):
            gif_label.configure(image=gif_frames[frame_index])
            self.login.after(100, update_gif_frame, (frame_index + 1) % len(gif_frames))

        update_gif_frame(1)


login  = ctk.CTk()
login_user = login_user(login)
login.resizable(False,False)
login.mainloop()


