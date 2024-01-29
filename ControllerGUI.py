import tkinter as tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
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

root.mainloop()