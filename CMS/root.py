import tkinter as tk
import customtkinter as ctk



class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Yinra - Management System")

        win_width = 950
        win_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.root.minsize(win_width, win_height)
        self.root.maxsize(win_width, win_height)

        header = ctk.CTkFrame(master=self.root, height=50, width=win_width)
        header.place(x=0)


        def sidebar_event():
            def collapse_sidebar():
                sidebar.destroy()
                sidebar_btn.configure(text="≡")
                sidebar_btn.configure(command=sidebar_event)
            sidebar = ctk.CTkFrame(master=self.root,
                                   height=win_width, width=250)
            sidebar.place(x=0, y=51)
            sidebar_btn.configure(command=collapse_sidebar)


        sidebar_btn = ctk.CTkButton(master=self.root, text="≡",command=sidebar_event,
                                    width=100)
        sidebar_btn.configure(text="X")
        sidebar_btn.place(x=25, y=10)





root = ctk.CTk()
app = App(root)
root.resizable(False, False)
root.mainloop()

