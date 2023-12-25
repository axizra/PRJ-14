import tkinter
import socket
from tkinter import messagebox
from tkinter import simpledialog, scrolledtext

host = '192.168.0.100'
port = 8888


class YinraClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        login_win = tkinter.Tk()
        login_win.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=login_win)

        self.yinra_done = False
        self.running = True

        self.yinra_win = tkinter.Tk()
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

        self.message_box = tkinter.scrolledtext.ScrolledText(master=self.yinra_win, width=150, height=25)
        self.message_box.pack(pady=5)
        self.message_box.configure(state='disabled')

        self.input_message = tkinter.Text(master=self.yinra_win, font=("Times", 16), width=80, height=2)
        self.input_message.pack(anchor='w', padx=10, pady=10)

        self.send_button = tkinter.Button(master=self.yinra_win, text="Send", command=self.write, font=("Times", 18))
        self.send_button.place(x=665, y=410)
        self.yinra_done = True
        self.yinra_win.protocol("WM_DELETE_WINDOW", self.stop)

        # Schedule the initial call to check for new messages
        self.check_for_messages()

        # Run the Tkinter main loop
        self.yinra_win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_message.get('1.0', 'end')}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_message.delete('1.0', 'end')

    def check_for_messages(self):
        try:
            message = self.sock.recv(1024)
            print("Received message:", message)
            if message == b'NICK':
                self.sock.send(self.nickname.encode('utf-8'))
            else:
                if self.yinra_done:
                    print("Updating GUI")
                    self.update_gui(message.decode('utf-8'))
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            print("Connection reset by server")
            messagebox.showinfo("Connection Error", "The connection was reset by the server.")
            self.sock.close()
            self.stop()

        # Schedule the next call to check for new messages
        if self.running:
            self.yinra_win.after(100, self.check_for_messages)

    def update_gui(self, message):
        self.message_box.configure(state='normal')
        self.message_box.insert('end', message)
        self.message_box.yview('end')
        self.message_box.configure(state='disabled')

    def stop(self):
        self.running = False
        self.sock.close()
        exit(0)


client = YinraClient(host, port)
