#import MainFunctions as mf
import tkinter as tk
import tkinter.font as tkFont
import socket
from tkinter import Menu
import threading
import time
import os
import read as RFID
import RPi.GPIO as GPIO
scaler = 480/800
screen_width = 715
screen_height = 450
titleHeight = 30
titleWidth = 34
returnCorrectionWidth3 = 70
returnCorrectionWidth2 = 45
returnCorrectionHeight = 15
timeLastPressed = 0
inNurseMenu = False
padding = 0
clientEnable = True
faste = False
acceptedCards =[184266225316,584161695581]
lastCardScanned = 0
lastUser = 0
currentMenu = "MainMenu"
currentMainMenu = "MainMenu"
user = ["Daniel","Eivind"]
requestsRoom = []
def SOSbuttonFunction():
    
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN)
        if GPIO.input(26) == GPIO.HIGH:
            sendRequest("SOS",2)
            print("SOS button pressed")
            SOSpopup()
            time.sleep(1)
        else:
            time.sleep(0.1)
def useData(data):
    global faste
    data = data.split(",")
    print(f"data is : {data}")
    indexlist = []
    
    if data[0] == "MatPopup":
        if data[1] == "Middag":
            if faste != True:
                showPopupFood(f"Dagens middag er:\n{data[2]}","#F0AB44","Middag")
            
        elif data[1] == "Lunsj":
            if faste != True:
                showPopupFood(f"Dagens lunsj er:\n{data[2]}","#73F7C6","Lunsj")
            
        elif data[1] == "Frokost":
            if faste != True:
                showPopupFood(f"Frokost","#73F7C6","Frokost")
        elif data[1] == "Kvelds":
            if faste != True:
                showPopupFood(f"Kveldsmat","#4E7869","Kvelds")
        elif int(data[1]) == rom:
            if data[2] == "AddFaste":
                faste = True
                print(f"Faste: {faste}")
                showPopup(f"Faste lagt til\nav sykepleier","#F55454")
                returnButton()
            elif data[2] == "RemoveFaste":
                faste = False
                print(f"Faste: {faste}")
                showPopup(f"Faste fjernet\nav sykepleier","#F55454")
                returnButton()
        else:
            print("Could not use data 1")
    if data[0]=="Remote Remove":
        try:
            requestsRoom.remove({"Rom": int(data[1]), "Seng": int(data[2]), "Hva": data[3], "Hastegrad": int(data[4])})
            showPopup(f"Fjernet forespørsel\n{data[3]} trådløst","#F55454")
            returnButton()
        except Exception as e:
            print(f"Could not remove: {e}")
    for index,i in enumerate(requestsRoom):
        #print(f"{data[0] == 'Remove'} {i.get('Rom') == int(data[1])} { i.get('Seng') == int(data[2])}")
        if data[0] == "Remove" and i.get('Rom') == int(data[1]) and i.get('Seng') == int(data[2]):
            #print(f"added {index} to indexlist")
            indexlist.append(index)
    for i in range(len(indexlist)-1,-1,-1):
        print(f"Removing:{requestsRoom.pop(indexlist[i])}")
    return

if clientEnable:
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(("38:d5:7a:7d:5d:2e", 4))
def isRequestInRoom(rom, seng, hva, hastegrad):
    request = {"Rom": rom, "Seng": seng, "Hva": hva, "Hastegrad": hastegrad}
    for req in requestsRoom:
        if req.get('Rom') == request.get('Rom') and req.get('Seng') == request.get('Seng') and req.get('Hva') == request.get('Hva') and req.get('Hastegrad') == request.get('Hastegrad'):
            return True
    return False
def getButtonString(hva,hastegrad):
    newHva = hva
    if hva == "Mye smerte" or hva == "Litt smerte":
                newHva = "Smerte"
    elif hva == "Haster" or hva == "Haster ikke":
            newHva = "Toalett"
    elif hva == "Trenger hjelp nå" or hva == "Trenger hjelp senere":
        newHva = "Hjelp"
    elif hva in ["Skive med\nost","Skive med\nskinke","Skive med\negg","Skive med\nsyltetøy","Skive med\nbrunost"]:
        matList1 = ["Skive med\nost","Skive med\nskinke","Skive med\negg","Skive med\nsyltetøy","Skive med\nbrunost"]
        matList2 = ["Skive m/ost","Skive m/skinke","Skive m/egg","Skive m/syltetøy","Skive m/brunost"]
        newHva = matList2[matList1.index(hva)]
    if isRequestInRoom(rom, seng, newHva, hastegrad):
        if hva == "Mye smerte" or hva == "Litt smerte" or hva == "Haster" or hva == "Haster ikke":
            if hva == "Mye smerte" or hva == "Litt smerte":
                hva = "Smerte"
            elif hva == "Haster" or hva == "Haster ikke":
                hva = "Toalett"
            return f"Fjern betjening\n{hva}"
        if hva == "Trenger hjelp nå" or hva == "Trenger hjelp senere":
            hva = "Hjelp"
            return f"Fjern\n{hva} ønske"
        else:
            return f"Fjern\n{hva} ønske"
    elif hva == "Mye smerte":
        return "Mye smerte"
    elif hva == "Litt smerte":
        return "Litt smerte"
    elif hva == "Haster":
        return "Haster"
    elif hva == "Haster ikke":
        return "Haster ikke"
    else:
        return hva

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
def showPopupFood(Text,Color="lightblue",Hva = "Mat"):
    top_frame = tk.Frame(root,bg=Color)
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    foodLabel = tk.Label(top_frame,
                        text=Text,
                        font=button_font,
                        bg=Color,
                        fg="#000000")
    foodLabel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)
    ynlabel = tk.Label(top_frame,
                        text="Ønsker du dette?",
                        font=button_font,
                        bg=Color,
                        fg="#000000")
    ynlabel.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.2)
    if Hva == "Frokost" or Hva =="Kvelds":
        yes = tk.Button(top_frame,
                        text = "Ja",
                        bg="#7BCAE4",
                        fg = "#000000",
                        font=button_font,
                        command=matBestilling)
        no = tk.Button(top_frame,
                        text = "Nei",
                        bg="#7BCAE4",
                        fg = "#000000",
                        font=button_font,
                        command=returnButton)
    else:
        yes = tk.Button(top_frame,
                        text = "Ja",
                        bg="#7BCAE4",
                        fg = "#000000",
                        font=button_font,
                        command=lambda: sendRequest(Hva,5))
        no = tk.Button(top_frame,
                        text = "Nei",
                        bg="#7BCAE4",
                        fg = "#000000",
                        font=button_font,
                        command=returnButton)
    yes.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
    no.place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.2)
    root.update()  # Update the root window to ensure label is drawn before the main loop continues
    #time.sleep(1)  # Wait for 1 seconds
def SOSpopup(Color ="#FF0000"):
    top_frame = tk.Frame(root,bg=Color)
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    SOSLabel = tk.Label(top_frame,
                        text="Du har trykket på\nSOS knappen!\n\nHvis du trykket feil, trykk AVBRYT",
                        font=button_font,
                        bg=Color,
                        fg="#000000")
    SOSLabel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.4)
    abortButton = tk.Button(top_frame,
                        text = "AVBRYT",
                        bg="#CA4747",
                        fg = "#000000",
                        font=button_font,
                        command=lambda: sendRequest("SOS",99))
    abortButton.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.2)

def getButtonSize(col, row, tiltle = False):
    if tiltle:
        return (int(screen_height/row)-padding*2-int(titleHeight/row),int(screen_width/col)+int(titleWidth/col)-padding*2)
    else:
        return (int(screen_height/row)-padding*2,int(screen_width/col)-padding*2)
def showSent():
    top_label = tk.Label(root,
                        text="Forespørsel sent",
                        font=button_font,
                        bg="lightblue",
                        fg="#000000")
    top_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)
    root.update()  # Update the root window to ensure label is drawn before the main loop continues
    time.sleep(1)  # Wait for 1 seconds
def showRemoved():
    top_label = tk.Label(root,
                        text="Forespørsel fjernet",
                        font=button_font,
                        bg="#FF5858",
                        fg="#000000")
    top_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)
    root.update()  # Update the root window to ensure label is drawn before the main loop continues
    time.sleep(1)  # Wait for 1 seconds
def showPopup(Text,Color="lightblue"):
    top_label = tk.Label(root,
                        text=Text,
                        font=button_font,
                        bg=Color,
                        fg="#000000")
    top_label.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)
    root.update()  # Update the root window to ensure label is drawn before the main loop continues
    time.sleep(1)  # Wait for 1 seconds
def sendRequest(request, hastegrad):
    remove = True
    if hastegrad == 2 and request == "SOS":
        remove = False
    elif request == "SOS":
        remove = True
        hastegrad = 2
    show = ""
    global root  # Assuming root is a global variable
    message = f"{rom},{seng},{request},{hastegrad},{user[lastUser]}"
    if hastegrad != 0:
        try:
            isEqual = False
            receivedData = message.split(",")
            receivedDict = {
                "Rom": int(receivedData[0]),
                "Seng": int(receivedData[1]),
                "Hva": receivedData[2],
                "Hastegrad": int(receivedData[3])
            }
            for i in requestsRoom:
                if (i.get('Rom') == receivedDict.get('Rom') and
                    i.get('Seng') == receivedDict.get('Seng') and
                    i.get('Hva') == receivedDict.get('Hva')):
                    if receivedDict.get('Hastegrad') < i.get('Hastegrad'):
                        print("Hastegrad endret")
                        remove = False
                        show = "sent"
                        i['Hastegrad'] = receivedDict.get('Hastegrad')
                        if clientEnable != True:
                            showSent()
                            returnButton()
                        
                    isEqual = True
            if not isEqual:
                requestsRoom.append(receivedDict)
                show = "sent"
                if clientEnable != True:
                    showSent()
                    returnButton() 
            elif remove:
                print(f"Removing request: {receivedDict}")
                requestsRoom.remove(receivedDict)
                message = f"{rom},{seng},{request},-1,{user[lastUser]}"
                show = "removed"
                if clientEnable != True:
                    showRemoved()
                    returnButton()
        except Exception as e:
            print(f"Data could not be used: {e}")
    else:
        useData(f"{request},{rom},{seng}")
        show = "removed"
    if clientEnable:
        sendData(message)
        if show == "sent" and request != "SOS":
            showSent()
            returnButton()
        elif show == "removed" and request != "SOS":
            showRemoved()
            returnButton()
        elif show == "removed":
            returnButton()
    print(f"Requests: {requestsRoom}")
def returnButton():
        print(f"CurrentMenu: {currentMenu}")
        print(f"CurrentMainMenu: {currentMainMenu}")
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
        elif currentMenu == "ChangeDifficulty" or currentMenu == "RomOrBed" or currentMenu == "AddOrRemoveCard":
            mainAdminMenu()
        elif currentMenu == "ChangeRoom"or currentMenu == "ChangeBed":
            mainAdminMenu()
        elif currentMenu == "EasyMenu":
            mainEasyMenu()
        elif currentMenu == "MediumMenu":
            mainMediumMenu()
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
                          command = returnButton,
                          height = btn_size[0]+int(returnCorrectionHeight/pos[0]),
                          width = btn_size[1]+int(returnCorrectionWidth/pos[1]))
    returnBtn.grid(row = pos[0], column = pos[1], padx=padding, pady=padding)
    return

def Smerte():
    global inNurseMenu
    inNurseMenu = False
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
                        text = getButtonString("Mye smerte",3),
                        bg="#F46A00",
                        fg = buttonTextColor,
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Smerte",3),
                        height= getButtonSize(2,2,True)[0],
                        width=  getButtonSize(2,2,True)[1])
    littSmerte = tk.Button(root,
                           text = getButtonString("Litt smerte",4),
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
    global inNurseMenu
    inNurseMenu = False
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
                    text = getButtonString("Juice",5),
                    bg = "#FFC75F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command= lambda: sendRequest("Juice",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Vann = tk.Button(root,
                    text = getButtonString("Vann",5),
                    bg = "#00E1FF",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Vann",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Saft = tk.Button(root,
                    text = getButtonString("Saft",5),
                    bg = "#F66F6F",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Saft",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Kaffe = tk.Button(root,
                    text = getButtonString("Kaffe",5),
                    bg = "#814B2E",
                    fg = buttonTextColor,
                    image=pixelVirtual,
                    compound="c",
                    font=button_font,
                    command = lambda: sendRequest("Kaffe",5),
                    height=getButtonSize(3, 2,True)[0],
                    width=getButtonSize(3, 2,True)[1])
    Te = tk.Button(root,
                    text = getButtonString("Te",5),
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
    global inNurseMenu
    inNurseMenu = False
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
                        text = getButtonString("Haster",4),
                        bg="#EAA940",
                        fg = buttonTextColor,
                        image=pixelVirtual,
                        compound="c",
                        font=button_font,
                        command=lambda: sendRequest("Toalett",4),
                        height= getButtonSize(2,2,True)[0],
                        width=  getButtonSize(2,2,True)[1])
    littSmerte = tk.Button(root,
                           text = getButtonString("Haster ikke",5),
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
    global inNurseMenu
    inNurseMenu = False
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
                text = getButtonString("Skive med\nost",5),
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/ost",5),
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    m2 = tk.Button(root,
                text = getButtonString("Skive med\nskinke",5),
                bg="#F8B422",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/skinke",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m3 = tk.Button(root,
                text = getButtonString("Skive med\negg",5),
                bg="#E2A156",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/egg",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m4 = tk.Button(root,
                text = getButtonString("Skive med\nsyltetøy",5),
                bg="#3A86F7",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/syltetøy",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m5 = tk.Button(root,
                text = getButtonString("Skive med\nbrunost",5),
                bg="#E8DC9D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/brunost",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    
    m1.grid(row = 1, column = 1, padx=padding, pady=padding)
    m2.grid(row = 1, column = 2, padx=padding, pady=padding)
    m3.grid(row = 1, column = 3, padx=padding, pady=padding)
    m4.grid(row = 2, column = 1, padx=padding, pady=padding)
    m5.grid(row = 2, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(3,2,True),(2,3))
    return
def AddOrRemoveMat(alternativ):
    global bestilling
    
    if alternativ in bestilling:
        bestilling.remove(alternativ)
    elif alternativ in ["Brødskive","Knekkebrød","Rundstykke"]:
        for i in bestilling:
            if i in ["Brødskive","Knekkebrød","Rundstykke"]:
                bestilling.remove(i)
        bestilling.append(alternativ)
    else:
        bestilling.append(alternativ)
    print(f"Bestilling: {bestilling}")
    matBestilling()

def getTextMat(alternativ):
    global bestilling
    if alternativ in bestilling:
        return f"Fjern {alternativ}"
    else:
        return f"{alternativ}"
bestillinger = []
bestilling = []
def sendTextMat():
    global bestillinger
    global bestilling
    bestillinger.append(bestilling)
    bestilling = []
    if bestillinger[-1] == []:
        bestillinger.pop(-1)
    print(f"Bestillinger: {bestillinger}")
    for i in bestillinger:
        print(f"Sender: {','.join(i)}")
        sendRequest('.'.join(i),5)
    bestillinger = []
    returnButton()
def newOrderFunction():
    global bestilling
    global bestillinger
    bestillinger.append(bestilling)
    bestilling = []
    matBestilling()
def removeOrderFunction(bestilling):
    global bestillinger
    bestillinger.remove(bestilling)
    matBestilling()
def matBestilling(textfont = ("Helvetica", 14)):
    global bestillinger
    global bestilling
    print(f"Bestillinger1: {bestillinger}")
    global inNurseMenu
    inNurseMenu = False
    for widget in root.winfo_children():
        widget.destroy()
    title = tk.Label(root,
                        text = "                              Matbestilling                    Trykk for å fjerne",
                        font=title_font,
                        bg=bacground_color,
                        fg="#ffffff")
    title.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    left_frame = tk.Frame(root,bg=bacground_color)
    left_frame.place(relx=0, rely=0.1, relwidth=0.333, relheight=0.9)
    middle_frame = tk.Frame(root,bg=bacground_color)
    middle_frame.place(relx=0.333, rely=0.1, relwidth=0.333, relheight=0.9)
    right_frame = tk.Frame(root,bg=bacground_color)
    right_frame.place(relx=0.666, rely=0.1, relwidth=0.333, relheight=0.9)
    bunnAlternativ = ["Brødskive","Knekkebrød","Rundstykke"]
    colorsBunn = ["#FF8D2F","#FAAC64","#FEBB7C"]
    for index,i in enumerate(bunnAlternativ):   
        bunn = tk.Button(left_frame,
                        text = getTextMat(i),
                        bg=colorsBunn[index],
                        fg = buttonTextColor,
                        font=button_font,
                        command= lambda i=i: AddOrRemoveMat(i))
        bunn.place(relx=0,rely=0+(1/len(bunnAlternativ))*index,relwidth=1,relheight=1/len(bunnAlternativ))
    paaleggAlternativ = ["Majones","Smør","Ost","Brunost","Skinke","Egg","Syltetøy"]
    colorsPaalegg = ["#F7E75C","#FFEDA6","#FFEA00","#C97633","#FF88B4","#FFFDDF","#FF2020"]
    for index,i in enumerate(paaleggAlternativ):
        paalegg = tk.Button(middle_frame,
                        text = getTextMat(i),
                        bg=colorsPaalegg[index],
                        fg = buttonTextColor,
                        font=button_font,
                        command= lambda i=i: AddOrRemoveMat(i))
        paalegg.place(relx=0,rely=0+(1/len(paaleggAlternativ))*index,relwidth=1,relheight=1/len(paaleggAlternativ))
    newOrder = tk.Button(right_frame,
                        text = "Legg til",
                        bg="#BABABA",
                        fg = buttonTextColor,
                        font=button_font,
                        command=lambda: newOrderFunction())
    newOrder.place(relx=0,rely=(1/7)*5,relwidth=1,relheight=1/7)
    sendOrder = tk.Button(right_frame,
                        text = "Send bestilling",
                        bg="#51FF44",
                        fg = buttonTextColor,
                        font=button_font,
                        command= sendTextMat)
    sendOrder.place(relx=0,rely=(1/7)*6,relwidth=1,relheight=1/7)
    if len(bestillinger) > 5:
        for index,i in enumerate(bestillinger):
            if len(i) <= 3:
                bestillingText = ",".join(i)
            elif len(i) <= 6:
                bestillingText = ",".join(i[:3])+"\n"+",".join(i[3:])
            else:
                bestillingText = ",".join(i[:3])+"\n"+",".join(i[3:6])+"\n"+",".join(i[6:])
            orders = tk.Button(right_frame,
                                text = bestillingText,
                                bg="#FFC75F",
                                fg="#000000",
                                border=1,
                                font=textfont,
                                command=lambda i = i: removeOrderFunction(i))
            orders.place(relx=0,rely=0+(((1/7)*5)/len(bestillinger))*index,relwidth=1,relheight=((1/7)*5)/len(bestillinger))
    else:
        for index,i in enumerate(bestillinger):
            if len(i) <= 3:
                bestillingText = ",".join(i)
            elif len(i) <= 6:
                bestillingText = ",".join(i[:3])+"\n"+",".join(i[3:])
            else:
                bestillingText = ",".join(i[:3])+"\n"+",".join(i[3:6])+"\n"+",".join(i[6:])
            orders = tk.Button(right_frame,
                                text = bestillingText,
                                bg="#FFC75F",
                                fg="#000000",
                                font=textfont,
                                command=lambda i = i: removeOrderFunction(i))
            orders.place(relx=0,rely=0+(0.7/5)*index,relwidth=1,relheight=0.7/5)
def matFrokostKvelds():
    global inNurseMenu
    inNurseMenu = False
    for widget in root.winfo_children():
        widget.destroy()
    title = tk.Label(root,
                     text = "Matbestilling",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    m1 = tk.Button(root,
                text = getButtonString("Skive med\nost",5),
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/ost",5),
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    m2 = tk.Button(root,
                text = getButtonString("Skive med\nskinke",5),
                bg="#F8B422",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/skinke",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m3 = tk.Button(root,
                text = getButtonString("Skive med\negg",5),
                bg="#E2A156",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/egg",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m4 = tk.Button(root,
                text = getButtonString("Skive med\nsyltetøy",5),
                bg="#3A86F7",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/syltetøy",5),
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    m5 = tk.Button(root,
                text = getButtonString("Skive med\nbrunost",5),
                bg="#E8DC9D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: sendRequest("Skive m/brunost",5),
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
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
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
def romOrBed():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "RomOrBed"
    rom = tk.Button(root,
                text = "Endre rom",
                bg="#7BCAE4",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeRoom,
                height= getButtonSize(2,2)[0],
                width=  getButtonSize(2,2)[1])
    bed = tk.Button(root,
                text = "Endre Seng",
                bg="#DE817D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeBed,
                height= getButtonSize(2,2)[0],
                width=  getButtonSize(2,2)[1])
    rom.grid(row = 1, column = 1, padx=padding, pady=padding)
    bed.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2),(2,2))
def changeBed():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "ChangeBed"
    title = tk.Label(root,
                     text = "Velg Seng:",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)

    bed1 = tk.Button(root,
                text = "Seng 1",
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setBed(1),
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    bed2 = tk.Button(root,
                text = "Seng 2",
                bg="#7A3B39",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=lambda: setBed(2),
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    bed1.grid(row = 1, column = 1, padx=padding, pady=padding)
    bed2.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
def addApprovedCard():
    global lastCardScanned
    lastCardScanned = 0
    append = True
    showPopup("Hold kortet mot leseren")
    start_time = time.time()

    while lastCardScanned == 0:
        if time.time() - start_time > 5:
            append = False
            break
        time.sleep(0.5)
    if append:       
        if lastCardScanned not in acceptedCards:
            inNurseMenu = True
            enterUsername()
        else:
            showPopup(f"ID kort allerede lagt til","#F3D739")
            returnButton()
    else:
        showPopup(f"Ingen kort scannet","#F3D739")
        returnButton()
userSaved = False
def saveUsername(username):
    global user
    global userSaved
    userSaved = True
    user.append(username)
    acceptedCards.append(lastCardScanned)
    showPopup(f"ID kort lagt til")
    returnButton()
    print(f"Cards: {acceptedCards}")
    print(f"Users: {user}")
def createButton(root,key,row,col,command,width =0.8/10):
    button = tk.Button(root,
                text = key,
                bg="#7BCAE4",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=command)
    xpos = 0.05 + (col)*(0.8/10)
    ypos = 0.5 + (row)*(0.8/5)
    height = 0.8/5
    button.place(relx=xpos, rely=ypos, relwidth=width, relheight=height)

currentName = ""
def buttonCommand(key,entry):
    global currentName
    print("Button pressed:", key)  # Add this line for debugging
    if key == "back":
        currentName = currentName[:-1]
    elif currentName == "":
        currentName += key
    else:
        currentName += key.lower()
    entry.delete(0, tk.END)  # Clear the current text in the entry widget
    entry.insert(0, currentName)  # Insert the updated current name
    root.update()
def enterUsername():
    global inNurseMenu
    global currentName
    global userSaved
    
    currentName = ""
    inNurseMenu = False
    userSaved = False
    
    top_frame = tk.Frame(root, bg="#71AFED")
    top_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    
    username_entry = tk.Entry(top_frame, font=("Helvetica", 20))
    username_entry.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.2)
    
    submit = tk.Button(top_frame, text="Lagre", font=("Helvetica", 20),
                       bg="#ffffff", fg="#000000",
                       command=lambda: saveUsername(username_entry.get()))
    submit.place(relx=0.825, rely=0.075, relwidth=0.15, relheight=0.15)
    
    row1 = ["Q","W","E","R","T","Y","U","I","O","P","Å"]
    for col, key in enumerate(row1):
        createButton(top_frame, key, 0, col, lambda k=key: buttonCommand(k,username_entry))

    row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ø", "Æ"]
    for col, key in enumerate(row2):
        createButton(top_frame, key, 1, col, lambda k=key: buttonCommand(k,username_entry))

    row31 = ["Z", "X", "C"]
    for col, key in enumerate(row31):
        createButton(top_frame, key, 2, col, lambda k=key: buttonCommand(k,username_entry))

    createButton(top_frame, " ", 2, 3, lambda k=" ": buttonCommand(k,username_entry), 0.8 / 10 * 4)

    row32 = ["V", "B", "N", "M"]
    for col, key in enumerate(row32, start=7):
        createButton(top_frame, key, 2, col, lambda k=key: buttonCommand(k,username_entry))
    
    #backspace
    button = tk.Button(top_frame, text="<--", bg="#7BCAE4", fg=buttonTextColor,
                       image=pixelVirtual, compound="c", font=button_font,
                       command=lambda: buttonCommand("back",username_entry))
    button.place(relx=0.05 + 8*(0.8/10), rely=0.5-0.8/5, relwidth=(0.8/10)*3, relheight=0.8/5)
    
    root.update()  # Update the root window to ensure label is drawn before the main loop continues
    submit.wait_variable(userSaved)
def removeApprovedCard():
    global lastCardScanned
    lastCardScanned = 0
    remove = True
    if len(acceptedCards) == 1:
        showPopup(f"Kan ikke fjerne siste kort","#D33D26")
        returnButton()
    else:
        showPopup("Hold kortet mot leseren")
        start_time = time.time()

        while lastCardScanned == 0:
            if time.time() - start_time > 5:
                remove = False
                break
            time.sleep(0.5)
        if remove:
            try:
                acceptedCards.remove(lastCardScanned)
                showPopup(f"ID kort fjernet","#EC5757")
                returnButton()
            except:
                showPopup(f"ID kort ikke funnet","#F3D739")
                returnButton()
        else:
            showPopup(f"Ingen kort scannet","#F3D739")
            returnButton()
def addOrRemoveCard():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    currentMenu = "AddOrRemoveCard"
    title = tk.Label(root,
                     text = "Legg til eller fjern kort",
                     font=title_font,
                     bg=bacground_color,
                     fg="#ffffff")
    title.grid(row=0, column = 1, columnspan=4)
    addCard = tk.Button(root,
                text = "Legg til kort",
                bg="#7BCAE4",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=addApprovedCard,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    removeCard = tk.Button(root,
                text = "Fjern kort",
                bg="#DE817D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=removeApprovedCard,
                height= getButtonSize(2,2,True)[0],
                width=  getButtonSize(2,2,True)[1])
    addCard.grid(row = 1, column = 1, padx=padding, pady=padding)
    removeCard.grid(row = 1, column = 2, padx=padding, pady=padding)
    createReturnBtn(getButtonSize(2,2,True),(2,2))
def quitFunc():
    root.quit()
def mainAdminMenu():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
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
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    changeBedButton = tk.Button(root,
                text = "Endre seng",
                bg="#DE817D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=changeBed,
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    addRemoveCard = tk.Button(root,
                text = "Legg til/\nfjern kort",
                bg="#DE817D",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=addOrRemoveCard,
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    changeDifficultyButton = tk.Button(root,
                text = "Endre\nvanskelighetsgrad",
                bg="#EAC471",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=("Helvetica", 23),
                command=changeDifficulty,
                height= getButtonSize(3,2,True)[0],
                width= getButtonSize(3,2,True)[1])
    closeProgram = tk.Button(root,
                text = "Lukk program",
                bg="#FF5733",
                fg = buttonTextColor,
                image=pixelVirtual,
                compound="c",
                font=button_font,
                command=quitFunc,
                height= getButtonSize(3,2,True)[0],
                width=  getButtonSize(3,2,True)[1])
    
    changeRoomButton.grid(row = 1, column = 1, padx=padding, pady=padding)
    changeBedButton.grid(row = 1, column = 2, padx=padding, pady=padding)
    addRemoveCard.grid(row = 1, column = 3, padx=padding, pady=padding)
    changeDifficultyButton.grid(row = 2, column = 1, padx=padding, pady=padding)
    closeProgram.grid(row = 2, column = 2, padx=padding, pady=padding)

    createReturnBtn(getButtonSize(3,2,True),(2,3))
    return
def changeDifficulty():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
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
"""def removeRequestNurse():
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
    return"""
def mainNurseMenu():
    global inNurseMenu
    inNurseMenu = True
    global timeLastPressed
    timeLastPressed = time.time()
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
                text = getButtonString("StansAlarm",1),
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
    global inNurseMenu
    inNurseMenu = False
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    global currentMainMenu
    currentMenu = "EasyMenu"
    currentMainMenu = "EasyMenu"
    btn1 = tk.Button(root,
                    text = getButtonString("Trenger hjelp nå",3),
                    bg = "#F16800",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    command=lambda: sendRequest("Hjelp",3),
                    font = button_font)
                    #height = getButtonSize(2,1)[0]+padding*2,
                    #width = getButtonSize(2,1,True)[1])
    btn2 = tk.Button(root,
                     text = getButtonString("Trenger hjelp senere",5),
                     bg = "#E0D025",
                     fg = buttonTextColor,
                     image=pixelVirtual,
                     compound="c",
                     command =lambda: sendRequest("Hjelp",5),
                     font = button_font)
                     #height = getButtonSize(2,1)[0]+padding*2,
                     #width = getButtonSize(2,1,True)[1])
    """btn6 = tk.Button(root,
                     text = "Sykepleiermeny",
                     bg = "#D87E7E",
                     fg = buttonTextColor,
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command = mainNurseMenu,
                     height = getButtonSize(2,1)[0],
                     width = getButtonSize(2,1,True)[1])"""
    btn1.place(relx=0,rely=0,relwidth=0.5,relheight=1)
    btn2.place(relx=0.5,rely=0,relwidth=0.5,relheight=1)
    #btn6.grid(row = 2, column = 2, padx=padding, pady=padding)
def mainMediumMenu():
    global inNurseMenu
    inNurseMenu = False
    for widget in root.winfo_children():
        widget.destroy()
    global currentMenu
    global currentMainMenu
    currentMenu = "MediumMenu"
    currentMainMenu = "MediumMenu"
    btn1 = tk.Button(root,
                    text = getButtonString("Trenger hjelp nå",3),
                    bg = "#F16800",
                    fg = buttonTextColor, 
                    image=pixelVirtual,
                    compound="c",
                    command=lambda: sendRequest("Hjelp",3),
                    font = button_font,
                    height = getButtonSize(2,2)[0],
                    width = getButtonSize(2,2,True)[1])
    btn2 = tk.Button(root,
                     text = getButtonString("Trenger hjelp senere",5),
                     bg = "#E0D025",
                     fg = buttonTextColor,
                     image=pixelVirtual,
                     compound="c",
                     command =lambda: sendRequest("Hjelp",5),
                     font = button_font,
                     height = getButtonSize(2,2)[0],
                     width = getButtonSize(2,2,True)[1])
    btn3 = tk.Button(root,
                        text = getButtonString("Drikke",5),
                        bg = "#40ADDC",
                        fg = buttonTextColor,
                        image=pixelVirtual ,
                        compound="c",
                        font=button_font,
                        command = lambda:sendRequest("Drikke",5),
                        height = getButtonSize(2,2)[0],
                        width = getButtonSize(2,2,True)[1])
    btn4 = tk.Button(root,
                        text = getButtonString("Mat",5),
                        bg = "#d87e7e",
                        fg = buttonTextColor,
                        image=pixelVirtual ,
                        compound="c",
                        font=button_font,
                        command = lambda:sendRequest("Mat",5),
                        height = getButtonSize(2,2)[0],
                        width = getButtonSize(2,2,True)[1])
    
    btn1.grid(row = 1, column = 1, padx=padding, pady=padding)
    btn2.grid(row = 1, column = 2, padx=padding, pady=padding)
    if faste != True:
        btn3.grid(row = 2, column = 1, padx=padding, pady=padding)
        btn4.grid(row = 2, column = 2, padx=padding, pady=padding)
def MainMenu():
    global inNurseMenu
    inNurseMenu = False
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
                   text = getButtonString("Betjening",4),
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
    """b6 = tk.Button(root,
                     text = getButtonString("SOS",2),
                     bg = "#FF0000",
                     fg = buttonTextColor,
                     image=pixelVirtual ,
                     compound="c",
                     font=button_font,
                     command =lambda: sendRequest("SOS",2),
                     height = button_height,
                     width = button_width)"""
    
    b1.grid(row = 1, column = 1, padx=padding, pady=padding)
    b3.grid(row = 1, column = 2, padx=padding, pady=padding)
    b4.grid(row = 1, column = 3, padx=padding, pady=padding)
    if faste != True:
        b2.grid(row = 2, column = 1, padx=padding, pady=padding)
        b5.grid(row = 2, column = 2, padx=padding, pady=padding)
    #b6.grid(row = 2, column = 3, padx=padding, pady=padding)
    
    # Create return btn
    #createReturnBtn()
    return



MainMenu()
def timeout():
    global timeLastPressed
    global currentMenu
    global inNurseMenu
    while True:
        if time.time() - timeLastPressed > 10 and inNurseMenu:
            currentMenu = "MainNurseMenu"
            print("Timeout Nurse Menu")
            returnButton()
        time.sleep(1)
def useRFID():
    global lastCardScanned
    global lastUser
    read = True
    start_time = time.time()
    card = 1
    while True:
        
        elapsed_time = time.time() - start_time
        if elapsed_time < 0.5:
            read = False
        else:
                read = True
        
        if read:
            card = RFID.getCardId()
            lastCardScanned = card
            start_time = time.time()
            print(f"Card read: {card}")
            if card in acceptedCards:
                lastUser = acceptedCards.index(lastCardScanned)
                print("card accepted")
                mainNurseMenu()
            else:
                print("Card denied")
    
RFIDthread = threading.Thread(target=useRFID)
RFIDthread.start()

timeoutThread = threading.Thread(target=timeout)
timeoutThread.start()

buttonThread = threading.Thread(target=SOSbuttonFunction)
buttonThread.start()
# Start the GUI
if clientEnable:
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

root.mainloop() 
if clientEnable:
    client.close()

