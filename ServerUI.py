import tkinter as tk
import tkinter.ttk as ttk 
from PIL import ImageTk, Image
from ServerClass import Server

server = None
listPeer = None

def RunServer():
    global server
    port = portEntry.get()
    if (port != ""):
        server = Server(int(port))
        server.startServer()
        l3 = tk.Label(master, text = server.IP, font = ("Helvetica", 11))
        l3.place(x = 190, y = 60)
        portEntry.configure(state = "readonly")
        runServerBtn.configure(state = "disable")
    else:
        print("Missing value !")

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
    if (server != None):
        server.endSystem()
    master.destroy()

master = tk.Tk()
master.title("Server")
master.geometry("650x440")
master.resizable(0, 0)

# 
appTitle = tk.Label(master, text = "File Sharing App", font=("Helvetica", 25, "bold"), width = 33, background ="#b8f89e", anchor="center")
appTitle.place(x = 0, y = 0)

style = ttk.Style()
style.configure("my.TButton", font=("Helvetica", 10))
img1 = Image.open("images/run.png")
img2 = Image.open("images/run_hover.png")
icon1 = ImageTk.PhotoImage(img1)
icon2 = ImageTk.PhotoImage(img2)
runServerBtn = tk.Button(master, image = icon1, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunServer)
runServerBtn.bind("<Enter>", func = lambda e: runServerBtn.config(image = icon2))
runServerBtn.bind("<Leave>", func = lambda e: runServerBtn.config(image = icon1))
runServerBtn.place(x = 427, y = 58)

l1 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l1.place(x = 20, y = 60)
l2.place(x = 165, y = 60)

portEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
portEntry.place(x = 60, y = 60)

#
l4 = tk.Label(master, text = "Users:", font = ("Helvetica", 11))
l4.place(x = 20, y = 125)
img3 = Image.open("images/refresh.png")
img4 = Image.open("images/refresh_hover.png")
icon3 = ImageTk.PhotoImage(img3)
icon4 = ImageTk.PhotoImage(img4)
showListPeer = tk.Button(master, image = icon3, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListUser)
showListPeer.bind("<Enter>", func = lambda e: showListPeer.config(image = icon4))
showListPeer.bind("<Leave>", func = lambda e: showListPeer.config(image = icon3))
showListPeer.place(x = 249, y = 128)

userArea = tk.Frame(master, background="white")
userArea.place(x = 20, y = 150)
scroll1 = ttk.Scrollbar(userArea)
listbox = tk.Listbox(userArea, yscrollcommand = scroll1.set, font = ("Helvetica", 14), width = 22, height = 8, 
                    selectbackground = "#b8f89e", selectforeground = "black", activestyle = "none", 
                    highlightthickness = 0, borderwidth=0, selectmode = "single", cursor = "hand2", state = "disabled")
listbox.bind("<<ListboxSelect>>", showPeerInfo)
scroll1.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

#
l5 = tk.Label(master, text = "Infomation", font = ("Helvetica", 11))
l5.place(x = 425, y = 125)

infoArea = tk.Frame(master, background = "white")
infoArea.place(x = 320, y = 150)
scroll2 = ttk.Scrollbar(infoArea)
info = tk.Text(infoArea, font=("Helvetica", 14), yscrollcommand = scroll2.set, state = "disable", width = 25, height = 11, borderwidth = 0)
scroll2.pack(side = "right", fill = "y")
info.pack(side = "left", padx = 5, pady = 5)

master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()