# Python tkinter hello world program 

import tkinter as tk
import tkinter.font as tkFont
scaler = 0.784
screen_width = int(1920 * scaler)
screen_height = int(1080 * scaler)
padding = 10


root = tk.Tk() 
# root window title and dimension
root.title("Sengepost")
# Set geometry (widthxheight)
root.geometry(f'{screen_width}x{screen_height}')
root.configure(bg='#2A324B')




#add image file
pixelVirtual = tk.PhotoImage(width=1, height=1)
returnIm = tk.PhotoImage(file = r"images/return.png")
# Changes the size of the image
returnIm = returnIm.subsample(2, 2)

def MainMenu():
    for widget in root.winfo_children():
        widget.destroy()
    # Create three big buttons
    b1 = tk.Button(root, text = "Button 1", bg = "#F3A712", fg = "white", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/3)-padding*2)
    b2 = tk.Button(root, text = "Vann", bg = "#669BBC",fg = "white", image=pixelVirtual ,compound="c", command = Vann, height = 200, width = int(screen_width/3)-padding*2)
    b3 = tk.Button(root, text = "Button 3", bg = "blue", fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3)-padding*2) 
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b2.grid(row = 1, column = 2, padx=padding, pady=padding)
    b3.grid(row = 1, column = 3, padx=padding, pady=padding)
    
    
    # Create return btn
    createReturnBtn()
    return
def createReturnBtn():
    returnBtn = tk.Button(root, bg = "white", fg = "#A8C686", image=returnIm ,compound="c", command = MainMenu, width = int(screen_width/3))
    # Setting the position of the button on the bottom of the screen.
    returnBtn.place(x = screen_width- int(screen_width/3), y = screen_height-270)
    
    return
def Vann():
    
    for widget in root.winfo_children():
        widget.destroy()
    # Create a title over grid
    title = tk.Label(root, text="Vann", font=("Helvetica", 16))
    # Center title
    title.grid(row = 0, column = 1, columnspan = 4)
    # Create two buttons
    vannHøy = tk.Button(root, text = "Stor hastegrad", bg = "red", fg = "white", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/2))
    vannLav = tk.Button(root, text = "Liten hastegrad", bg = "green",fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/2))
    vannHøy.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    vannLav.grid(row = 1, column = 3,columnspan=2, padx=padding, pady=padding)
    createReturnBtn()
# Position buttons with grid layout
    return

# Create three big buttons 
MainMenu()

# Start the GUI


root.mainloop() 
