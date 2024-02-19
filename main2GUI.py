# Python tkinter hello world program 

import tkinter as tk
import tkinter.font as tkFont
scaler = 0.784
screen_width = int(1800 * scaler)
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
    b1 = tk.Button(root, text = "Smerte", bg = "coral", fg = "white", image=pixelVirtual ,compound="c", command= Smerte, height = 200, width = int(screen_width/3)-padding*2)
    b2 = tk.Button(root, text = "Drikke", bg = "lightskyblue",fg = "white", image=pixelVirtual ,compound="c", command = Drikke, height = 200, width = int(screen_width/3)-padding*2)
    b3 = tk.Button(root, text = "Toalett", bg = "mediumpurple", fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Hello World"), height = 200, width = int(screen_width/3)-padding*2) 
    b4 = tk.Button(root, text = "Betjening", bg= "hotpink", fg = "white", image = pixelVirtual, compound= "c", command= lambda: print("Betjening kommer"), height= 200, width = int(screen_width/3) - padding*2)
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b2.grid(row = 1, column = 2, padx=padding, pady=padding)
    b3.grid(row = 1, column = 3, padx=padding, pady=padding)
    b4.grid(row = 2, column = 1, padx=padding, pady=padding)
    
    
    # Create return btn
    createReturnBtn()
    return
def createReturnBtn():
    returnBtn = tk.Button(root, bg = "white", fg = "#A8C686", image=returnIm ,compound="c", command = MainMenu, width = int(screen_width/3))
    # Setting the position of the button on the bottom of the screen.
    returnBtn.place(x = screen_width- int(screen_width/3), y = screen_height-270)
    return

def Drikke():
    for widget in root.winfo_children():
        widget.destroy()
    # Create a title over grid
    title = tk.Label(root, text="Drikke", font=("Helvetica", 16))
    # Center title
    title.grid(row = 0, column = 1, columnspan = 4)
    # Create two buttons
    Juice = tk.Button(root, text = "Juice", bg = "orange", fg = "white", image=pixelVirtual ,compound="c", command= lambda: print("Juice er på vei"), height = 200, width = int(screen_width/2))
    Vann = tk.Button(root, text = "Vann", bg = "green",fg = "white", image=pixelVirtual ,compound="c", command = lambda: print("Vann er på vei"), height = 200, width = int(screen_width/2))
    Juice.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    Vann.grid(row = 1, column = 3,columnspan=2, padx=padding, pady=padding)
    createReturnBtn()
# Position buttons with grid layout
    return

def Betjening():
    for widget in root.winfo_children():
        widget.destroy()
    #create title above grid
    title = tk.Label(root, text="Betjening", font=("Arial", 16))
    #center title
    title.grid(row=0, column = 1, columnspan = 4)

    createReturnBtn()
    return

def Smerte():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text = "Smerte", font=("Arial", 16))
    title.grid(row=0, column = 1, columnspan=4)
    myeSmerte = tk.Button(root, text = "Mye smerte", bg="SlateBlue2", fg = "white", image=pixelVirtual, compound="c", command=lambda: print("Mye smerte registrert"), height= 200, width= int(screen_width/2))
    littSmerte = tk.Button(root, text = "Litt smerte", bg="aquamarine", fg = "white", image=pixelVirtual, compound="c", command=lambda: print("Litt smerte registrert"), height= 200, width= int(screen_width/2))
    myeSmerte.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 3,columnspan= 2, padx=padding, pady=padding)
    createReturnBtn()
    return
# Create three big buttons 
MainMenu()

# Start the GUI


root.mainloop() 
