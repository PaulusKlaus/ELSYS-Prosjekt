import tkinter as tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
import time as t

def color(hastegrad):
    if hastegrad== 1:
        return "#28F936"
    elif hastegrad == 2:
        return "#F3F041"
    elif hastegrad == 3:
        return "#FF800A"
    elif hastegrad == 4:
        return "#FF0000"
    else:
        return "#002E5D"
def romPosition(rom):
    if rom == 301:
        return (40,20)
    elif rom == 303:
        return (160,20)
    elif rom == 305:
        return (260,20)
    elif rom == 307:
        return (380,20)
    elif rom == 309:
        return (700,20)
    elif rom == 311:
        return (810,20)
    elif rom == 313:
        return (920,20)
    elif rom == 315:
        return (1030,20)
    elif rom == 302:
        return (150,350)
    elif rom == 304:
        return (260,350)
    elif rom == 306:
        return (810,350)
    elif rom == 308:
        return (920,350)
    else:
        print("Rom ikke funnet")
        return (0,0)

    

requests = []
requests.append({"Rom":301,"Seng":1, "Hva":"ALARM", "Hastegrad":4, "Tid":"10:25:23", "ID": 1})
requests.append({"Rom":305,"Seng":1, "Hva":"Do", "Hastegrad":3, "Tid":"12:46:09" , "ID": 2})
requests.append({"Rom":308,"Seng":1, "Hva":"Mat", "Hastegrad":3, "Tid":"13:35:09", "ID": 3})
requests.append({"Rom":311,"Seng":2, "Hva":"Vann", "Hastegrad":2, "Tid":"12:26:25", "ID": 4})
requests.append({"Rom":313,"Seng":1, "Hva":"Spørsmål", "Hastegrad":2, "Tid":"12:26:25", "ID": 5})
requests.append({"Rom":306,"Seng":2, "Hva":"Vann", "Hastegrad":1, "Tid":"12:26:25", "ID": 6})
requests.append({"Rom":304,"Seng":1, "Hva":"Spørsmål", "Hastegrad":1, "Tid":"12:26:25", "ID": 7})
requests.append({"Rom":302,"Seng":1, "Hva":"Vann", "Hastegrad":1, "Tid":"12:26:25", "ID": 8})

max_width = 1800
max_height = int((max_width/16)*9)

root = tk.Tk()
root.title("Romoversikt")
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
                bg = color(i.get("Hastegrad")),
                pady=10,
                padx=10))
        romMerking.append(tk.Label(rightTop_frame,
                text="!",
                font=("Consolas",50),
                bg="#fbfafa",
                fg = color(i.get('Hastegrad'))
                )) 
def okHastegrad():

    global requests
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 4:
                requests[index]['Hastegrad']= i.get('Hastegrad')+1
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    updateButtons()
    for i in buttons:
        i.pack(fill = tk.X)
    for i in range(len(romMerking)):
        romMerking[i].place(x=romPosition(requests[i].get('Rom'))[0],
                            y=romPosition(requests[i].get('Rom'))[1])
    
def senkHastegrad():
    
    global requests
    for index,i in enumerate(requests):
        print(f"id = {i.get('ID')}")
        print(f"currnetbutton = {currentButton}")
        if i.get('ID')== currentButton:
            print(f"hastegrad = {i.get('Hastegrad')}")
            if i.get('Hastegrad')!= 1:
                requests[index]['Hastegrad']= i.get('Hastegrad')-1
                print(f"Hastegrad endret til {requests[index].get('Hastegrad')}")
    for i in menubuttons:
        i.pack_forget()
    for i in buttons:
        i.pack_forget()
    updateButtons()
    for i in buttons:
        i.pack(fill = tk.X)
    for i in range(len(romMerking)):
        romMerking[i].place(x=romPosition(requests[i].get('Rom'))[0],
                            y=romPosition(requests[i].get('Rom'))[1])
def fjernRequest():
    global requests
    global currentButton
    
    # Remove the request at the currentButton index
    requests.pop(currentButton-1)
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
        romMerking[i].place(x=romPosition(requests[i].get('Rom'))[0],
                            y=romPosition(requests[i].get('Rom'))[1])
        
button_texts = ["Fjern", "Øke Hastighetsgrad", "Senk hastighetsgrad", "Test"]
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
              bg = color(i.get("Hastegrad")),
              pady=10,
              padx=10))
    romMerking.append(tk.Label(rightTop_frame,
             text="!",
             font=("Consolas",50),
             bg="#fbfafa",
             fg = color(i.get('Hastegrad'))
             ))
for i in buttons:
    i.pack(fill = tk.X)
for i in range(len(romMerking)):
    romMerking[i].place(x=romPosition(requests[i].get('Rom'))[0],
                        y=romPosition(requests[i].get('Rom'))[1])
root.mainloop()




