import customtkinter as ctk



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