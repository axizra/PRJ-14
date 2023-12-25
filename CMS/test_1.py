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



        win_width = 590
        win_height = 240
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.login.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.login.minsize(win_width, win_height)
        self.login.maxsize(win_width, win_height)


        gif_path = "hi.gif"  # Replace with the path to your animated GIF file
        gif_image = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]

        gif_label = ctk.CTkLabel(master=self.login, image=gif_frames[0], text="")
        gif_label.place(x=350)

        def update_gif_frame(frame_index):
            gif_label.configure(image=gif_frames[frame_index])
            self.login.after(100, update_gif_frame, (frame_index + 1) % len(gif_frames))

        # Start the update loop to display the frames
        update_gif_frame(1)



        fname_label = ctk.CTkLabel(master=self.login, text="Full Name: ",font=('Times',20), text_color="#ad2f5d")
        fname = ctk.CTkEntry(master=self.login, width=212, height=30,font=('Times',16),
                             corner_radius=20, fg_color="#979593", border_color="#ad2f5d", text_color="white" )

        fname_label.place(x=35, y=30)
        fname.place(x=140, y=30)


        address_label = ctk.CTkLabel(master=self.login, text="Address: ",font=('Times',20), text_color="#ad2f5d")
        address = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16),
                              fg_color = "#979593", border_color = "#ad2f5d", text_color="white" )

        address_label.place(x=35, y=80)
        address.place(x=140, y=80)

        email_label = ctk.CTkLabel(master=self.login, text="E-mail: ",font=('Times',20), text_color="#ad2f5d")
        email = ctk.CTkEntry(master=self.login, width=212, height=30, corner_radius=20,font=('Times',16),
                             fg_color="#979593", border_color="#ad2f5d", text_color="white"   )

        email_label.place(x=35, y=130)
        email.place(x=140, y=130)


        confirm_btn = ctk.CTkButton(master=self.login, text="Confirm",font=('Times',19),height=32,
                                    corner_radius=22, text_color="white",
                                    fg_color="#a02956", hover_color="#a98a94")
        confirm_btn.place(x=140, y=185)











login  = ctk.CTk()
login_user = login_user(login)
login.configure(fg_color="#e0dfdf")
login.resizable(False,False)
login.mainloop()


