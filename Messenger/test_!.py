import tkinter
import socket
import threading
from tkinter import messagebox
from tkinter import simpledialog, scrolledtext
from queue import Queue

class Yinra:
    def __init__(self, yinra_win):
        self.yinra_win = yinra_win
        self.initialize_window()

    def create_gui(self):
        self.yinra_win.title("Yinra")
        win_width = 760
        win_height = 550
        screen_width = self.yinra_win.winfo_screenwidth()
        screen_height = self.yinra_win.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        self.yinra_win.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.yinra_win.minsize(win_width, win_height)
        self.yinra_win.maxsize(win_width, win_height)

        self.inbox_label = tkinter.Label(master=self.yinra_win, text="Inbox", font=("Times", 25))
        self.inbox_label.pack(pady=8)
        self.inbox_label.configure(state='disabled')

        self.message_box = tkinter.scrolledtext.ScrolledText(master=self.yinra_win, width=150, height=50)
        self.message_box.pack(pady=10)
        self.message_box.configure(state='disabled')

        self.input_message = tkinter.Text(master=self.yinra_win,
                                          font=("Times", 16),
                                          width=600, height=40)
        self.input_message.pack(anchor='w', padx=10, pady=10)

        self.send_button = tkinter.Button(master=self.yinra_win, text="Send", command=self.write,
                                          font=("Times", 16), width=60, height=40)
        self.send_button.place(x=650, y=490)
        self.yinra_done = True
        self.yinra_win.protocol("WM_DELETE_WINDOW", self.stop)

def main():
    yinra_win = tkinter.Tk()
    yinra_window = Yinra(yinra_win)
    yinra_win.mainloop()


if __name__ == "__main__":
    main()

