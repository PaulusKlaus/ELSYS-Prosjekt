#import MainFunctions as mf
import tkinter as tk
import tkinter.font as tkFont
import socket
from tkinter import Menu
scaler = 0.784
screen_width = int(1800 * scaler)
screen_height = int(1080 * scaler)
padding = 0

rom = 301
seng = 1
def setRoom(romNumber):
    global rom
    rom = romNumber
    root.title(f"Inlogget som rom {rom} seng {seng}")
    return
def setBed(sengNumber):
    global seng
    seng = sengNumber
    root.title(f"Inlogget som rom {rom} seng {seng}")
    return

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("38:d5:7a:7d:5d:2e", 4))
def sendData(data):
    try:
        client.send(data.encode('utf-8'))
    except OSError as e:
        print("Error sending data")
        pass
    return

root = tk.Tk() 
# root window title and dimension
root.title("Sengepost")
# Set geometry (widthxheight)
root.geometry(f'{screen_width}x{screen_height}')
bacground_color = "#2A324B"
title_font = ("Helvetica", 20)
button_font = ("Helvetica", 40)
buttonTextColor = "#000000"


setRoom(301)
setBed(1)

menubar = Menu(root)
romMenu = Menu(menubar, tearoff=0)
romMenu.add_command(label="301",command=lambda: setRoom(301))
romMenu.add_command(label="302",command=lambda: setRoom(302))
romMenu.add_command(label="303",command=lambda: setRoom(303))
romMenu.add_command(label="304",command=lambda: setRoom(304))
romMenu.add_command(label="305",command=lambda: setRoom(305))
romMenu.add_command(label="306",command=lambda: setRoom(306))
romMenu.add_command(label="307",command=lambda: setRoom(307))
romMenu.add_command(label="308",command=lambda: setRoom(308))
romMenu.add_command(label="309",command=lambda: setRoom(309))
romMenu.add_command(label="311",command=lambda: setRoom(311))
romMenu.add_command(label="313",command=lambda: setRoom(313))
romMenu.add_command(label="315",command=lambda: setRoom(315))

sengMenu = Menu(menubar, tearoff=1)
sengMenu.add_command(label="1",command=lambda: setBed(1))
sengMenu.add_command(label="2",command=lambda: setBed(2))

menubar.add_cascade(label="Romvalg",font=("Arial",18), menu=romMenu)
menubar.add_cascade(label="Sengevalg",font=("Arial",18), menu=sengMenu)
root.configure(menu=menubar,bg=bacground_color)




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

def sendRequest(request,hastegrad):
    message = f"{rom},{seng},{request},{hastegrad}"
    sendData(message)

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
                        bg="#F46A00",
                        fg = buttonTextColor,
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Smerte",2),
                        height= getButtonSize(2,2)[0],
                        width=  getButtonSize(2,2)[1])
    littSmerte = tk.Button(root,
                           text = "Litt smerte",
                           bg="#FFDD00",
                           fg = buttonTextColor,
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Smerte",3),
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
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command= lambda: sendRequest("Juice",4),
                    height=getButtonSize(3, 2)[0],
                    width=getButtonSize(3, 2)[1])
    Vann = tk.Button(root,
                    text = "Vann",
                    bg = "#00E1FF",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Vann",4),
                    height=getButtonSize(3, 2)[0],
                    width=getButtonSize(3, 2)[1])
    Saft = tk.Button(root,
                    text = "Saft",
                    bg = "#F66F6F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Saft",4),
                    height=getButtonSize(3, 2)[0],
                    width=getButtonSize(3, 2)[1])
    Kaffe = tk.Button(root,
                    text = "Kaffe",
                    bg = "#814B2E",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Kaffe",4),
                    height=getButtonSize(3, 2)[0],
                    width=getButtonSize(3, 2)[1])
    Te = tk.Button(root,
                    text = "Te",
                    bg = "#ED9F5F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Te",4),
                    height=getButtonSize(3, 2)[0],
                    width=getButtonSize(3, 2)[1])
    
    Juice.grid(row = 1, column = 1, padx=padding, pady=padding)
    Vann.grid(row = 1, column = 2, padx=padding, pady=padding)
    Saft.grid(row = 1, column = 3, padx=padding, pady=padding)
    Kaffe.grid(row = 2, column = 1, padx=padding, pady=padding)
    Te.grid(row = 2, column = 2, padx=padding, pady=padding)

    createReturnBtn(getButtonSize(3,2),(2,3))
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
                        bg="#EAA940",
                        fg = buttonTextColor,
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Toalett",3),
                        height= getButtonSize(2,2)[0],
                        width=  getButtonSize(2,2)[1])
    littSmerte = tk.Button(root,
                           text = "Haster litt",
                           bg="#D5CF5C",
                           fg = buttonTextColor,
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Toalett",4),
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
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Hamburger",4),
                height= getButtonSize(3,2)[0],
                width=  getButtonSize(3,2)[1])
    m2 = tk.Button(root,
                text = "Pizza",
                bg="#F8B422",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pizza",4),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m3 = tk.Button(root,
                text = "Kylling",
                bg="#E2A156",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Kylling",4),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m4 = tk.Button(root,
                text = "Fisk",
                bg="#3A86F7",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Fisk",4),
                height= getButtonSize(3,2)[0],
                width= getButtonSize(3,2)[1])
    m5 = tk.Button(root,
                text = "Pasta",
                bg="#E8DC9D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pasta",4),
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
                    bg = "#CD6A1F",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    command= Smerte,
                    font = button_font,
                    height = button_height,
                    width = button_width)
    b2 = tk.Button(root,
                   text = "Drikke",
                   bg = "#669BBC",
                   fg = buttonTextColor,
                   image=pixelVirtual,
                   compound="c",
                   command = Drikke,
                   font = button_font,
                   height = button_height,
                   width = button_width)
    b3 = tk.Button(root,
                   text = "Toalett",
                   bg = "#BEBEBE",
                   fg = buttonTextColor,
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = toalett,
                   height = button_height,
                   width = button_width)
    b4 = tk.Button(root,
                   text = "Betjening",
                   bg = "#A7C88A",
                   fg = buttonTextColor,
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = lambda: sendRequest("Betjening",3),
                   height = button_height,
                   width = button_width) 
    b5 = tk.Button(root,
                   text = "Mat",
                   bg = "#EABD79",
                   fg = buttonTextColor,
                   image=pixelVirtual ,
                   compound="c",
                   font=button_font,
                   command = mat,
                   height = button_height,
                   width = button_width)
    b6 = tk.Button(root,
                     text = "ALARM",
                     bg = "#FF0000",
                     fg = buttonTextColor,
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command = lambda: sendRequest("ALARM",1),
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
client.close()