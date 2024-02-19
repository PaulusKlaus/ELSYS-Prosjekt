import datetime as dt
import tkinter as tk

def createReturnBtn(root,image,command,button_width,button_height,padding):
    returnBtn = tk.Button(root,
                          bg = "#ffffff",
                          fg = "#A8C686",
                          image=image ,
                          compound="c",
                          command = command,
                          height = button_height,
                          width = button_width)
    # Setting the position of the button on the bottom of the screen.
    #returnBtn.place(x = screen_width- int(screen_width/3), y = screen_height-270)
    returnBtn.grid(row = 2, column = 3, padx=padding, pady=padding)
    return
