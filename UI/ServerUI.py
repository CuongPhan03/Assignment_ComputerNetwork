import tkinter as tk
import tkinter.ttk as ttk 
from tkinter.messagebox import showerror, showwarning
from PIL import ImageTk, Image
from ServerClass import Server
import time

server = None
listPeer = None

def RunServer():
    global server
    port = portEntry.get()
    if (port != ""):
        server = Server(int(port))
        server.startServer()
        while (server.endAllThread == None):
           time.sleep(0.01)
        if (server.endAllThread == True):
           server = None
           showerror("Error", "  Fail binding address !")
           return
        l3 = tk.Label(master, text = server.IP, font = ("Helvetica", 11))
        l3.place(x = 255, y = 70)
        portEntry.configure(state = "readonly")
        runServerBtn.configure(state = "disable", cursor = "arrow")
        runServerBtn.bind("<Enter>", func = lambda e: runServerBtn.config(image = icon1))
    else:
        showwarning("Warning", "  Missing value !  ")

def updateListUser():
    global server
    global listPeer
    if (server == None):
        return
    listPeer = server.jsonPeerDatas
    listbox.delete(0, "end")
    info.configure(state = "normal")
    info.delete(1.0, "end")
    info.configure(state = "disable")
    if (listPeer != None and len(listPeer) > 0):
        listbox.configure(state = "normal")
        i = 0
        for peer in listPeer:
            listbox.insert(i, ' ' + peer["name"])
            i += 1

def showPeerInfo(e):
    global server
    global listPeer
    try:
        index = listbox.curselection()[0]
    except:
        return
    peer = listPeer[index]
    info.configure(state = "normal")
    info.delete(1.0, "end")
    info.insert("end", " name:    " + peer["name"] + "\n")
    info.insert("end", " port:      " + str(peer["port"]) + "\n")
    info.insert("end", " IP:         " + peer["IP"] + "\n")
    info.insert("end", " List file:\n")
    if (peer["listFile"] != None):
        for fname in peer["listFile"]:
            info.insert("end", "      " + fname +"\n")
    info.configure(state = "disable")

def on_closing():
    global server
    print("Server off.")
    if ((server != None) and (server.endAllThread == False)):
        server.endSystem()
    master.destroy()

master = tk.Tk()
master.title("Server")
master.geometry("709x440")
master.tk_setPalette(background='#f8f8f8')
master.resizable(0, 0)

# 
appTitle = tk.Label(master, text = "FILE SHARING APP", font=("Helvetica", 23, "bold"), width = 37, pady = 5, bg ="#ff904f", fg = "white", anchor="center")
appTitle.place(x = 0, y = 0)

label1 = tk.Label(master, text = "Bind\nAddress", font=("Helvetica", 11, "bold"), width = 7, height = 3, bg = "#3399ff", fg = "white", anchor="center")
label2 = tk.Label(master, text = "User\nData", font=("Helvetica", 11, "bold"), width = 7, height = 18, bg = "#3399ff", fg = "white", anchor="center")
label1.place(x = 0, y = 50)
label2.place(x = 0, y = 110)
line1 = tk.Frame(master, highlightbackground = "#ddd", highlightthickness = 1, width = 720)
line1.place(x = 0, y = 115)

l1 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l1.place(x = 85, y = 70)
l2.place(x = 230, y = 70)

portEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
portEntry.place(x = 125, y = 70)

style = ttk.Style()
style.configure("my.TButton", font=("Helvetica", 10))
img1 = Image.open("D:\Documents\CƠ SỞ NGÀNH\Mạng máy tính\Btl\Assignment1\Code\images\\run.png")
img2 = Image.open("D:\Documents\CƠ SỞ NGÀNH\Mạng máy tính\Btl\Assignment1\Code\images\\run_hover.png")
icon1 = ImageTk.PhotoImage(img1)
icon2 = ImageTk.PhotoImage(img2)
runServerBtn = tk.Button(master, image = icon1, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunServer)
runServerBtn.bind("<Enter>", func = lambda e: runServerBtn.config(image = icon2))
runServerBtn.bind("<Leave>", func = lambda e: runServerBtn.config(image = icon1))
runServerBtn.place(x = 492, y = 63)

#
l4 = tk.Label(master, text = "Users", font = ("Helvetica", 11))
l4.place(x = 85, y = 135)
img3 = Image.open("D:\Documents\CƠ SỞ NGÀNH\Mạng máy tính\Btl\Assignment1\Code\images\\refresh.png")
img4 = Image.open("D:\Documents\CƠ SỞ NGÀNH\Mạng máy tính\Btl\Assignment1\Code\images\\refresh_hover.png")
icon3 = ImageTk.PhotoImage(img3)
icon4 = ImageTk.PhotoImage(img4)
showListPeer = tk.Button(master, image = icon3, border = 0, borderwidth = 0, bg = "#f8f8f8", relief = "sunken", cursor = "hand2", command = updateListUser)
showListPeer.bind("<Enter>", func = lambda e: showListPeer.config(image = icon4))
showListPeer.bind("<Leave>", func = lambda e: showListPeer.config(image = icon3))
showListPeer.place(x = 317, y = 138)

userArea = tk.Frame(master, background = "white")
userArea.place(x = 85, y = 160)
scroll1 = ttk.Scrollbar(userArea)
listbox = tk.Listbox(userArea, yscrollcommand = scroll1.set, font = ("Helvetica", 14), width = 22, height = 8, 
                    bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                    highlightthickness = 0, borderwidth=0, selectmode = "single", cursor = "hand2", state = "disabled")
listbox.bind("<<ListboxSelect>>", showPeerInfo)
scroll1.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

#
l5 = tk.Label(master, text = "Infomation", font = ("Helvetica", 11))
l5.place(x = 490, y = 134)

infoArea = tk.Frame(master, background = "white")
infoArea.place(x = 380, y = 160)

scroll2 = ttk.Scrollbar(infoArea)
info = tk.Text(infoArea, font=("Helvetica", 14), yscrollcommand = scroll2.set, state = "disable", width = 25, height = 11, bg = "white", borderwidth = 0)
scroll2.configure(command = info.yview)
scroll2.pack(side = "right", fill = "y")
info.pack(side = "left", padx = 5, pady = 5)

master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()