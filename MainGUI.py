#import MainFunctions as mf
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
bacground_color = "#2A324B"
title_font = ("Helvetica", 20)
button_font = ("Helvetica", 15)
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

def Smerte():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root,
                     text = "Smerte",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    
    title.grid(row=0, column = 1, columnspan=4)

    myeSmerte = tk.Button(root,
                        text = "Mye smerte",
                        bg="#123456",
                        fg = "#ffffff",
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Mye smerte"),
                        height= getButtonSize(2,2)[0],
                        width=  getButtonSize(2,2)[1])
    littSmerte = tk.Button(root,
                           text = "Litt smerte",
                           bg="#046FDB",
                           fg = "#ffffff",
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Litt smerte"),
                           height= getButtonSize(2,2)[0],
                           width= getButtonSize(2,2)[1])
    myeSmerte.grid(row = 1, column = 1, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2),(2,2))
    return

def Drikke():
    for widget in root.winfo_children():
        widget.destroy()
    # Create a title over grid
    title = tk.Label(root,
                     text="Drikke",
                     font= title_font,
                     bg = bacground_color,
                     fg="#ffffff")
    # Center title
    title.grid(row = 0, column = 1, columnspan = 4)
    # Create two buttons
    Juice = tk.Button(root,
                    text = "Juice",
                    bg = "#FFC75F",
                    fg = "#ffffff",
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command= lambda: sendRequest("Juice"),
                    height=getButtonSize(2, 2)[0],
                    width=getButtonSize(2, 2)[1])
    Vann = tk.Button(root,
                    text = "Vann",
                    bg = "#008000",
                    fg = "#ffffff", 
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Vann"),
                    height=getButtonSize(2, 2)[0],
                    width=getButtonSize(2, 2)[1])
    Melk = tk.Button(root,
                    text = "Melk",
                    bg = "#123456",
                    fg = "#ffffff",
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Melk"),
                    height=getButtonSize(2, 2)[0],
                    width=getButtonSize(2, 2)[1])
    
    Juice.grid(row = 1, column = 1, padx=padding, pady=padding)
    Vann.grid(row = 1, column = 2, padx=padding, pady=padding)
    Melk.grid(row = 2, column = 1, padx=padding, pady=padding)

    createReturnBtn(getButtonSize(2,2),(2,2))
def toalett():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root,
                     text = "Toalett",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    myeSmerte = tk.Button(root,
                        text = "Haster veldig",
                        bg="#123456",
                        fg = "#ffffff",
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Toalett veldig hast"),
                        height= getButtonSize(2,2)[0],
                        width=  getButtonSize(2,2)[1])
    littSmerte = tk.Button(root,
                           text = "Haster litt",
                           bg="#046FDB",
                           fg = "#ffffff",
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Toalett litt hast"),
                           height= getButtonSize(2,2)[0],
                           width= getButtonSize(2,2)[1])
    myeSmerte.grid(row = 1, column = 1, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2),(2,2))
    return
def mat():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root,
                     text = "Matbestilling",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    m1 = tk.Button(root,
                text = "Hamburger",
                bg="#123456",
                fg = "#ffffff",
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Hamburger"),
                height= getButtonSize(3,2)[0],
                width=  getButtonSize(3,2)[1])
    m2 = tk.Button(root,
                text = "Pizza",
                bg="#046FDB",
                fg = "#ffffff",
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pizza"),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m3 = tk.Button(root,
                text = "Kylling",
                bg="#046FDB",
                fg = "#ffffff",
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Kylling"),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m4 = tk.Button(root,
                text = "Fisk",
                bg="#046FDB",
                fg = "#ffffff",
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Fisk"),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m5 = tk.Button(root,
                text = "Pasta",
                bg="#046FDB",
                fg = "#ffffff",
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pasta"),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    
    m1.grid(row = 1, column = 1, padx=padding, pady=padding)
    m2.grid(row = 1, column = 2, padx=padding, pady=padding)
    m3.grid(row = 1, column = 3, padx=padding, pady=padding)
    m4.grid(row = 2, column = 1, padx=padding, pady=padding)
    m5.grid(row = 2, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(3,2),(2,3))
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
                    font=button_font,
                    command= Smerte,
                    font = ("Arial", 30),
                    height = button_height,
                    width = button_width)
    b2 = tk.Button(root,
                   text = "Drikke",
                   bg = "#669BBC",
                   fg = "#FFFFFF",
                   image=pixelVirtual,
                   compound="c",
                   font=button_font,
                   command = Drikke,
                   font = ("Arial", 30),
                   height = button_height,
                   width = button_width)
    b3 = tk.Button(root,
                   text = "Toalett",
                   bg = "#8BF2E3",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = toalett,
                   height = button_height,
                   width = button_width)
    b4 = tk.Button(root,
                   text = "Betjening",
                   bg = "#9AF1B0",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = lambda: sendRequest("Betjening"),
                   height = button_height,
                   width = button_width) 
    b5 = tk.Button(root,
                   text = "Mat",
                   bg = "#123456",
                   fg = "#FFFFFF",
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = mat,
                   height = button_height,
                   width = button_width)
    b6 = tk.Button(root,
                     text = "BT5",
                     bg = "#75A6CE",
                     fg = "#FFFFFF",
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command = lambda: print("Bt5 pressed"),
                     height = button_height,
                     width = button_width) 
    
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b2.grid(row = 1, column = 2, padx=padding, pady=padding)
    b3.grid(row = 1, column = 3, padx=padding, pady=padding)
    b4.grid(row = 2, column = 1, padx=padding, pady=padding)
    b5.grid(row = 2, column = 2, padx=padding, pady=padding)
    b6.grid(row = 2, column = 3, padx=padding, pady=padding)
    
    # Create return btn
    #createReturnBtn()
    return



MainMenu()

# Start the GUI


root.mainloop() 
