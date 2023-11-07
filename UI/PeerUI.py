import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import ImageTk, Image
from PeerClass import Peer
import time
import copy
import os

peer = None
closeApp = False
btnFrames = []
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
        while (peer.endAllThread == None):
            time.sleep(0.01)
        if (peer.endAllThread == True):
            peer = None
            return
        while (peer.ID == None):
            time.sleep(0.01)
            if (peer.endAllThread == True):
               return
        l7 = tk.Label(master, text = peer.IP, font = ("Helvetica", 11))
        l7.place(x = 475, y = 102)
        serverIPEntry.configure(state = "readonly")
        serverPortEntry.configure(state = "readonly")
        peerNameEntry.configure(state = "readonly")
        peerPortEntry.configure(state = "readonly")
        runPeerBtn.configure(state = "disable", cursor = "arrow")
        runPeerBtn.bind("<Enter>", func = lambda e: runPeerBtn.config(image = icon1))
    else:
        showwarning("Warning", "  Missing value !  ")

def updateListFile():
    global peer
    if (peer == None):
        return
    peer.reqListFile()
    time.sleep(0.1)
    listFile = peer.listFileServer
    listbox.delete(0, "end")
    for i in range(len(peerBtns)):
        peerBtns[i].destroy()
        btnFrames[i].destroy()
    if (len(listFile) > 0):
        listbox.configure(state = "normal") 
        for i in range(len(listFile)):
            listbox.insert(i, ' ' + listFile[i])
    peer.listFileServer = []

def showListPeer(e):
    global peer
    try:
        str = listbox.get(listbox.curselection())
    except:
        return
    fname = str.replace(" ", "")
    peer.reqListPeer(fname)
    time.sleep(0.1)
    listPeer = copy.deepcopy(peer.listPeerServer)
    for i in range(len(peerBtns)):
        peerBtns[i].destroy()
        btnFrames[i].destroy()
    if (len(listPeer) > 0):
        for i in range(len(listPeer)):
            btnFrame = tk.Frame(master, highlightbackground = "#ff904f", highlightthickness = 2)
            btnFrame.place(x = 530, y = i*45 + 200)
            peerBtn = tk.Button(btnFrame, text = listPeer[i]["name"], font = "Helvetica 11 bold", takefocus = 0,  relief = "sunken", cursor = "hand2", width = 8, pady = 1,
                                border = 0, bg = "#ff904f", fg = "white", disabledforeground = "#eee", activeforeground = "#ff904f", activebackground = "#eee",
                                command = lambda IP = listPeer[i]["IP"], port = listPeer[i]["port"], filename = fname, name = listPeer[i]["name"]: 
                                peer.requestFile(IP, port, filename, name))
            if (peer.ID == listPeer[i]["ID"]):
                peerBtn.configure(state = "disable", cursor = "arrow", bg = "#ffb488")
                btnFrame.configure(highlightbackground = "#ffb488")
            else:
                peerBtn.bind("<Enter>", func = lambda e, btn = peerBtn: btn.config(bg = "white", fg = "#ff904f"))
                peerBtn.bind("<Leave>", func = lambda e, btn = peerBtn: btn.config(bg = "#ff904f", fg = "white"))
            peerBtn.pack()
            btnFrames.append(btnFrame)
            peerBtns.append(peerBtn)
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
        showwarning("Warning", "  Missing value !  ")

def on_closing():
    global peer
    print("Peer off.")
    if ((peer != None) and (peer.endAllThread == False)):
        peer.endSystem()
    master.destroy()

master = tk.Tk()
master.title("Peer")
master.geometry("720x503")
master.tk_setPalette(background='#f8f8f8')
master.resizable(0, 0)

#
appTitle = tk.Label(master, text = "FILE SHARING APP", font=("Helvetica", 23, "bold"), width = 38, pady = 5, bg ="#ff904f", fg = "white", anchor="center")
appTitle.place(x = 0, y = 0)

#
label1 = tk.Label(master, text = "Register", font=("Helvetica", 11, "bold"), width = 8, height = 5, bg ="#3399ff", fg = "white", anchor="center")
label2 = tk.Label(master, text = "Download", font=("Helvetica", 11, "bold"), width = 8, height = 14, bg ="#3399ff", fg = "white", anchor="center")
label3 = tk.Label(master, text = "Publish", font=("Helvetica", 11, "bold"), width = 8, height = 6, bg ="#3399ff", fg = "white", anchor="center")
label1.place(x = 0, y = 50)
label2.place(x = 0, y = 140)
label3.place(x = 0, y = 390)
line1 = tk.Frame(master, highlightbackground = "#ddd", highlightthickness = 1, width = 720)
line2 = tk.Frame(master, highlightbackground = "#ddd", highlightthickness = 1, width = 720)
line1.place(x = 0, y = 145)
line2.place(x = 0, y = 390)

#
l1 = tk.Label(master, text = "Sever:", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l3 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l1.place(x = 220, y = 65)
l2.place(x = 310, y = 65)
l3.place(x = 450, y = 65)
serverPortEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
serverIPEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 14)
serverPortEntry.place(x = 350, y = 65)
serverIPEntry.place(x = 475, y = 65)

l4 = tk.Label(master, text = "Name", font = ("Helvetica", 11))
l5 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l6 = tk.Label(master, text = "IP", font = ("Helvetica", 11))
l4.place(x = 90, y = 102)
l5.place(x = 310, y = 102)
l6.place(x = 450, y = 102)
peerNameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 15)
peerPortEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
peerNameEntry.place(x = 140, y = 102)
peerPortEntry.place(x = 350, y = 102)
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
img1 = Image.open(path + "\images\\run.png")
img2 = Image.open(path + "\images\\run_hover.png")
icon1 = ImageTk.PhotoImage(img1)
icon2 = ImageTk.PhotoImage(img2)
runPeerBtn = tk.Button(master, image = icon1, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunPeer)
runPeerBtn.bind("<Enter>", func = lambda e: runPeerBtn.config(image = icon2))
runPeerBtn.bind("<Leave>", func = lambda e: runPeerBtn.config(image = icon1))
runPeerBtn.place(x = 625, y = 82)

#
l8 = tk.Label(master, text = "List file", font = ("Helvetica", 11))
l8.place(x = 90, y = 170)
img3 = Image.open(path + "\images\\refresh.png")
img4 = Image.open(path + "\images\\refresh_hover.png")
icon3 = ImageTk.PhotoImage(img3)
icon4 = ImageTk.PhotoImage(img4)
showListFile = tk.Button(master, image = icon3, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListFile)
showListFile.bind("<Enter>", func = lambda e: showListFile.config(image = icon4))
showListFile.bind("<Leave>", func = lambda e: showListFile.config(image = icon3))
showListFile.place(x = 388, y = 172)

fileArea = tk.Frame(master, background="white")
fileArea.place(x = 90, y = 195)
scroll = ttk.Scrollbar(fileArea)
listbox = tk.Listbox(fileArea, yscrollcommand = scroll.set, font = ("Helvetica", 14), width = 28, height = 7, 
                     bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                     highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled")
listbox.bind("<<ListboxSelect>>", showListPeer)
scroll.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

l9 = tk.Label(master, text = "Users has the file", font = ("Helvetica", 11))
l9.place(x = 515, y = 166)

#
l11 = tk.Label(master, text = "lname", font = ("Helvetica", 11))
l11.place(x = 90, y = 410)
lnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 45, state = "readonly")
lnameEntry.place(x = 145, y = 410)
style = ttk.Style()
style.configure("my.TButton", font = ("Helvetica", 10))
browseFileBtn = ttk.Button(master, text = "Browse", style = "my.TButton", width = 8, takefocus = 0, cursor = "hand2", command = OpenFile)
browseFileBtn.place(x = 550, y = 410)

l12 = tk.Label(master, text = "fname", font = ("Helvetica", 11))
l12.place(x = 90, y = 455)
fnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 19)
fnameEntry.place(x = 145, y = 455)

img5 = Image.open(path + "\images\publish.png")
img6 = Image.open(path + "\images\publish_hover.png")
icon5 = ImageTk.PhotoImage(img5)
icon6 = ImageTk.PhotoImage(img6)
publishBtn = tk.Button(master, image = icon5, border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = publishFile)
publishBtn.bind("<Enter>", func = lambda e: publishBtn.config(image = icon6))
publishBtn.bind("<Leave>", func = lambda e: publishBtn.config(image = icon5))
publishBtn.place(x = 380, y = 453)

#
master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()