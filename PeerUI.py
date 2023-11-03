import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import filedialog
from PIL import ImageTk, Image
from PeerClass import Peer
import time
import copy

peer = None
closeApp = False
peerBtns = []

def RunPeer():
    global peer
    serverIP = serverIPEntry.get()
    serverPort = serverPortEntry.get()
    peerName = peerNameEntry.get()
    peerPort = peerPortEntry.get()
    if ((serverIP != "") and (serverPort != "") and (peerName != "") and (peerPort != "")):
        peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
        peer.startPeer()
        time.sleep(0.2)
        if (peer.endAllThread == True):
            peer = None
            return
        serverIPEntry.configure(state = "readonly")
        serverPortEntry.configure(state = "readonly")
        peerNameEntry.configure(state = "readonly")
        peerPortEntry.configure(state = "readonly")
        runPeerBtn.configure(state = "disable")
        l7 = tk.Label(master, text = peer.IP, font = ("Helvetica", 11))
        l7.place(x = 405, y = 95)
    else:
        print("Missing value !")

def updateListFile():
    global peer
    if (peer == None):
        return
    peer.reqListFile()
    time.sleep(0.05)
    listFile = peer.listFileServer
    listbox.delete(0, "end")
    for peerBtn in peerBtns:
        peerBtn.destroy()
    i = 0
    if (len(listFile) > 0):
        listbox.configure(state = "normal")
        for fname in listFile:
            listbox.insert(i, ' ' + fname)
            i += 1
    peer.listFileServer = []

def showListPeer(e):
    global peer
    try:
        str = listbox.get(listbox.curselection())
    except:
        return
    fname = str.replace(" ", "")
    peer.reqListPeer(fname)
    time.sleep(0.05)
    listPeer = copy.deepcopy(peer.listPeerServer)
    for peerBtn in peerBtns:
        peerBtn.destroy()
    if (len(listPeer) > 0):
        for i in range(len(listPeer)):
            peerBtn = ttk.Button(master, text = listPeer[i]["name"], style = "my.TButton", takefocus = 0, cursor = "hand2", padding = 2, 
                                 command = lambda IP = listPeer[i]["IP"], port = listPeer[i]["port"], filename = fname, name = listPeer[i]["name"]: 
                                 peer.requestFile(IP, port, filename, name))
            peerBtn.place(x = 460, y = i*40 + 190)
            peerBtns.append(peerBtn)
            if (peer.ID == listPeer[i]["ID"]):
                peerBtn.configure(state = "disable")
        peer.listPeerServer = []
    
def OpenFile():
    path = filedialog.askopenfilename()
    lnameEntry.configure(state="normal")  
    lnameEntry.delete(0, "end")
    lnameEntry.insert(0, path)
    lnameEntry.configure(state="readonly")
    pass

def publishFile():
    global peer
    if (peer == None):
        return
    lname = lnameEntry.get()
    fname = fnameEntry.get()
    if (lname != "" and fname != ""):
        peer.publFile(lname, fname)
    else:
        print("Missing value !")

def on_closing():
    global peer
    if ((peer != None) and (peer.endAllThread == False)):
        peer.endSystem()
    master.destroy()

master = tk.Tk()
master.title("Peer")
master.geometry("650x480")
master.resizable(0, 0)

#
appTitle = tk.Label(master, text = "File Sharing App", font=("Helvetica", 25, "bold"), width = 33, pady = 5, background ="#b8f89e", anchor="center")
appTitle.place(x = 0, y = 0)

#
l1 = tk.Label(master, text = "Sever:", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l3 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l1.place(x = 150, y = 60)
l2.place(x = 240, y = 60)
l3.place(x = 380, y = 60)
serverPortEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
serverIPEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 14)
serverPortEntry.place(x = 280, y = 60)
serverIPEntry.place(x = 405, y = 60)

#
l4 = tk.Label(master, text = "Name", font = ("Helvetica", 11))
l5 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l6 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l4.place(x = 20, y = 95)
l5.place(x = 240, y = 95)
l6.place(x = 380, y = 95)
peerNameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 15)
peerPortEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
peerNameEntry.place(x = 70, y = 95)
peerPortEntry.place(x = 280, y = 95)
style = ttk.Style()
style.configure("my.TButton", font=("Helvetica", 10))
img1 = Image.open("images/run.png")
img2 = Image.open("images/run_hover.png")
icon1 = ImageTk.PhotoImage(img1)
icon2 = ImageTk.PhotoImage(img2)
runPeerBtn = tk.Button(master, image = icon1, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunPeer)
runPeerBtn.bind("<Enter>", func = lambda e: runPeerBtn.config(image = icon2))
runPeerBtn.bind("<Leave>", func = lambda e: runPeerBtn.config(image = icon1))
runPeerBtn.place(x = 555, y = 70)

#
l8 = tk.Label(master, text = "List File:", font = ("Helvetica", 11))
l8.place(x = 20, y = 160)
img3 = Image.open("images/refresh.png")
img4 = Image.open("images/refresh_hover.png")
icon3 = ImageTk.PhotoImage(img3)
icon4 = ImageTk.PhotoImage(img4)
showListFile = tk.Button(master, image = icon3, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListFile)
showListFile.bind("<Enter>", func = lambda e: showListFile.config(image = icon4))
showListFile.bind("<Leave>", func = lambda e: showListFile.config(image = icon3))
showListFile.place(x = 316, y = 163)

fileArea = tk.Frame(master, background="white")
fileArea.place(x = 20, y = 185)
scroll = ttk.Scrollbar(fileArea)
listbox = tk.Listbox(fileArea, yscrollcommand = scroll.set, font = ("Helvetica", 14), width = 28, height = 7, 
                     selectbackground = "#b8f89e", selectforeground = "black", activestyle = "none", 
                     highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled")
listbox.bind("<<ListboxSelect>>", showListPeer)
scroll.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

l9 = tk.Label(master, text = "Users has the file", font = ("Helvetica", 11))
l9.place(x = 445, y = 158)

#
l10 = tk.Label(master, text = "Publish File:", font = ("Helvetica", 11))
l10.place(x = 20, y = 385)

l11 = tk.Label(master, text = "lname", font = ("Helvetica", 11))
l11.place(x = 130, y = 385)
lnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 42, state="readonly")
lnameEntry.place(x = 185, y = 385)
browseFileBtn = ttk.Button(master, text = "Browse", style = "my.TButton", width = 8, takefocus = 0, cursor = "hand2", command = OpenFile)
browseFileBtn.place(x = 550, y = 385)

l12 = tk.Label(master, text = "fname", font = ("Helvetica", 11))
l12.place(x = 130, y = 425)
fnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 19)
fnameEntry.place(x = 185, y = 425)
publishBtn = ttk.Button(master, text = "Publish", style = "my.TButton", width = 8, takefocus = 0, cursor = "hand2", command = publishFile)
publishBtn.place(x = 400, y = 425)

master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()