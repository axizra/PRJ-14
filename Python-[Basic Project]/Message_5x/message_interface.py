import tkinter as tk


def create_window(title, message, command=None):
    window = tk.Toplevel()
    window.title(title)

    new_width = 530
    new_height = 400

    # Calculate the x and y coordinates for the window to be centered
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2

    window.geometry(f"{new_width}x{new_height}+{x}+{y}")
    window.minsize(new_width, new_height)
    window.maxsize(new_width, new_height)
    window.resizable(False, False)  # To disable window resizing

    # Use label with wraplength and anchor to center align the text
    message_label = tk.Label(window, text=message, font=("Times New Roman", 23, "bold"), wraplength=new_width - 40)
    message_label.pack(padx=20, pady=20, fill=tk.BOTH, expand=True, anchor='center')

    if command:
        next_btn = tk.Button(window, text="Next", command=command)
        next_btn.pack(pady=10)

    return window


# Messages
first_message = "Projects folder encompasses a basic Python project that employs the Tkinter model for creating a graphical user interface."
second_message = "Inside this directory, you'll find a Python project that utilizes the Tkinter library to construct a user interface, along with incorporating the concept of dictionaries for data management."
third_message = "The contents of this folder revolve around a fundamental Python project where Tkinter is harnessed to develop an interactive graphical interface, while also implementing dictionary concepts."
forth_message = "Additionally, some project makes use of the Pillow module for image processing and the ImageTk module for working with images in the Tkinter interface."


def close_open1():
    form_1.withdraw()
    form_2.deiconify()


def close_open2():
    form_2.withdraw()
    form_3.deiconify()


def close_open3():
    form_3.withdraw()
    form_4.deiconify()


# Create the main window
form_1 = tk.Tk()
form_1.title("Message")

new_width = 530
new_height = 400

# Calculate the x and y coordinates for the window to be centered
screen_width = form_1.winfo_screenwidth()
screen_height = form_1.winfo_screenheight()
x = (screen_width - new_width) // 2
y = (screen_height - new_height) // 2

form_1.geometry(f"{new_width}x{new_height}+{x}+{y}")
form_1.minsize(new_width, new_height)
form_1.maxsize(new_width, new_height)

first_mesg = tk.Label(form_1, text=first_message, font=("Times New Roman", 23, "bold"), wraplength=new_width - 40)
first_mesg.pack(padx=20, pady=20, fill=tk.BOTH, expand=True, anchor='center')

first_btn = tk.Button(form_1, text="Next", command=close_open1)
first_btn.pack(pady=10)

form_1.resizable(False, False)

# Create the subsequent windows as Toplevel windows
form_2 = create_window("Message 2", second_message, close_open2)
form_2.withdraw()

form_3 = create_window("Message 3", third_message, close_open3)
form_3.withdraw()

form_4 = create_window("Message 4", forth_message)
form_4.withdraw()

# Start the main event loop
form_1.mainloop()
