import tkinter as tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
import time as t

def color(hastegrad):
    if hastegrad== 1:
        return "#25F533"
    elif hastegrad == 2:
        return "#F3F041"
    elif hastegrad == 3:
        return "#FF800A"
    elif hastegrad == 4:
        return "#FF0000"
    else:
        return "#002E5D"

requests = []
requests.append({"Rom":301,"Seng":1, "Hva":"ALARM", "Hastegrad":4, "Tid":"10:25:23" })
requests.append({"Rom":315,"Seng":1, "Hva":"Do", "Hastegrad":3, "Tid":"12:46:09" })
requests.append({"Rom":321,"Seng":1, "Hva":"Mat", "Hastegrad":2, "Tid":"13:35:09" })
requests.append({"Rom":305,"Seng":2, "Hva":"Vann", "Hastegrad":1, "Tid":"12:26:25" })
requests.append({"Rom":304,"Seng":1, "Hva":"Spørsmål", "Hastegrad":1, "Tid":"12:26:25" })
requests.append({"Rom":302,"Seng":1, "Hva":"Vann", "Hastegrad":1, "Tid":"12:26:25" })
max_width = 1800
max_height = int((max_width/16)*9)

root = tk.Tk()
root.title("Romoversikt")
root.maxsize(max_width, max_height)
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

# Create a label to display the image
image_label = Label(rightTop_frame, image=image, bg='grey')
image_label.pack(fill="x")
for i in requests:
    tk.Label(left_frame,text=f"Rom: {i.get('Rom'):3} Seng: {i.get('Seng'):1} Ønsker: {i.get('Hva'):8} Tid: {i.get('Tid'):8}"  ,font=("Consolas",18),bg = color(i.get("Hastegrad")),width=int(0.029*max_width), height=int(0.003*max_height)).pack()
    print(i.get("Hastegrad"))


root.mainloop()

