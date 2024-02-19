# Python tkinter hello world program 
import MainFunctions as mf
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
button_height = int(screen_height/2)-padding*2
button_width = int(screen_width/3)-padding*2
def MainMenu():
    for widget in root.winfo_children():
        widget.destroy()
    # Create three big buttons
    
    b1 = tk.Button(root,
                    text = "Smerte",
                    bg = "#F3A712",
                    fg = "#FFFFFF", 
                    image=pixelVirtual,
                    compound="c",
                    height = button_height,
                    width = button_width)
    b2 = tk.Button(root,
                   text = "Drikke",
                   bg = "#669BBC",
                   fg = "#FFFFFF",
                   image=pixelVirtual,
                   compound="c",
                   command = Vann,
                   height = button_height,
                   width = button_width)
    b3 = tk.Button(root,
                   text = "Toalett",
                   bg = "#8BF2E3",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = lambda: print("Hello World"),
                   height = button_height,
                   width = button_width)
    b4 = tk.Button(root,
                   text = "Betjening",
                   bg = "#9AF1B0",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = lambda: print("Hello World"),
                   height = button_height,
                   width = button_width) 
    b5 = tk.Button(root,
                   text = "Mat",
                   bg = "blue",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = lambda: print("Hello World"),
                   height = button_height,
                   width = button_width) 
    
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b2.grid(row = 1, column = 2, padx=padding, pady=padding)
    b3.grid(row = 1, column = 3, padx=padding, pady=padding)
    b4.grid(row = 2, column = 1, padx=padding, pady=padding)
    b5.grid(row = 2, column = 2, padx=padding, pady=padding)
    
    
    # Create return btn
    mf.createReturnBtn(root,returnIm,MainMenu,button_width,button_height,padding)
    return

def Vann():
    
    for widget in root.winfo_children():
        widget.destroy()
    # Create a title over grid
    title = tk.Label(root, text="Vann", font=("Helvetica", 16))
    # Center title
    title.grid(row = 0, column = 1, columnspan = 4)
    # Create two buttons
    vannHøy = tk.Button(root, text = "Stor hastegrad", bg = "red", fg = "#FFFFFF", image=pixelVirtual ,compound="c", height = 200, width = int(screen_width/2))
    vannLav = tk.Button(root, text = "Liten hastegrad", bg = "green",fg = "#FFFFFF", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/2))
    vannHøy.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    vannLav.grid(row = 1, column = 3,columnspan=2, padx=padding, pady=padding)
    mf.createReturnBtn(root,returnIm,MainMenu,button_width,button_height,padding)
# Position buttons with grid layout
    return

# Create three big buttons 
MainMenu()

# Start the GUI


root.mainloop() 
