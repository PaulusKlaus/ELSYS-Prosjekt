#import MainFunctions as mf
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
bacground_color = "#2A324B"
title_font = tkFont.Font("Helvetica", 20)
root.configure(bg=bacground_color)




#add image file
pixelVirtual = tk.PhotoImage(width=1, height=1)
returnIm = tk.PhotoImage(file = r"images/return.png")
# Changes the size of the image
returnIm = returnIm.subsample(2, 2)
button_height = int(screen_height/2)-padding*2
button_width = int(screen_width/3)-padding*2
print(f"Button height: {button_height}, Button width: {button_width}")
def getButtonSize(col, row):
    return (int(screen_height/row)-padding*2,int(screen_width/col)-padding*2)
def sendRequest(request):
    print(request)
    return

def createReturnBtn(btn_size = (button_height,button_width),pos = (2,3)):
    returnBtn = tk.Button(root,
                          bg = "#ffffff",
                          fg = "#A8C686",
                          image=returnIm ,
                          compound="c",
                          command = MainMenu,
                          height = btn_size[0],
                          width = btn_size[1])
    returnBtn.grid(row = pos[0], column = pos[1], padx=padding, pady=padding)
    return

def MainMenu():
    for widget in root.winfo_children():
        widget.destroy()
    
    b1 = tk.Button(root,
                    text = "Smerte",
                    bg = "#F3A712",
                    fg = "#FFFFFF", 
                    image=pixelVirtual,
                    compound="c",
                    command= Smerte,
                    height = button_height,
                    width = button_width)
    b2 = tk.Button(root,
                   text = "Drikke",
                   bg = "#669BBC",
                   fg = "#FFFFFF",
                   image=pixelVirtual,
                   compound="c",
                   command = Drikke,
                   height = button_height,
                   width = button_width)
    b3 = tk.Button(root,
                   text = "Toalett",
                   bg = "#8BF2E3",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = sendRequest("Toalett"),
                   height = button_height,
                   width = button_width)
    b4 = tk.Button(root,
                   text = "Betjening",
                   bg = "#9AF1B0",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = Betjening,
                   height = button_height,
                   width = button_width) 
    b5 = tk.Button(root,
                   text = "Mat",
                   bg = "blue",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   command = lambda: print("Bt5 pressed"),
                   height = button_height,
                   width = button_width) 
    
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b2.grid(row = 1, column = 2, padx=padding, pady=padding)
    b3.grid(row = 1, column = 3, padx=padding, pady=padding)
    b4.grid(row = 2, column = 1, padx=padding, pady=padding)
    b5.grid(row = 2, column = 2, padx=padding, pady=padding)
    
    
    # Create return btn
    createReturnBtn()
    return

def Drikke():
    for widget in root.winfo_children():
        widget.destroy()
    # Create a title over grid
    title = tk.Label(root,
                     text="Drikke",
                     font=title_font,bg = bacground_color,fg="#ffffff")
    # Center title
    title.grid(row = 0, column = 1, columnspan = 4)
    # Create two buttons
    Juice = tk.Button(root,
                    text = "Juice",
                    bg = "#FFA500",
                    fg = "#ffffff",
                    image=pixelVirtual,
                    compound="c",
                    command= lambda: sendRequest("Juice"),
                    height=getButtonSize(2, 2)[0],
                    width=getButtonSize(2, 2)[1])
    Vann = tk.Button(root, text = "Vann",
                    bg = "#008000",
                    fg = "#ffffff", 
                    image=pixelVirtual,
                    compound="c",
                    command = lambda: sendRequest("Vann"),
                    height=getButtonSize(2, 2)[0],
                    width=getButtonSize(2, 2)[1])
    print(f"Button height: {getButtonSize(2, 2)[0]}, Button width: {getButtonSize(2, 2)[1]}")
    Juice.grid(row = 1, column = 1, padx=padding, pady=padding)
    Vann.grid(row = 1, column = 2, padx=padding, pady=padding)

    createReturnBtn(getButtonSize(2,2),(2,2))

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

    myeSmerte = tk.Button(root,
                        text = "Mye smerte",
                        bg="SlateBlue2",
                        fg = "white",
                        image=pixelVirtual,
                        compound="c",
                        command=lambda: print("Mye smerte registrert"),
                        height= 200,
                        width= int(screen_width/2))
    littSmerte = tk.Button(root,
                           text = "Litt smerte",
                           bg="aquamarine",
                           fg = "white",
                           image=pixelVirtual,
                           compound="c",
                           command=lambda: print("Litt smerte registrert"),
                           height= 200,
                           width= int(screen_width/2))
    myeSmerte.grid(row = 1, column = 1,columnspan= 2, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 3,columnspan= 2, padx=padding, pady=padding)
    createReturnBtn()
    return
MainMenu()

# Start the GUI


root.mainloop() 
