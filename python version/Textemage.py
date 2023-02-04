"""
TEXTEMAGE
version: 1.2
author: Akash Bora (Akascape)
license: MIT
more info: https://github.com/Akascape/TEXTEMAGE
"""


import customtkinter as ctk
import tkinter
import os
import sys
from PIL import Image, ImageTk, UnidentifiedImageError
import random
import pytesseract
import webbrowser

ctk.set_default_color_theme(random.choice(['blue','green','dark-blue']))

root = ctk.CTk()
root.title("TEXTEMAGE")
root.geometry("900x500")
root.minsize(600,400)
root.rowconfigure(0, weight=1)
root.columnconfigure((0,1), weight=1)
root.bind("<1>", lambda event: event.widget.focus_set())

def resource(relative_path):
    # resource finder via pyinstaller
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

root.wm_iconbitmap()
icopath = ImageTk.PhotoImage(file=resource("icon.png"))
root.iconphoto(False, icopath)

file = ""
image = ""
previous = ""

def open_image():
    # open image file
    global file, image, img, previous
    file = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*webp'])
                                                          ,('All Files', '*.*')])
    if file:
        previous = file
        if len(os.path.basename(file))>=30:
            open_button.configure(text=os.path.basename(file)[:30]+"..."+os.path.basename(file)[-3:])
        else:
            open_button.configure(text=os.path.basename(file))

        try:
            Image.open(file)
        except UnidentifiedImageError:
            tk.messagebox.showerror("Oops!", "Not a valid image file!")
            return

        img = Image.open(file)   
        image = ctk.CTkImage(img)
        label_image.configure(text="", image=image)
        image.configure(size=(label_image.winfo_height(),label_image.winfo_height()*img.size[1]/img.size[0]))
    else:
        if previous!="":
            file = previous
            
def resize_event(event):
    # dynamic resize of the image with UI
    global image
    if image!="":
        image.configure(size=(event.height,event.height*img.size[1]/img.size[0]))

def convert():
    # do the conversion
    if not file:
        return
    try:
        result = pytesseract.image_to_string(img)
    except:
        tkinter.messagebox.showerror("Missing Tesseract-OCR!",
                                     "Tesseract is not installed or it's not in your PATH")
        return

    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.END, result)

if ctk.get_appearance_mode()=="Dark":
    o = 1
else:
    o = 0
    
def new_window():
    # About window 
    label_header.configure(state="disabled")
    
    def exit_top_level():
        top_level.destroy()
        label_header.configure(state="normal")
        
    def web(link):
        webbrowser.open_new_tab(link)
        
    top_level = ctk.CTkToplevel(root)
    top_level.protocol("WM_DELETE_WINDOW", exit_top_level)
    top_level.minsize(400,200)
    top_level.title("About")
    top_level.attributes("-topmost", True)
    top_level.resizable(width=False, height=False)
    top_level.wm_iconbitmap()
    top_level.iconphoto(False, icopath)
    
    label_top = ctk.CTkLabel(top_level, text="Textemage v1.2", font=("Roboto",15))
    label_top.grid(padx=20, pady=20, sticky="w")
    
    try:
        version = str(pytesseract.get_tesseract_version())[:5]
    except:
        version = "Unknown"
        
    desc = "Tesseract version: "+version+"\n\nDeveloped by Akash Bora (Akascape) \nLicense: MIT \nCopyright 2023 "
    label_disc = ctk.CTkLabel(top_level,  text=desc, justify="left", font=("Roboto",12))
    label_disc.grid(padx=20, pady=0, sticky="w")

    logo = ctk.CTkImage(Image.open(resource("icon.png")), size=(150,150))
    
    label_logo = ctk.CTkLabel(top_level, text="", image=logo)
    label_logo.place(x=230,y=20)
    
    link = ctk.CTkLabel(top_level, text="Official Page", justify="left", font=("",13), text_color="light blue")
    link.grid(padx=20, pady=0, sticky="w")   
    link.bind("<Button-1>", lambda event: web("https://github.com/Akascape/TEXTEMAGE"))
    link.bind("<Enter>", lambda event: link.configure(font=("", 13, "underline"), cursor="hand2"))
    link.bind("<Leave>", lambda event: link.configure(font=("", 13), cursor="arrow"))

DIRPATH = os.getcwd()

with open(os.path.join(DIRPATH,"tesseract_path.txt"), 'r') as tfile:
    patht = tfile.read() # read the path from the path file
    pytesseract.pytesseract.tesseract_cmd = patht
    tfile.close()

frame_1 = ctk.CTkFrame(root)
frame_1.grid(row=0, column=0, sticky="news", padx=20, pady=20)
frame_1.rowconfigure(2, weight=1)
frame_1.columnconfigure(0, weight=1)

frame_2 = ctk.CTkFrame(root)
frame_2.grid(row=0, column=1, sticky="news", padx=(0,20), pady=20)
frame_2.rowconfigure(1, weight=1)
frame_2.columnconfigure(0, weight=1)

label_header = ctk.CTkButton(frame_1, text="TEXTEMAGE", fg_color=ctk.ThemeManager.theme["CTkTextbox"]["fg_color"][o],
                             height=30, command=new_window, hover=False, corner_radius=30)
label_header.grid(padx=10, pady=10)

open_button = ctk.CTkButton(frame_1, text="OPEN SOURCE IMAGE", command=open_image, corner_radius=30)
open_button.grid(padx=10, pady=10, sticky="nwe")

image_frame = ctk.CTkFrame(frame_1, corner_radius=20)
image_frame.grid(padx=10, pady=10, sticky="nwes")
image_frame.rowconfigure(0, weight=1)
image_frame.columnconfigure(0, weight=1)

label_image = ctk.CTkLabel(image_frame, text="➕", corner_radius=10)
label_image.grid(padx=10, pady=10, sticky="nwes")

image_frame.bind("<Configure>", resize_event)

convert_button = ctk.CTkButton(frame_1, text="EXTRACT", command=convert, corner_radius=30)
convert_button.grid(padx=10, pady=10, sticky="we")

label_2 = ctk.CTkLabel(frame_2, text="Converted text will be shown here")
label_2.grid(padx=10, pady=10)

text_box = ctk.CTkTextbox(frame_2)
text_box.grid(sticky="news", padx=10, pady=10)
text_box._textbox.configure(selectbackground=open_button._apply_appearance_mode(open_button._fg_color))

root.mainloop()
