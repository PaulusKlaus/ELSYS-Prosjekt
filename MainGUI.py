# Python tkinter hello world program 

import tkinter as tk
import tkinter.font as tkFont

screen_width = 1500
screen_height = 800
padding = 10


root = tk.Tk() 
# root window title and dimension
root.title("Sengepost")
# Set geometry (widthxheight)
root.geometry(f'{screen_width+110}x{screen_height}')

#add image file
pixelVirtual = tk.PhotoImage(width=1, height=1)
returnIm = tk.PhotoImage(file = r"images/return.png")
# Changes the size of the image
returnIm = returnIm.subsample(2, 2)

def MainMenu():
    for widget in root.winfo_children():
        widget.destroy()
    b1 = tk.Button(root, text = "Button 1", bg = "red", fg = "white", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/3))
    b2 = tk.Button(root, text = "Vann", bg = "blue",fg = "white", image=pixelVirtual ,compound="c", command = Vann, height = 200, width = int(screen_width/3))
    b3 = tk.Button(root, text = "Button 3", bg = "blue", fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3)) 
    return
def createReturnBtn():
    returnBtn = tk.Button(root, bg = "white", fg = "black", image=returnIm ,compound="c", command = MainMenu, width = int(screen_width/3))
    returnBtn.grid(row = 3, column = 3, padx=padding, pady=padding)
    return
def Vann():
    for widget in root.winfo_children():
        widget.destroy()
    vannHøy = tk.Button(root, text = "Stor hastegrad", bg = "red", fg = "white", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/3))
    vannLav = tk.Button(root, text = "Liten hastegrad", bg = "green",fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3))
    vannHøy.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    vannLav.grid(row = 1, column = 3,columnspan=2, padx=padding, pady=padding)
    createReturnBtn()
# Position buttons with grid layout
    return

# Create three big buttons 
b1 = tk.Button(root, text = "Button 1", bg = "red", fg = "white", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/3))
b2 = tk.Button(root, text = "Vann", bg = "blue",fg = "white", image=pixelVirtual ,compound="c", command = Vann, height = 200, width = int(screen_width/3))
b3 = tk.Button(root, text = "Button 3", bg = "blue", fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3))
# Position buttons with grid layout
title = tk.Label(root, text = "Sengepost", font = ("Helvetica", 50))
title.grid(row = 0, column = 0, columnspan = 4)
b1.grid(row = 1, column = 1, padx=padding, pady=padding)
b2.grid(row = 1, column = 2, padx=padding, pady=padding)
b3.grid(row = 1, column = 3, padx=padding, pady=padding)
# Create return btn
returnBtn = tk.Button(root, bg = "white", fg = "black", image=returnIm ,compound="c", command = MainMenu, width = int(screen_width/3))
returnBtn.grid(row = 3, column = 3, padx=padding, pady=padding)

# Start the GUI


root.mainloop() 
