import tkinter
import tkinter as tk
import socket
import threading
from tkinter import messagebox
from tkinter import simpledialog, scrolledtext

host = '127.0.0.1'
port = 8888


class Yinra_client:
    def __init__(self, host, port):
        self.yinra_win = None
        self.send_button = None
        self.input_message = None
        self.message_box = None
        self.inbox_label = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        login_win = tk.Tk()
        login_win.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=login_win)
        self.yinra_done = False
        self.running = True

        yinra_thread = threading.Thread(target=self.yinra_loop)
        receive_thread = threading.Thread(target=self.receive)

        yinra_thread.start()
        receive_thread.start()

    def yinra_loop(self):
        self.yinra_win = tk.Tk()
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

        self.message_box = tkinter.scrolledtext.ScrolledText(master=self.yinra_win, width=700, height=400)
        self.message_box.pack(pady=10)
        self.message_box.configure(state='disabled')

        self.input_message = tkinter.Text(master=self.yinra_win,
                                          font=("Times", 16),
                                          width=600, height=40)
        self.input_message.pack(anchor='w', padx=35, pady=10)

        self.send_button = tk.Button(master=self.yinra_win, text="Send", command=self.write,
                                     font=("Times", 16), width=60, height=40)
        self.send_button.place(x=650, y=490)
        self.yinra_done = True
        self.yinra_win.protocol("WM_DELETE_WINDOW", self.stop)
        self.yinra_win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_message.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_message.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.yinra_win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == b'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.yinra_win:
                        self.message_box.configure(state='normal')
                        self.message_box.insert('end', message.decode('utf-8'))
                        self.message_box.yview('end')
                        self.message_box.configure(state='disabled')
            except ConnectionAbortedError:
                break
            except ConnectionResetError:
                messagebox.showinfo("Connection Error", "The connection was reset by the server.")
                self.stop()


client = Yinra_client(host, port)
