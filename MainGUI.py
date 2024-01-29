# Python tkinter hello world program 

import tkinter as tk
import tkinter.font as tkFont

screen_width = 1500
screen_height = 800


root = tk.Tk() 
# root window title and dimension
root.title("Sengepost")
# Set geometry (widthxheight)
root.geometry(f'{screen_width+86}x{screen_height}')
pixelVirtual = tk.PhotoImage(width=1, height=1)
def MainMenu():
    b1.config(text="Button 1")
    b2.config(text="Button 2")
    return
def MenuItem1():
    b1.config(text="Hello World")
    b2.config(text="Hello World")
    return

# Create three big buttons 
b1 = tk.Button(root, text = "Button 1", bg = "red", fg = "white", image=pixelVirtual ,compound="c", command = MenuItem1, height = 200, width = int(screen_width/3))
b2 = tk.Button(root, text = "Button 2", bg = "green",fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3))
b3 = tk.Button(root, text = "Button 3", bg = "blue", fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3))
# Position buttons with grid layout
b1.grid(row = 0, column = 1)
b2.grid(row = 0, column = 2)
b3.grid(row = 0, column = 3)
# Create return btn
returnBtn = tk.Button(root, text = "Return", bg = "white", fg = "black", image=pixelVirtual ,compound="c", command = MainMenu, height = 200, width = int(screen_width/3))
returnBtn.grid(row = 3, column = 3)

# Start the GUI


root.mainloop() 
