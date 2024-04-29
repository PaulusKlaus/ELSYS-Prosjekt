import tkinter as tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
import time as t
import StyreenhetFunctions as cf
from tkinter import Menu
import socket
import threading

#Defined colors and functions
clientEnabled = True
romMerkingPadx = 20
romMerkingPady = 2
romMerkingFont = ("Impact",80)
max_width = 1800 #Defines the maximum width of the window
max_height = int((max_width/16)*9) #calculates the height of the window relation 16:9
pageTitle = "Romoversikt" #Defines the title of the window
button_texts = ["Fjern", "↑ (Hastegrad)", "↓ (Hastegrad)", "Feil!"]
windowBackgroundColor = "#bfd1e0"
menuButtonColor = ["#B0B0B0","#B0B0B0","#B0B0B0","#B0B0B0"]
buttonColor = "#437EB8"
currentUser = "Default User"
lowest_hastegrad_requests = []

# Sends data to the "Styreenhet"
def sendData(data):
    try:
        client.send(data.encode('utf-8')) 
    except OSError as e:
        print("Error sending data")
        pass
    return

# Sends a help request to the "Styreenhet"
def sendRequestBT(request,function):
    message = f"{function},{request.get('Rom')},{request.get('Seng')},{request.get('Hva')},{request.get('Hastegrad'),}"
    if clientEnabled:  
        sendData(message)
def useData(recievedData):
    try:
        isEqual = False
        update = True
        recievedData = recievedData.split(",")
        print(f"recieved Data:{recievedData}")
        recivedDict ={"Rom":int(recievedData[0]),
                            "Seng":int(recievedData[1]),
                            "Hva":recievedData[2],
                            "Hastegrad":int(recievedData[3]),
                            "Tid":cf.getCurrentTime(),
                            "Occupied":cf.is_room_occupied(requests,int(recievedData[0])),
                            "ID": 99}
        print(f"hastegrad = {recievedData[3]}")
        if  recievedData[3]=="-1":
            print("Removing request")
            for i in range(len(requests)-1, -1, -1):
                if requests[i].get('Rom') == recivedDict.get('Rom') and requests[i].get('Seng') == recivedDict.get('Seng') and requests[i].get('Hva') == recivedDict.get('Hva'):
                    print(f"Hastegrad: {recivedDict.get('Hastegrad')}")
                    if requests[i].get('Hastegrad') == 1:
                        cf.fileWrite("logFileData.txt", cf.logStringData(recievedData[4], requests[i], "Remote Delete", cf.getCurrentTime()))
                        cf.fileWrite("logFileText.txt", cf.logStringText(recievedData[4], requests[i], "Remote Delete", cf.getCurrentTime()))
                    else:
                        cf.fileWrite("logFileData.txt", cf.logStringData(f"Rom {recivedDict.get('Rom')}", requests[i], "Room Delete", cf.getCurrentTime()))
                        cf.fileWrite("logFileText.txt", cf.logStringText(f"Rom {recivedDict.get('Rom')}", requests[i], "Room Delete", cf.getCurrentTime()))
                    requests.pop(i)
                    print("Request removed")
                    cf.sort_Hastegrad_ID_Time(requests)
                    print("before funcion 1")
                    updateButtons()
                    print("after funcion 1")
                    cf.print_requests(requests)
            
        elif recievedData[3] != "0":         
            for i in requests:
                if i.get('Rom')== recivedDict.get('Rom') and i.get('Seng')== recivedDict.get('Seng') and i.get('Hva')== recivedDict.get('Hva'):
                    update = False
                    if recivedDict.get('Hastegrad') < i.get('Hastegrad'):
                        print("Hastegrad endret")
                        cf.fileWrite("logFileText.txt",cf.logStringText(f"Rom {recivedDict.get('Rom')}",recivedDict,"Increase Importance",cf.getCurrentTime()))
                        cf.fileWrite("logFileData.txt",cf.logStringData(f"Rom {recivedDict.get('Rom')}",recivedDict,"Increase Importance",cf.getCurrentTime()))
                        i['Hastegrad'] = recivedDict.get('Hastegrad')
                        update = True
                    isEqual = True
                    
            if not isEqual:
                requests.append(recivedDict)
                if recievedData[3] == "1":
                    cf.fileWrite("logFileData.txt",cf.logStringData(recievedData[4],recivedDict,"Added",cf.getCurrentTime()))
                    cf.fileWrite("logFileText.txt",cf.logStringText(recievedData[4],recivedDict,"Added",cf.getCurrentTime()))
                else:
                    cf.fileWrite("logFileData.txt",cf.logStringData(f"Rom {recivedDict.get('Rom')}",recivedDict,"Added",cf.getCurrentTime()))
                    cf.fileWrite("logFileText.txt",cf.logStringText(f"Rom {recivedDict.get('Rom')}",recivedDict,"Added",cf.getCurrentTime()))
            else:
                print("Request already in list")
            if update:
                cf.sort_Hastegrad_ID_Time(requests)
                
                print("before funcion 2")
                updateButtons()
                print("after funcion 2")
                cf.print_requests(requests)
        else:
            indexlist = []
            for index,i in enumerate(requests):
                print(f"{recievedData[2] == 'Remove'} {i.get('Rom') == int(recievedData[0])} { i.get('Seng') == int(recievedData[1])}")
                if recievedData[2] == 'Remove' and i.get('Rom') == int(recievedData[0]) and i.get('Seng') == int(recievedData[1]):
                    print(f"added {index} to indexlist")
                    indexlist.append(index)
            for i in range(len(indexlist)-1,-1,-1):
                cf.fileWrite("logFileData.txt",cf.logStringData(recievedData[4],requests[indexlist[i]],"Remote Delete",cf.getCurrentTime()))
                cf.fileWrite("logFileText.txt",cf.logStringText(recievedData[4],requests[indexlist[i]],"Remote Delete",cf.getCurrentTime()))
                print(f"Removing:{requests.pop(indexlist[i])}")
            cf.sort_Hastegrad_ID_Time(requests)
            print("before funcion 3")
            updateButtons()
            print("after funcion 3")
            cf.print_requests(requests)


    except Exception as e:
        print(f"Exception: {e}")
        print("Data could not be used")
        print("Here")
        pass

def receive_data():
    global client
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind(("38:d5:7a:7d:5d:2e", 4))

    server.listen(99)

    client, address = server.accept()

    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            useData(data)
    except OSError as e:
        pass
    client.close()
    server.close()

# Create a new thread to run the receive_data function

def setUser(userName):
    global currentUser
    currentUser = userName
    root.title(f"Pålogget som {currentUser}")
    return


requests = []
"""requests.append({"Rom":301,"Seng":1, "Hva":"ALARM", "Hastegrad":1, "Tid":"10:25:23","Occupied":True, "ID": 1})
requests.append({"Rom":305,"Seng":1, "Hva":"Do", "Hastegrad":2, "Tid":"12:46:09" ,"Occupied":True,"ID": 2})
requests.append({"Rom":308,"Seng":1, "Hva":"Mat", "Hastegrad":1, "Tid":"13:35:09","Occupied":False, "ID": 3})
requests.append({"Rom":311,"Seng":2, "Hva":"Vann", "Hastegrad":3, "Tid":"12:23:23","Occupied":False, "ID": 5})
requests.append({"Rom":313,"Seng":1, "Hva":"Spørsmål", "Hastegrad":3, "Tid":"12:26:25","Occupied":True, "ID": 6})
requests.append({"Rom":306,"Seng":2, "Hva":"Vann", "Hastegrad":2, "Tid":"12:16:25","Occupied":False, "ID": 7})
requests.append({"Rom":304,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:27","Occupied":False, "ID": 8})
requests.append({"Rom":302,"Seng":1, "Hva":"Vann", "Hastegrad":4, "Tid":"12:26:25","Occupied":False, "ID": 9})
requests.append({"Rom":309,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:25","Occupied":True, "ID": 10})
requests.append({"Rom":315,"Seng":1, "Hva":"Vann", "Hastegrad":4, "Tid":"12:26:25","Occupied":False, "ID": 11})
requests.append({"Rom":307,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:25","Occupied":False, "ID": 12})

requests.append({"Rom":301,"Seng":1, "Hva":"ALARM", "Hastegrad":2, "Tid":"10:25:23","Occupied":True, "ID": 1})
requests.append({"Rom":305,"Seng":1, "Hva":"Do", "Hastegrad":3, "Tid":"12:46:09" ,"Occupied":True,"ID": 2})
requests.append({"Rom":308,"Seng":1, "Hva":"Mat", "Hastegrad":2, "Tid":"13:35:09","Occupied":True, "ID": 3})
requests.append({"Rom":302,"Seng":2, "Hva":"Vann", "Hastegrad":4, "Tid":"12:23:23","Occupied":True, "ID": 4})
requests.append({"Rom":311,"Seng":2, "Hva":"Vann", "Hastegrad":4, "Tid":"12:23:23","Occupied":True, "ID": 5})
requests.append({"Rom":313,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:25","Occupied":True, "ID": 6})
requests.append({"Rom":306,"Seng":2, "Hva":"Vann", "Hastegrad":3, "Tid":"12:16:25","Occupied":True, "ID": 7})
requests.append({"Rom":304,"Seng":1, "Hva":"Spørsmål", "Hastegrad":5, "Tid":"12:26:27","Occupied":True, "ID": 8})
requests.append({"Rom":302,"Seng":1, "Hva":"Vann", "Hastegrad":5, "Tid":"12:26:25","Occupied":True, "ID": 9})
requests.append({"Rom":309,"Seng":1, "Hva":"Spørsmål", "Hastegrad":5, "Tid":"12:26:25","Occupied":True, "ID": 10})
requests.append({"Rom":315,"Seng":1, "Hva":"Vann", "Hastegrad":5, "Tid":"12:26:25","Occupied":True, "ID": 11})
requests.append({"Rom":307,"Seng":1, "Hva":"Spørsmål", "Hastegrad":5, "Tid":"12:26:25","Occupied":True, "ID": 12})
requests.append({"Rom":303,"Seng":2, "Hva":"ALARM", "Hastegrad":2, "Tid":"10:25:23","Occupied":True, "ID": 13})
requests.append({"Rom":301,"Seng":1, "Hva":"SOS", "Hastegrad":2, "Tid":"10:25:23","Occupied":False, "ID": 1})
requests.append({"Rom":301,"Seng":1, "Hva":"Smerte", "Hastegrad":3, "Tid":"12:46:09" ,"Occupied":False,"ID": 2})
requests.append({"Rom":301,"Seng":1, "Hva":"Betjening", "Hastegrad":4, "Tid":"13:35:09","Occupied":False, "ID": 3})
requests.append({"Rom":301,"Seng":1, "Hva":"Skive m/brunost", "Hastegrad":5, "Tid":"12:23:23","Occupied":False, "ID": 4})"""
#print("UNSORTED:  ")
#cf.print_requests(requests)
cf.sort_Hastegrad_ID_Time(requests)
#print("SORTED:  ")
#cf.print_requests(requests)

root = tk.Tk()
root.title(pageTitle)
root.attributes('-fullscreen',True)
#root.maxsize(max_width, max_height)
#root.minsize(max_width, max_height)
root.geometry(str(max_width) + "x" + str(max_height))
root["background"] = windowBackgroundColor

# Adds alerts
left_frame = Frame(root, width=int(max_width*0.4 - 2*max_height*0.01), height=int(max_height - 2*max_height*0.01), bg='grey')
left_frame.grid(row=0, column=0, rowspan=2, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

# Adds room layout
rightTop_frame = Frame(root, width=int(max_width*0.6 - 2*max_height*0.01), height=int(max_height*0.5 - 2*max_height*0.01), bg='grey')
rightTop_frame.grid(row=0, column=1, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

# Adds food orders
rightBottom_frame = Frame(root, width=int(max_width*0.6 - 2*max_height*0.01), height=int(max_height*0.5 - 2*max_height*0.01), bg=windowBackgroundColor)
rightBottom_frame.grid(row=1, column=1, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

# Adds food menu
rightBottomRight_frame = Frame(rightBottom_frame,bg="grey")
rightBottomRight_frame.place(relx= 0.4625,rely = 0,relwidth = 0.5375,relheight = 1)
rightBottomLeft_frame = Frame(rightBottom_frame,bg="#123456")
rightBottomLeft_frame.place(relx= 0,rely = 0,relwidth = 0.4375,relheight = 1)
# Configure row and column weights to distribute space
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create a menu of users
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Amalie",command=lambda: setUser("Amalie"))
filemenu.add_command(label="Daniel",command=lambda: setUser("Daniel"))
filemenu.add_command(label="Eivind",command=lambda: setUser("Eivind"))
filemenu.add_command(label="Nicole",command=lambda: setUser("Nicole"))
filemenu.add_command(label="Palina",command=lambda: setUser("Palina"))
menubar.add_cascade(label="Brukervalg",font=("Arial",18), menu=filemenu)
root.config(menu=menubar)

image_path = r"images\romLayout.png"  
image = PhotoImage(file=image_path)
image_label = Label(rightTop_frame, image=image, bg='grey') # Create a label with the image
image_label.pack(fill=tk.BOTH, expand=True) # Fill the entire frame with the image
currentButton = 0
index = 0 
buttons = []
romMerking = []
menubuttons = []
fasteRom = []
alleRom = [301,302,303,304,305,306,307,308,309,311,313,315]



"""def sendFoodOrder(textcolor = "white",textFont = ("Consolas",18)):

    #FROKOST
    frokostLabel = tk.Label(rightBottomLeft_frame, text="Frokost", font=textFont,bg=bgcolor,fg=textcolor)
    frokostLabel.place(relx=0.05, rely=0.0, relwidth=0.9, relheight=0.1)

    room0Entry = tk.Entry(rightBottomLeft_frame, font=textFont)
    room0Entry.place(relx=0.05, rely=0.1, relwidth=0.65, relheight=0.2)

    submit0Button = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=textFont,
                            bg=buttonColor)
                            #command=lambda: sendFoodOrderButton(roomEntry.get()))
    submit0Button.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.2)
    #MIDDAG
    middagLabel = tk.Label(rightBottomLeft_frame, text="Middag", font=textFont,bg=bgcolor,fg=textcolor)
    middagLabel.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.1)

    roomEntry1 = tk.Entry(rightBottomLeft_frame, font=textFont)
    roomEntry1.place(relx=0.05, rely=0.4, relwidth=0.65, relheight=0.2)

    submitButton1 = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=textFont,
                            bg=buttonColor)
                            #command=lambda: sendFoodOrderButton(roomEntry.get()))
    submitButton1.place(relx=0.75, rely=0.4, relwidth=0.2, relheight=0.2)
    #KVELDS
    kveldsLabel = tk.Label(rightBottomLeft_frame, text="Kvelds", font=textFont,bg=bgcolor,fg=textcolor)
    kveldsLabel.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.1)

    roomEntry2 = tk.Entry(rightBottomLeft_frame, font=textFont)
    roomEntry2.place(relx=0.05, rely=0.7, relwidth=0.65, relheight=0.2)

    submitButton2 = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=textFont,
                            bg=buttonColor)
                            #command=lambda: sendFoodOrderButton(roomEntry.get()))
    submitButton2.place(relx=0.75, rely=0.7, relwidth=0.2, relheight=0.2)"""
Valgt = "Frokost"
changeButtonText = "Bytt til kvelds"
topColor = "#73F7C6"
bottomColor = "#4E7869"

# Change the food options
def changebuttonfunction():
    global Valgt
    global changeButtonText
    global topColor
    global bottomColor
    if Valgt == "Frokost":
        Valgt = "Kvelds"
        changeButtonText = "Bytt til frokost"
        topColor = "#4E7869"
        bottomColor = "#73F7C6"
    else:
        Valgt = "Frokost"
        changeButtonText = "Bytt til kvelds"
        topColor = "#73F7C6"
        bottomColor = "#4E7869"
    frokostKveldsOrder()
def sendOrder(data):
    sendData(data)
    sendFoodOrder()
def frokostKveldsOrder():

    for i in rightBottomLeft_frame.winfo_children():
        i.destroy()
    fkLabel = tk.Label(rightBottomLeft_frame, text=Valgt, font=("Consolas",18),bg=topColor,fg="black")
    fkLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
    changeButton = tk.Button(rightBottomLeft_frame,text=changeButtonText,font=("Consolas",18),bg=bottomColor,command=changebuttonfunction)
    changeButton.place(relx=0.2, rely=0.14, relwidth=0.6, relheight=0.1)
    fasteLabel = tk.Label(rightBottomLeft_frame, text="Faste rom:", font=("Consolas",18),bg="#F84545",fg="black")
    fasteLabel.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.1)
    for index,rom in enumerate(fasteRom):
        x = index
        y = 0
        if index > 5:
            x = index-6
            y = 1
        romLabel = tk.Label(rightBottomLeft_frame, text=f"{rom}", font=("Consolas",18),bg="#F84545",fg="black")
        romLabel.place(relx=0.02+0.16333*x, rely=0.38+0.176*y, relwidth=0.14333, relheight=0.156)
    submitButton = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=("Consolas",18),
                            bg="#437EB8",
                            command=lambda: sendOrder(f"MatPopup,{Valgt}"))
    submitButton.place(relx=0.2, rely=0.75, relwidth=0.55, relheight=0.2)
    returnButton = tk.Button(rightBottomLeft_frame,
                            text="↵",
                            font=("Consolas",50),
                            bg="#949A9F",
                            command=sendFoodOrder)
    returnButton.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.2)
 
 # Setup for a lunch order      
def lunsjOrder():
    for i in rightBottomLeft_frame.winfo_children():
        i.destroy()
    lunsjLabel = tk.Label(rightBottomLeft_frame, text="Lunsj", font=("Consolas",18),bg="#73F7C6",fg="black")
    lunsjLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
    lunsjEntryLabel = tk.Label(rightBottomLeft_frame, text="Dagens lunsj:", font=("Consolas",18),bg="#73F7C6",fg="black")
    lunsjEntryLabel.place(relx=0.02, rely=0.14, relwidth=0.35, relheight=0.1)
    lunsjEntry = tk.Entry(rightBottomLeft_frame, font=("Consolas",18))
    lunsjEntry.place(relx=0.37, rely=0.14, relwidth=0.61, relheight=0.1)
    fasteLabel = tk.Label(rightBottomLeft_frame, text="Faste rom:", font=("Consolas",18),bg="#F84545",fg="black")
    fasteLabel.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.1)
    for index,rom in enumerate(fasteRom):
        x = index
        y = 0
        if index > 5:
            x = index-6
            y = 1
        romLabel = tk.Label(rightBottomLeft_frame, text=f"{rom}", font=("Consolas",18),bg="#F84545",fg="black")
        romLabel.place(relx=0.02+0.16333*x, rely=0.38+0.176*y, relwidth=0.14333, relheight=0.156)
    submitButton = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=("Consolas",18),
                            bg="#437EB8",
                            command=lambda: sendOrder(f"MatPopup,Lunsj,{lunsjEntry.get()}"))
    submitButton.place(relx=0.2, rely=0.75, relwidth=0.55, relheight=0.2)
    returnButton = tk.Button(rightBottomLeft_frame,
                            text="↵",
                            font=("Consolas",50),
                            bg="#949A9F",
                            command=sendFoodOrder)
    returnButton.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.2)
    
# Setup for a dinner order
def middagOrder():
    for i in rightBottomLeft_frame.winfo_children():
        i.destroy()
    middagLabel = tk.Label(rightBottomLeft_frame, text="Middag", font=("Consolas",18),bg="#F0AB44",fg="black")
    middagLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
    middagEntryLabel = tk.Label(rightBottomLeft_frame, text="Dagens middag:", font=("Consolas",18),bg="#F0AB44",fg="black")
    middagEntryLabel.place(relx=0.02, rely=0.14, relwidth=0.35, relheight=0.1)
    middagEntry = tk.Entry(rightBottomLeft_frame, font=("Consolas",18))
    middagEntry.place(relx=0.37, rely=0.14, relwidth=0.61, relheight=0.1)
    fasteLabel = tk.Label(rightBottomLeft_frame, text="Faste rom:", font=("Consolas",18),bg="#F84545",fg="black")
    fasteLabel.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.1)
    for index,rom in enumerate(fasteRom):
        x = index
        y = 0
        if index > 5:
            x = index-6
            y = 1
        romLabel = tk.Label(rightBottomLeft_frame, text=f"{rom}", font=("Consolas",18),bg="#F84545",fg="black")
        romLabel.place(relx=0.02+0.16333*x, rely=0.38+0.176*y, relwidth=0.14333, relheight=0.156)
    submitButton = tk.Button(rightBottomLeft_frame,
                            text="Send",
                            font=("Consolas",18),
                            bg="#437EB8",
                            command=lambda: sendOrder(f"MatPopup,Middag,{middagEntry.get()}"))
    submitButton.place(relx=0.2, rely=0.75, relwidth=0.55, relheight=0.2)
    returnButton = tk.Button(rightBottomLeft_frame,
                            text="↵",
                            font=("Consolas",50),
                            bg="#949A9F",
                            command=sendFoodOrder)
    returnButton.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.2)

# Set fasting rooms
def fasteButtonFunction(rom):
    global fasteRom
    if rom in fasteRom:
        fasteRom.remove(rom)
        sendData(f"MatPopup,{rom},RemoveFaste")
        print(f"Removed faste rom:{rom}")
        cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,{"Rom":rom},"Faste Removed",cf.getCurrentTime()))
        cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,{"Rom":rom},"Faste Removed",cf.getCurrentTime()))
    else:
        fasteRom.append(rom)
        fasteRom.sort()
        sendData(f"MatPopup,{rom},AddFaste")
        print(f"Added faste rom:{rom}")
        cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,{"Rom":rom},"Faste Added",cf.getCurrentTime()))
        cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,{"Rom":rom},"Faste Added",cf.getCurrentTime()))
    fasteOrder()
fasteDots = []
for index,i in enumerate(fasteRom):
    fasteDots.append(tk.Label(rightTop_frame, text="◉", font=("Consolas",20),bg="#fbfafa",fg="#FF0000"))
    fasteDots[index].place(x=cf.roomPosition(i)[0]+18,y=cf.roomPosition(i)[1]+140)
def fasteOrder():
    for i in rightBottomLeft_frame.winfo_children():
        i.destroy()
    for i in fasteDots:
        i.destroy()
    fasteDots.clear()
    fasteLabel = tk.Label(rightBottomLeft_frame, text="Faste", font=("Consolas",18),bg="#F84545",fg="black")
    fasteLabel.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
    romLabel = []
    for rom in alleRom:
        buttonColor = "#7AEE56"
        buttonText = f"Legg til\n{rom}"
        if rom in fasteRom:
            buttonText = f"Fjern rom:\n{rom}"
            buttonColor = "#F84545"
        romLabel.append(tk.Button(rightBottomLeft_frame, text=buttonText, font=("Consolas",18),bg=buttonColor,fg="black",command=lambda rom=rom:fasteButtonFunction(rom)))
    x = 0
    y = 0
    for romLabels in romLabel:
        if x > 3:
            x -=4
            y += 1
        #print(f"x:{x}, y:{y}")
        romLabels.place(relx=0.02+0.24*x, rely=0.14+0.2*y, relwidth=0.24, relheight=0.2)
        x += 1
    returnButton = tk.Button(rightBottomLeft_frame,
                            text="↵",
                            font=("Consolas",50),
                            bg="#949A9F",
                            command=sendFoodOrder)
    returnButton.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.2)

    for index,i in enumerate(fasteRom):
        fasteDots.append(tk.Label(rightTop_frame, text="◉", font=("Consolas",20),bg="#fbfafa",fg="#FF0000"))
        fasteDots[index].place(x=cf.roomPosition(i)[0]+18,y=cf.roomPosition(i)[1]+140)

# Arrange buttons in the food menu section
def sendFoodOrder(textFont = ("Consolas",30)):
    #FROKOST
    for i in rightBottomLeft_frame.winfo_children():
        i.destroy()
    frokostButton = tk.Button(rightBottomLeft_frame,
                            text="Frokost/\nKvelds",
                            font=textFont,
                            bg="#59D8E8",
                            command=frokostKveldsOrder)
    lunsjButton = tk.Button(rightBottomLeft_frame,
                            text="Lunsj",
                            font=textFont,
                            bg="#73F7C6",
                            command=lunsjOrder)
    middagButton = tk.Button(rightBottomLeft_frame,
                            text="Middag",
                            font=textFont,
                            bg="#F0AB44",
                            command=middagOrder)
    fasteButton = tk.Button(rightBottomLeft_frame,
                            text="Faste",
                            font=textFont,
                            bg="#DF513E",
                            command=fasteOrder)
    frokostButton.place(relx=0.01, rely=0.01, relwidth=0.485, relheight=0.485)
    lunsjButton.place(relx=0.505, rely=0.01, relwidth=0.485, relheight=0.485)
    middagButton.place(relx=0.01, rely=0.505, relwidth=0.485, relheight=0.485)
    fasteButton.place(relx=0.505, rely=0.505, relwidth=0.485, relheight=0.485)
sendFoodOrder()

def showFoodOrders(textcolor = "#000000",textFont = ("Consolas",16)):
    for i in rightBottomRight_frame.winfo_children():
        i.destroy()
    foodStuff = ["Juice","Vann","Saft","Kaffe","Te","Skive m/ost","Skive m/skinke","Skive m/egg","Skive m/syltetøy","Skive m/brunost","Drikke","Mat","Middag","Lunsj"]
    foodStuff2 = ["Brødskive","Knekkebrød","Rundstykke","Ost","Skinke","Egg","Majones","Syltetøy","Brunost"]
    foodRequests = []
    for i in requests:
        if i.get('Hva') in foodStuff:
            foodRequests.append(i)
        else:
            hvaList = i.get('Hva').split(".")
            for j in hvaList:
                if j in foodStuff2:
                    foodRequests.append(i)
                    break
    for index, i in enumerate(foodRequests):
        foodButton = tk.Button(rightBottomRight_frame,
                            text=f"Rom {i.get('Rom'):3},{i.get('Seng'):1} Ønske: {i.get('Hva'):8} {i.get('Tid'):8}",
                            font=textFont,
                            bg = cf.color(i.get("Hastegrad")),
                            fg=textcolor)
        foodButton.place(relx=0.0, rely=0+index*0.1, relwidth=1, relheight=0.1)

showFoodOrders()

def buttonFunction(buttonIndex):
    global currentButton
    currentButton = buttonIndex+1
    print(currentButton)
    if requests[buttonIndex].get('Occupied'):
        button_texts[3]= "Fjern tistedeværelse"
    else:
        button_texts[3]= "Legg til tilstedeværelse"
    menubuttons.pop(-1)
    
    menubuttons.append(tk.Button(left_frame,
                            text=button_texts[3],
                            font=("Consolas", 14),
                            bg=menuButtonColor[3],
                            command = changeOccupancy))
    # Forget all previously packed buttons and menu buttons
    for i in left_frame.winfo_children():
        i.place_forget()
    popdown = 0
    for index,button in enumerate(buttons):
        button.place(relx=0.0, rely=(popdown+index)*0.05, relwidth=1, relheight=0.05)
        if index == buttonIndex:
            """for index2,button2 in enumerate(menubuttons):
                popdown=2
                button2.place(relx=0.25*index2, rely=(popdown+index)*0.05, relwidth=0.25, relheight=0.05)"""
            popdown = 2
            menubuttons[0].place(relx=0.0, rely=(index+1)*0.05, relwidth=0.5, relheight=0.05)
            menubuttons[1].place(relx=0.5, rely=(index+1)*0.05, relwidth=0.5, relheight=0.05)
            menubuttons[3].place(relx=0.0, rely=(index+2)*0.05, relwidth=0.5, relheight=0.05)
            menubuttons[2].place(relx=0.5, rely=(index+2)*0.05, relwidth=0.5, relheight=0.05)

    
    #print("Button pressed")
    return


def changeOccupancy():
    global requests
    global currentButton
    if requests[currentButton-1].get('Occupied'):
        requests[currentButton-1]['Occupied']= False
        for index,i in enumerate(requests):
            if i.get('Rom')== requests[currentButton-1].get('Rom'):
                requests[index]['Occupied']= False
        #log changes
        cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,requests[currentButton-1],"Unoccupied",cf.getCurrentTime()))
        cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,requests[currentButton-1],"Unoccupied",cf.getCurrentTime()))
    else:
        requests[currentButton-1]['Occupied']= True
        for index,i in enumerate(requests):
            if i.get('Rom')== requests[currentButton-1].get('Rom'):
                requests[index]['Occupied']= True
        #log changes
        cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,requests[currentButton-1],"Occupied",cf.getCurrentTime()))
        cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,requests[currentButton-1],"Occupied",cf.getCurrentTime()))
    
    updateButtons()
    return


def get_lowest_hastegrad_requests(requests):
    lowest_hastegrad_requests = []
    room_hastegrad_map = {}
    for request in requests:
        room = request.get('Rom')
        hastegrad = request.get('Hastegrad')
        if room not in room_hastegrad_map:
            room_hastegrad_map[room] = hastegrad
        else:
            if hastegrad < room_hastegrad_map[room]:
                room_hastegrad_map[room] = hastegrad
    for request in requests:
        room = request.get('Rom')
        hastegrad = request.get('Hastegrad')
        if hastegrad == room_hastegrad_map[room]:
            lowest_hastegrad_requests.append(request)
    
    return lowest_hastegrad_requests

def updateButtons():
    global buttons
    global romMerking
    global lowest_hastegrad_requests
    for i in left_frame.winfo_children():
        i.place_forget()
    
    showFoodOrders()
    sendFoodOrder()
    for i, label in enumerate(romMerking):
        label.place_forget()
    buttons.clear()
    romMerking.clear()
    for index, i in enumerate(requests):
        buttons.append(tk.Button(left_frame,
                command=lambda index=index: buttonFunction(index),
                text=f"Rom {i.get('Rom'):3},{i.get('Seng'):1} Ønske: {i.get('Hva'):8} {i.get('Tid'):8}",
                font=("Consolas",16),
                bg = cf.color(i.get("Hastegrad")),
                pady=10,
                padx=10))
    
    for index,i in enumerate(get_lowest_hastegrad_requests(requests)):
        romMerking.append(tk.Label(rightTop_frame,
                text="!",
                font=romMerkingFont,
                bg=cf.occupiedColor(i),
                fg = cf.color(i.get('Hastegrad')),
                padx=romMerkingPadx,
                pady=romMerkingPady
                ))
        romMerking[index].place(x=cf.roomPosition(i.get('Rom'))[0],
                            y=cf.roomPosition(i.get('Rom'))[1])
        for index,button in enumerate(buttons):
            button.place(relx=0.0, rely=index*0.05, relwidth=1, relheight=0.05)

def okHastegrad():

    global requests
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 1:
                requests[index]['Hastegrad']= i.get('Hastegrad')-1
                #log changes
                cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,requests[currentButton-1],"Increase Importance",cf.getCurrentTime()))
                cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,requests[currentButton-1],"Increase Importance",cf.getCurrentTime()))
                
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    cf.sort_Hastegrad_ID_Time(requests)
    
    updateButtons()
      
def senkHastegrad():
    global requests
    
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 5:
                #log changes
                requests[index]['Hastegrad']= i.get('Hastegrad')+1
                cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,requests[currentButton-1],"Decrease Importance",cf.getCurrentTime()))
                cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,requests[currentButton-1],"Decrease Importance",cf.getCurrentTime()))
                
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    cf.sort_Hastegrad_ID_Time(requests)
    
    updateButtons()

    
def fjernRequest():
    global requests
    global currentButton
    if clientEnabled:
        sendData(f"Remote Remove,{requests[currentButton-1].get('Rom')},{requests[currentButton-1].get('Seng')},{requests[currentButton-1].get('Hva')},{requests[currentButton-1].get('Hastegrad')}")
    #log changes
    cf.fileWrite("logFileText.txt",cf.logStringText(currentUser,requests[currentButton-1],"Delete",cf.getCurrentTime()))
    cf.fileWrite("logFileData.txt",cf.logStringData(currentUser,requests[currentButton-1],"Delete",cf.getCurrentTime()))
    # Remove the request at the currentButton index
    requests.pop(currentButton-1)
    cf.sort_Hastegrad_ID_Time(requests)
    # Reset currentButton to 0 if there are no more requests
    if not requests:
        currentButton = 0
    else:
        # If currentButton is now out of range, set it to the last index
        currentButton = min(currentButton, len(requests))
    
    # Clear and update buttons and romMerking
    
    updateButtons()




menubuttons.append(tk.Button(left_frame,
                            text=button_texts[0],
                            font=("Consolas", 14),
                            bg=menuButtonColor[0],
                            command = fjernRequest))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[1],
                            font=("Consolas", 14),
                            bg=menuButtonColor[1],
                            command = okHastegrad))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[2],
                            font=("Consolas", 14),
                            bg=menuButtonColor[2],
                            command = senkHastegrad))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[3],
                            font=("Consolas", 14),
                            bg=menuButtonColor[3],
                            command = changeOccupancy))
"""
for index, i in enumerate(requests):
    buttons.append(tk.Button(left_frame,
              command=lambda index=index: buttonFunction(index),
              text=f"Rom: {i.get('Rom'):3} Seng: {i.get('Seng'):1} Ønsker: {i.get('Hva'):8} Tid: {i.get('Tid'):8}",
              font=("Consolas",16),
              bg = cf.color(i.get("Hastegrad")),
              pady=10,
              padx=10))
    romMerking.append(tk.Label(rightTop_frame,
             text="!",
             font=romMerkingFont,
             bg=cf.occupiedColor(i),
             fg = cf.color(i.get('Hastegrad')),
             padx=romMerkingPadx,
             pady=romMerkingPady
             ))
for index,button in enumerate(buttons):
    button.place(relx=0.0, rely=index*0.05, relwidth=1, relheight=0.05)
for i in range(len(romMerking)):
    romMerking[i].place(x=cf.roomPosition(requests[i].get('Rom'))[0],
                        y=cf.roomPosition(requests[i].get('Rom'))[1])"""
updateButtons()
if clientEnabled:
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()
root.mainloop()
