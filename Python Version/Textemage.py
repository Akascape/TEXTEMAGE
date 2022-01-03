import pytesseract
from PIL import Image
from tkinter import Tk, Button, PhotoImage, messagebox, filedialog, Canvas
import tkinter
import os
import sys
root= Tk()
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def openfile():
    global file
    file=tkinter.filedialog.askopenfilename(filetypes =[('PNG', '*.png'),('JPG','*.jpg')])
    if(len(file)>1):
        my_canvas.itemconfig(LocationError, text=file, fill="#6D76CD", font=("Aharoni",10))
        saveImg['text']='REOPEN'
        saveImg['bg']='#D0CECE'
        Common1=(os.path.basename(file).split('.')[0])
        path1=os.path.dirname(file)
    else:
        my_canvas.itemconfig(LocationError, text="Please Choose the Image", fill="#6D76CD", font=("Aharoni",10))
        saveImg['text']='OPEN'
        saveImg['bg']="#82CC6C"
def Check():
    if(saveImg['text']=='REOPEN'):
        change(file)
    else:
        messagebox.showerror("Error","Please open your image!")    
def change(file):
    try:
        img=Image.open(file)
        patht=resource_path0("Tesseract\Tesseract-OCR\Tesseract")#make sure you install the tesseract module inside the folder Tesseract.
        pytesseract.pytesseract.tesseract_cmd=patht
        result=pytesseract.image_to_string(img)
        outputfile=os.path.splitext(file)[0]+'_extracted'+".txt"
        if os.path.exists(outputfile):
            res=messagebox.askquestion("Replace?","Do you want to replace the old file?")
            if res=='yes':
                with open(outputfile,mode ='w') as file:
                    file.write(result)
                    messagebox.showinfo("Done!","Text extracted successfully!\nClick Ok to view the file")
                    os.startfile(outputfile)
            if res=='no':
                pass
        else:
            with open(outputfile,mode ='w') as file:
                    file.write(result)
                    messagebox.showinfo("Done!","Text extracted successfully!\nClick Ok to view the file")
                    os.startfile(outputfile)      
    except:
        messagebox.showerror("Error","Something went wrong!")
root.title("Textemage")
path0=resource_path0("icon.ico")
root.wm_iconbitmap(path0)
my_canvas=Canvas(root, width=501, height=353)
root.resizable(width=False, height=False)
path1=resource_path0("bg.png")
art=PhotoImage(file=path1)
my_canvas.create_image(0,0, image=art, anchor="nw")
my_canvas.pack(fill="both", expand=True)
root.columnconfigure(0,weight=1)
path2=resource_path0("headlabel.png")
label=PhotoImage(file=path2)
my_canvas.create_image(0,0, image=label, anchor="nw")
LocationError=my_canvas.create_text(250,60,text="Please Choose the Image",fill="#6D76CD", font=("Aharoni",10))
saveImg=Button(root, width=50,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="OPEN",relief="groove", command=openfile)
saveImg_window=my_canvas.create_window(250,90, window=saveImg)
path3=resource_path0("convertbutton.png")
Icon=PhotoImage(file=path3)
btn2=Button(image=Icon,borderwidth=0,bg="#15406B",highlightthickness=0,padx=0,pady=0,command=Check)
btn2_window=my_canvas.create_window(249,155, window=btn2)
my_canvas.create_text(170,300,text="This is a quick tool to extract text from images easily."
                    "\nJust open the image file and click the Convert button \nThen view your extracted text."
                    "\nDeveloper: Akash Bora (A.k.a Akascape)\nFor more info, visit our github page!",font=("Aharoni",10), fill="white")
root.mainloop()
#DEVELOPER= AKASH BORA(a.k.a Akascape)
#Version=1.0

