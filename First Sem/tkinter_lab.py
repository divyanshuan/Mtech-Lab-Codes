import tkinter as tk
from tkinter import *
from tkinter import PhotoImage

font_tuple = ("Times New Roman", 20, "bold")
mainWindow = Tk()
mainWindow.title("GUI Application")
mainFrame = tk.Frame(mainWindow)
mainFrame.configure()
mainFrame.grid()
Label(mainFrame, text="GUI Application for Computational Lab I", font=font_tuple).grid(
    column=0, row=0
)
Label(mainFrame, text="This lab is done by Divyanshu Verma", font=font_tuple).grid(
    column=0, row=1
)
img = PhotoImage(file="boy.png")
picture_frame = tk.Label(mainFrame, image=img)
picture_frame.grid(row=2, column=0)
mainWindow.mainloop()
