#import MainFunctions as mf
import tkinter as tk
import tkinter.font as tkFont
import socket
from tkinter import Menu
import threading
scaler = 480/800
screen_width = 715
screen_height = 450
titleHeight = 30
titleWidth = 34
returnCorrectionWidth3 = 70
returnCorrectionWidth2 = 45
returnCorrectionHeight = 15
padding = 0
clientEnable = False
currentMenu = "MainMenu"
currentMainMenu = "MainMenu"
user = "Daniel"
requestsRoom = []
def ChangeUser(new_user):
    global user
    user = new_user
    print("User changed to: " + user)
    return

def useData(data):
    data = data.split(",")
    print(data)
    indexlist = []
    for index,i in enumerate(requestsRoom):
        print(f"{data[0] == 'Remove'} {i.get('Rom') == int(data[1])} { i.get('Seng') == int(data[2])}")
        if data[0] == "Remove" and i.get('Rom') == int(data[1]) and i.get('Seng') == int(data[2]):
            print(f"added {index} to indexlist")
            indexlist.append(index)
    for i in range(len(indexlist)-1,-1,-1):
        print(f"Removing:{requestsRoom.pop(indexlist[i])}")
    return

if clientEnable:
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(("38:d5:7a:7d:5d:2e", 4))

def receive_data():
    while True:
        try:
            data = client.recv(1024)
            data = data.decode('utf-8')
            useData(data)
        except OSError as e:
            pass
    return
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
#root.geometry(f'{screen_width}x{screen_height}')
root.attributes('-fullscreen',True)
bacground_color = "#2A324B"
title_font = ("Helvetica", 20)
button_font = ("Helvetica", 25)
buttonTextColor = "#000000"

root.configure(bg=bacground_color)

rom = 301
seng = 1

def setRoom(romNumber):
    global rom
    rom = romNumber
    root.title(f"Inlogget som rom {rom} seng {seng}")
    mainAdminMenu()
    return
def setBed(sengNumber):
    global seng
    seng = sengNumber
    root.title(f"Inlogget som rom {rom} seng {seng}")
    mainAdminMenu()
    return


#add image file
pixelVirtual = tk.PhotoImage(width=1, height=1)
returnIm = tk.PhotoImage(file = r"images/return.png")
# Changes the size of the image
returnIm = returnIm.subsample(2, 2)
button_height = int(screen_height/2)-padding*4
button_width = int(screen_width/3)-padding*4

print(f"Button height: {button_height}, Button width: {button_width}")

def getButtonSize(col, row, tiltle = False):
    if tiltle:
        return (int(screen_height/row)-padding*2-int(titleHeight/row),int(screen_width/col)+int(titleWidth/col)-padding*2)
    else:
        return (int(screen_height/row)-padding*2,int(screen_width/col)-padding*2)

def sendRequest(request,hastegrad):
    message = f"{rom},{seng},{request},{hastegrad},{user}"
    if hastegrad != 0:
        try:
            isEqual = False
            recievedData = message.split(",")
            recivedDict ={"Rom":int(recievedData[0]),
                            "Seng":int(recievedData[1]),
                            "Hva":recievedData[2],
                            "Hastegrad":int(recievedData[3])}
                            
            for i in requestsRoom:
                if i.get('Rom')== recivedDict.get('Rom') and i.get('Seng')== recivedDict.get('Seng') and i.get('Hva')== recivedDict.get('Hva'):
                    if recivedDict.get('Hastegrad') < i.get('Hastegrad'):
                        print("Hastegrad endret")
                        retrurnButton()
                        i['Hastegrad'] = recivedDict.get('Hastegrad')
                    isEqual = True
                    
            if not isEqual:
                requestsRoom.append(recivedDict)
                retrurnButton()
            else:
                print("Request already in list")
        except:
            print("Data could not be used")
            pass
    else:
        print(f"{request},{rom},{seng}")
        useData(f"{request},{rom},{seng}")
    if clientEnable:
        sendData(message)
    print(requestsRoom)
def retrurnButton():
    if currentMenu == "MainMenu":
        MainMenu()
        print("Something went wrong")
    elif currentMenu == "Smerte" or currentMenu == "Drikke" or currentMenu == "Toalett" or currentMenu == "Mat":
        MainMenu()
    elif currentMenu == "MainNurseMenu":
        if currentMainMenu == "EasyMenu":
            mainEasyMenu()
        elif currentMainMenu == "MediumMenu":
            mainMediumMenu()
        elif currentMainMenu == "MainMenu":
            MainMenu()
        else:
            print("Something went wrong")
        
    elif currentMenu == "MainAdminMenu":
        mainNurseMenu()
    elif currentMenu == "ChangeRoom"or currentMenu == "ChangeBed" or currentMenu == "ChangeDifficulty":
        mainAdminMenu()
    else:
        print("Something went wrong")

def createReturnBtn(btn_size = (button_height,button_width),pos = (2,3)):
    if pos[1] == 3:
        returnCorrectionWidth = returnCorrectionWidth3
    if pos[1] == 2:
        returnCorrectionWidth = returnCorrectionWidth2
    returnBtn = tk.Button(root,
                          bg = "#ffffff",
                          fg = "#A8C686",
                          image=returnIm ,
                          compound="c",
                          command = retrurnButton,
                          height = btn_size[0]+int(returnCorrectionHeight/pos[0]),
                          width = btn_size[1]+int(returnCorrectionWidth/pos[1]))
    returnBtn.grid(row = pos[0], column = pos[1], padx=padding, pady=padding)
    return

def Smerte():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "Smerte"
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
                        command=lambda: sendRequest("Smerte",3),
                        height= getButtonSize(2,2,True)[0],
                        width=  getButtonSize(2,2,True)[1])
    littSmerte = tk.Button(root,
                           text = "Litt smerte",
                           bg="#FFDD00",
                           fg = buttonTextColor,
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Smerte",4),
                           height= getButtonSize(2,2,True)[0],
                           width= getButtonSize(2,2,True)[1])
    myeSmerte.grid(row = 1, column = 1, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
    return

def Drikke():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "Drikke"
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
                    command= lambda: sendRequest("Juice",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Vann = tk.Button(root,
                    text = "Vann",
                    bg = "#00E1FF",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Vann",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Saft = tk.Button(root,
                    text = "Saft",
                    bg = "#F66F6F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Saft",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Kaffe = tk.Button(root,
                    text = "Kaffe",
                    bg = "#814B2E",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Kaffe",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Te = tk.Button(root,
                    text = "Te",
                    bg = "#ED9F5F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Te",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    
    Juice.grid(row = 1, column = 1, padx=padding, pady=padding)
    Vann.grid(row = 1, column = 2, padx=padding, pady=padding)
    Saft.grid(row = 1, column = 3, padx=padding, pady=padding)
    Kaffe.grid(row = 2, column = 1, padx=padding, pady=padding)
    Te.grid(row = 2, column = 2, padx=padding, pady=padding)

    createReturnBtn(getButtonSize(3,2,True),(2,3))
def toalett():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "Toalett"
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
                        command=lambda: sendRequest("Toalett",4),
                        height= getButtonSize(2,2,True)[0],
                        width=  getButtonSize(2,2,True)[1])
    littSmerte = tk.Button(root,
                           text = "Haster litt",
                           bg="#D5CF5C",
                           fg = buttonTextColor,
                           image=pixelVirtual,
                           compound="c",
                           font=button_font,
                           command=lambda: sendRequest("Toalett",5),
                           height= getButtonSize(2,2,True)[0],
                           width= getButtonSize(2,2,True)[1])
    myeSmerte.grid(row = 1, column = 1, padx=padding, pady=padding)
    littSmerte.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
    return
def mat():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "Mat"
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
                command=lambda: sendRequest("Hamburger",5),
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    m2 = tk.Button(root,
                text = "Pizza",
                bg="#F8B422",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pizza",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m3 = tk.Button(root,
                text = "Kylling",
                bg="#E2A156",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Kylling",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m4 = tk.Button(root,
                text = "Fisk",
                bg="#3A86F7",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Fisk",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m5 = tk.Button(root,
                text = "Pasta",
                bg="#E8DC9D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Pasta",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    
    m1.grid(row = 1, column = 1, padx=padding, pady=padding)
    m2.grid(row = 1, column = 2, padx=padding, pady=padding)
    m3.grid(row = 1, column = 3, padx=padding, pady=padding)
    m4.grid(row = 2, column = 1, padx=padding, pady=padding)
    m5.grid(row = 2, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(3,2,True),(2,3))
    return
def changeRoom():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "ChangeRoom"
    r301 = tk.Button(root,
                text = "Rom 301",
                bg="#FF5733",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(301),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r302 = tk.Button(root,
                text = "Rom 302",
                bg="#FFC300",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(302),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r303 = tk.Button(root,
                text = "Rom 303",
                bg="#DAF7A6",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(303),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r304 = tk.Button(root,
                text = "Rom 304",
                bg="#900C3F",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(304),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r305 = tk.Button(root,
                text = "Rom 305",
                bg="#581845",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(305),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r306 = tk.Button(root,
                text = "Rom 306",
                bg="#C70039",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(306),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r307 = tk.Button(root,
                text = "Rom 307",
                bg="#FF5733",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(307),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r308 = tk.Button(root,
                text = "Rom 308",
                bg="#FFBD33",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(308),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r309 = tk.Button(root,
                text = "Rom 309",
                bg="#DAF754",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(309),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r311 = tk.Button(root,
                text = "Rom 311",
                bg="#900C3E",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(311),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r313 = tk.Button(root,
                text = "Rom 313",
                bg="#581845",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(313),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r315 = tk.Button(root,
                text = "Rom 315",
                bg="#C70039",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setRoom(315),
                height= getButtonSize(4,3)[0],
                width=  getButtonSize(4,3)[1])
    r301.grid(row = 1, column = 1, padx=padding, pady=padding)
    r302.grid(row = 1, column = 2, padx=padding, pady=padding)
    r303.grid(row = 1, column = 3, padx=padding, pady=padding)
    r304.grid(row = 1, column = 4, padx=padding, pady=padding)
    r305.grid(row = 2, column = 1, padx=padding, pady=padding)
    r306.grid(row = 2, column = 2, padx=padding, pady=padding)
    r307.grid(row = 2, column = 3, padx=padding, pady=padding)
    r308.grid(row = 2, column = 4, padx=padding, pady=padding)
    r309.grid(row = 3, column = 1, padx=padding, pady=padding)
    r311.grid(row = 3, column = 2, padx=padding, pady=padding)
    r313.grid(row = 3, column = 3, padx=padding, pady=padding)
    r315.grid(row = 3, column = 4, padx=padding, pady=padding)
    
def changeBed():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "ChangeBed"
    bed1 = tk.Button(root,
                text = "Seng 1",
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setBed(1),
                height= getButtonSize(2,2)[0],
                width=  getButtonSize(2,2)[1])
    bed2 = tk.Button(root,
                text = "Seng 2",
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setBed(2),
                height= getButtonSize(2,2)[0],
                width=  getButtonSize(2,2)[1])
    bed1.grid(row = 1, column = 1, padx=padding, pady=padding)
    bed2.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2),(2,2))
    

def mainAdminMenu():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "MainAdminMenu"
    title = tk.Label(root,
                     text = "Sykepleiermeny",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    changeRoomButton = tk.Button(root,
                text = "Endre rom",
                bg="#7BCAE4",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeRoom,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    changeBedButton = tk.Button(root,
                text = "Endre Seng",
                bg="#DE817D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeBed,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    changeDifficultyButton = tk.Button(root,
                text = "Endre Vanskelighetsgrad",
                bg="#EAC471",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeDifficulty,
                height= getButtonSize(2,2,True)[0],
                width= getButtonSize(2,2,True)[1])
    
    changeRoomButton.grid(row = 1, column = 1, padx=padding, pady=padding)
    changeBedButton.grid(row = 1, column = 2, padx=padding, pady=padding)
    changeDifficultyButton.grid(row = 2, column = 1, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
    return
def changeDifficulty():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "ChangeDifficulty"
    title = tk.Label(root,
                     text = "Endre vanskelighetsgrad",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    easy = tk.Button(root,
                text = "Enkel",
                bg="#69D351",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=mainEasyMenu,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    medium = tk.Button(root,
                text = "Middels",
                bg="#D2C530",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=mainMediumMenu,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    hard = tk.Button(root,
                text = "Vanskelig",
                bg="#DE4C47",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=MainMenu,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    easy.grid(row = 1, column = 1, padx=padding, pady=padding)
    medium.grid(row = 1, column = 2, padx=padding, pady=padding)
    hard.grid(row = 2, column = 1, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
    return
def removeRequestNurse():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "RemoveRequestNurse"
    title = tk.Label(root,
                     text = "Fjern forespørsler",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)
    buttonList = []
    if len(requestsRoom) == 0:
        print("No requests")
        col = 1
        row = 1
    if len(requestsRoom) <= 3:
        col = 2
        row = 2
    elif len(requestsRoom) <= 5:
        col = 2
        rom = 3
    elif len(requestsRoom) <= 7:
        col = 2
        row = 4
    elif len(requestsRoom) <= 8:
        col = 3
        row = 3
    elif len(requestsRoom) <= 9:
        col = 2
        row = 5
    elif len(requestsRoom) <= 11:
        col = 3
        row = 4
    else:

        print("Too many requests")

    for index, i in enumerate(requestsRoom):
        buttonList.append(tk.Button(root,
                text = f"Fjern {i.get('Hva')}",
                bg="#F38581",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest(requestsRoom[index].get('Hva'),0),
                height= getButtonSize(row,col)[0],
                width=  getButtonSize(row,col)[1]))
    
    colIndex = 1
    rowIndex = 1
    for i in buttonList:
        i.grid(row = colIndex, column = rowIndex, padx=padding, pady=padding)
        if rowIndex == row:
            rowIndex = 0
            colIndex += 1
        rowIndex += 1
    createReturnBtn(getButtonSize(row,col),(col,row))
    return
def mainNurseMenu():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "MainNurseMenu"
    title = tk.Label(root,
                     text = "Sykepleiermeny",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    editRequestRoom = tk.Button(root,
                text = "Fjern forespørsler",
                bg="#F38581",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Remove",0),
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    otherRoom = tk.Button(root,
                text = "Annet",
                bg="#52A4F1",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=mainAdminMenu,
                height= getButtonSize(2,2,True)[0],
                width= getButtonSize(2,2,True)[1])
    stansAlarm = tk.Button(root,
                text = "Stans alarm",
                bg="#FF0000",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("StansAlarm",1),
                height= getButtonSize(2,2,True)[0],
                width= getButtonSize(2,2,True)[1])
    
    
    editRequestRoom.grid(row = 1, column = 1, padx=padding, pady=padding)
    otherRoom.grid(row = 1, column = 2, padx=padding, pady=padding)
    stansAlarm.grid(row = 2, column = 1, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
    return

def mainEasyMenu():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    global currentMainMenu
    currentMenu = "EasyMenu"
    currentMainMenu = "EasyMenu"
    btn1 = tk.Button(root,
                    text = "Trenger hjelp nå!",
                    bg = "#F16800",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    command=lambda: sendRequest("Hjelp",3),
                    font = button_font,
                    height = getButtonSize(2,2)[0],
                    width = getButtonSize(2,2,True)[1])
    btn2 = tk.Button(root,
                     text = "Trenger hjelp senere",
                     bg = "#E0D025",
                     fg = buttonTextColor,
                     image=pixelVirtual,
                     compound="c",
                     command =lambda: sendRequest("Hjelp",5),
                     font = button_font,
                     height = getButtonSize(2,2)[0],
                     width = getButtonSize(2,2,True)[1])
    btn6 = tk.Button(root,
                     text = "Sykepleiermeny",
                     bg = "#D87E7E",
                     fg = buttonTextColor,
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command = mainNurseMenu,
                     height = getButtonSize(2,2)[0],
                     width = getButtonSize(2,2,True)[1])
    btn1.grid(row = 1, column = 1, padx=padding, pady=padding)
    btn2.grid(row = 1, column = 2, padx=padding, pady=padding)
    btn6.grid(row = 2, column = 2, padx=padding, pady=padding)
def mainMediumMenu():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    global currentMainMenu
    currentMenu = "MediumMenu"
    currentMainMenu = "MediumMenu"
    btn1 = tk.Button(root,
                    text = "Trenger hjelp nå!",
                    bg = "#F16800",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    command=lambda: sendRequest("Hjelp",3),
                    font = button_font,
                    height = getButtonSize(2,2)[0],
                    width = getButtonSize(2,2,True)[1])
    btn2 = tk.Button(root,
                     text = "Trenger hjelp senere",
                     bg = "#E0D025",
                     fg = buttonTextColor,
                     image=pixelVirtual,
                     compound="c",
                     command =lambda: sendRequest("Hjelp",5),
                     font = button_font,
                     height = getButtonSize(2,2)[0],
                     width = getButtonSize(2,2,True)[1])
    btn3 = tk.Button(root,
                        text = "Drikke",
                        bg = "#40ADDC",
                        fg = buttonTextColor,
                        image=pixelVirtual ,
                        compound="c",
                        font=button_font,
                        command = lambda:sendRequest("Drikke",5),
                        height = getButtonSize(2,2)[0],
                        width = getButtonSize(2,2,True)[1])
    btn4 = tk.Button(root,
                        text = "Sykepleiermeny",
                        bg = "#d87e7e",
                        fg = buttonTextColor,
                        image=pixelVirtual ,
                        compound="c",
                        font=button_font,
                        command = mainNurseMenu,
                        height = getButtonSize(2,2)[0],
                        width = getButtonSize(2,2,True)[1])
    btn1.grid(row = 1, column = 1, padx=padding, pady=padding)
    btn2.grid(row = 1, column = 2, padx=padding, pady=padding)
    btn3.grid(row = 2, column = 1, padx=padding, pady=padding)
    btn4.grid(row = 2, column = 2, padx=padding, pady=padding)

def MainMenu():
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    global currentMainMenu
    currentMenu = "MainMenu"
    currentMainMenu = "MainMenu"
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
                   command = lambda: sendRequest("Betjening",4),
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
                     text = "Sykepleiermeny",
                     bg = "#D87E7E",
                     fg = buttonTextColor,
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command = mainNurseMenu,
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
if clientEnable:
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

root.mainloop() 
if clientEnable:
    client.close()
