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
def buttonFunction(i):

    button_texts = ["Fjern", "Øke Hastighetsgrad", "Senk hastighetsgrad", "Test"]
    for text in button_texts:
        tk.Button(left_frame,
                  text=text,
                  font=("Consolas", 14),
                  bg="blue").pack(side=tk.LEFT, expand=True, fill=tk.X)

    

    root.mainloop()
    print("Button pressed")
    return 
for i in requests:
   tk.Button(left_frame,
              command=lambda:buttonFunction(i),
              text=f"Rom: {i.get('Rom'):3} Seng: {i.get('Seng'):1} Ønsker: {i.get('Hva'):8} Tid: {i.get('Tid'):8}",
              font=("Consolas",18),
              bg = color(i.get("Hastegrad")),
              pady=10,
              padx=10).pack()
    
    tk.Label(rightTop_frame,
             text="!",
             font=("Consolas",50),
             bg="#fbfafa",
             fg = color(i.get('Hastegrad'))
             ).place(x=romPosition(i.get('Rom'))[0],
                     y=romPosition(i.get('Rom'))[1])
root.mainloop()



