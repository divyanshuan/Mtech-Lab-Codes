import tkinter as tk
from tkinter import PhotoImage, messagebox

font_tuple = ("Times New Roman", 20, "bold")


def on_button_click():
    user_input = input_box.get()
    messagebox.showinfo(
        "Welcome", f"Hello, {user_input}!\nWelcome to the GUI Application."
    )


mainWindow = tk.Tk()
mainWindow.title("GUI Application")
mainWindow.geometry("600x400")

mainFrame = tk.Frame(mainWindow, bg="lightblue")
mainFrame.grid(sticky="nsew")

tk.Label(
    mainFrame,
    text="GUI Application for Computational Lab I",
    font=font_tuple,
    bg="lightblue",
).grid(column=0, row=0, padx=10, pady=10)
tk.Label(
    mainFrame, text="By Divyanshu Verma (24MCS022)", font=font_tuple, bg="lightblue"
).grid(column=0, row=1, padx=10, pady=10)

img = PhotoImage(file="boy_studing.png")
picture_frame = tk.Label(mainFrame, image=img, bg="lightblue")
picture_frame.grid(row=2, column=0, padx=10, pady=10)

input_box = tk.Entry(mainFrame, width=30)
input_box.grid(row=3, column=0, padx=10, pady=10)

action_button = tk.Button(
    mainFrame, text="Submit", font=("Arial", 16), command=on_button_click
)
action_button.grid(row=4, column=0, padx=10, pady=10)
mainWindow.grid_columnconfigure(0, weight=1)
mainWindow.grid_rowconfigure(0, weight=1)
mainWindow.grid_rowconfigure(2, weight=1)


mainWindow.mainloop()
