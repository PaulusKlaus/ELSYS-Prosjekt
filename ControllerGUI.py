import tkinter as tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
import time as t
import ControllerFunctions as cf

#Defined colors and functions
roomMarkBG_Color = "#A2E8A8"  ##fbfafa  standar
max_width = 1800 #Defines the maximum width of the window
max_height = int((max_width/16)*9) #calculates the height of the window relation 16:9
pageTitle = "Romoversikt" #Defines the title of the window
button_texts = ["Fjern", "Øke Hastighetsgrad", "Senk hastighetsgrad", "Test"]

requests = []
requests.append({"Rom":301,"Seng":1, "Hva":"ALARM", "Hastegrad":1, "Tid":"10:25:23", "ID": 1})
requests.append({"Rom":305,"Seng":1, "Hva":"Do", "Hastegrad":2, "Tid":"12:46:09" , "ID": 2})
requests.append({"Rom":308,"Seng":1, "Hva":"Mat", "Hastegrad":1, "Tid":"13:35:09", "ID": 3})
requests.append({"Rom":311,"Seng":2, "Hva":"Vann", "Hastegrad":3, "Tid":"12:23:23", "ID": 5})
requests.append({"Rom":313,"Seng":1, "Hva":"Spørsmål", "Hastegrad":3, "Tid":"12:26:25", "ID": 6})
requests.append({"Rom":306,"Seng":2, "Hva":"Vann", "Hastegrad":2, "Tid":"12:16:25", "ID": 7})
requests.append({"Rom":304,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:27", "ID": 8})
requests.append({"Rom":302,"Seng":1, "Hva":"Vann", "Hastegrad":4, "Tid":"12:26:25", "ID": 9})
requests.append({"Rom":309,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:25", "ID": 10})
requests.append({"Rom":315,"Seng":1, "Hva":"Vann", "Hastegrad":4, "Tid":"12:26:25", "ID": 11})
requests.append({"Rom":307,"Seng":1, "Hva":"Spørsmål", "Hastegrad":4, "Tid":"12:26:25", "ID": 12})
requests.append({"Rom":303,"Seng":1, "Hva":"Vann", "Hastegrad":4, "Tid":"12:26:25", "ID": 13})
#print("UNSORTED:  ")
#cf.print_requests(requests)
cf.sort_Hastegrad_ID_Time(requests)
#print("SORTED:  ")
#cf.print_requests(requests)

root = tk.Tk()
root.title(pageTitle)
#root.maxsize(max_width, max_height)
root.minsize(max_width, max_height)
root.geometry(str(max_width) + "x" + str(max_height))
root["background"] = "#bfd1e0"

left_frame = Frame(root, width=int(max_width*0.4 - 2*max_height*0.01), height=int(max_height - 2*max_height*0.01), bg='grey')
left_frame.grid(row=0, column=0, rowspan=2, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

rightTop_frame = Frame(root, width=int(max_width*0.6 - 2*max_height*0.01), height=int(max_height*0.5 - 2*max_height*0.01), bg='grey')
rightTop_frame.grid(row=0, column=1, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

rightBottom_frame = Frame(root, width=int(max_width*0.6 - 2*max_height*0.01), height=int(max_height*0.5 - 2*max_height*0.01), bg='grey')
rightBottom_frame.grid(row=1, column=1, padx=int(max_height*0.01), pady=int(max_height*0.01), sticky="nsew")

# Configure row and column weights to distribute space
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

image_path = "romLayout.png"  
image = PhotoImage(file=image_path)
image_label = Label(rightTop_frame, image=image, bg='grey')
image_label.pack(fill="x")
currentButton = 0
index = 0 
buttons = []
romMerking = []
menubuttons = []
def buttonFunction(buttonIndex):
    global currentButton
    currentButton = buttonIndex+1
    print(currentButton)
    # Forget all previously packed buttons and menu buttons
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    
    # Pack the buttons in the left frame
    for index, i in enumerate(buttons):
        i.pack(fill=tk.X, side=tk.TOP, expand=False)  # Adjusted parameters
        if index == buttonIndex:
            #print(f"index:{index}  Button index: {buttonIndex}")
            # Pack the menu buttons under the pressed button
            for button in menubuttons:
                button.pack(side=tk.TOP, fill=tk.X, expand=False)  # Adjusted parameters
    

    
    #print("Button pressed")
    return
def updateButtons():
    global buttons
    global romMerking
    buttons.clear()
    romMerking.clear()
    for index, i in enumerate(requests):
        buttons.append(tk.Button(left_frame,
                command=lambda index=index: buttonFunction(index),
                text=f"Rom: {i.get('Rom'):3} Seng: {i.get('Seng'):1} Ønsker: {i.get('Hva'):8} Tid: {i.get('Tid'):8}",
                font=("Consolas",18),
                bg = cf.color(i.get("Hastegrad")),
                pady=10,
                padx=10))
        romMerking.append(tk.Label(rightTop_frame,
                text="!",
                font=("Consolas",50),
                bg=roomMarkBG_Color,
                fg = cf.color(i.get('Hastegrad')),
                padx=10,
                pady=5
                )) 
def okHastegrad():

    global requests
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 1:
                requests[index]['Hastegrad']= i.get('Hastegrad')-1
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    cf.sort_Hastegrad_ID_Time(requests)
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    updateButtons()
    for i in buttons:
        i.pack(fill = tk.X)
    for i in range(len(romMerking)):
        romMerking[i].place(x=cf.roomPosition(requests[i].get('Rom'))[0],
                            y=cf.roomPosition(requests[i].get('Rom'))[1])
    
def senkHastegrad():
    
    global requests
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 4:
                requests[index]['Hastegrad']= i.get('Hastegrad')+1
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    cf.sort_Hastegrad_ID_Time(requests)
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    updateButtons()
    for i in buttons:
        i.pack(fill = tk.X)
    for i in range(len(romMerking)):
        romMerking[i].place(x=cf.roomPosition(requests[i].get('Rom'))[0],
                            y=cf.roomPosition(requests[i].get('Rom'))[1])
def fjernRequest():
    global requests
    global currentButton
    
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
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    
    updateButtons()
    for i in buttons:
        i.pack(fill=tk.X)
    for i in range(len(romMerking)):
        romMerking[i].place(x=cf.roomPosition(requests[i].get('Rom'))[0],
                            y=cf.roomPosition(requests[i].get('Rom'))[1])
        

menubuttons.append(tk.Button(left_frame,
                            text=button_texts[0],
                            font=("Consolas", 14),
                            bg="#437EB8",
                            command = fjernRequest,
                            padx =5,
                            pady =5))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[1],
                            font=("Consolas", 14),
                            bg="#437EB8",
                            command = okHastegrad,
                            padx =5,
                            pady =5))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[2],
                            font=("Consolas", 14),
                            bg="#437EB8",
                            command = senkHastegrad,
                            padx =5,
                            pady =5))
menubuttons.append(tk.Button(left_frame,
                            text=button_texts[3],
                            font=("Consolas", 14),
                            bg="#437EB8",
                            padx =5,
                            pady =5))

for index, i in enumerate(requests):
    buttons.append(tk.Button(left_frame,
              command=lambda index=index: buttonFunction(index),
              text=f"Rom: {i.get('Rom'):3} Seng: {i.get('Seng'):1} Ønsker: {i.get('Hva'):8} Tid: {i.get('Tid'):8}",
              font=("Consolas",18),
              bg = cf.color(i.get("Hastegrad")),
              pady=10,
              padx=10))
    romMerking.append(tk.Label(rightTop_frame,
             text="!",
             font=("Consolas",50),
             bg=roomMarkBG_Color,
             fg = cf.color(i.get('Hastegrad')),
             padx=10,
             pady=5
             ))
for i in buttons:
    i.pack(fill = tk.X)
for i in range(len(romMerking)):
    romMerking[i].place(x=cf.roomPosition(requests[i].get('Rom'))[0],
                        y=cf.roomPosition(requests[i].get('Rom'))[1])
root.mainloop()




