import tkinter as tk
import tkinter.ttk as ttk 
from PeerClass import Peer

peer = None
closeApp = False
listFile = ["fbdbjfsd", "asfwefe"]
peerBtns = []

def RunPeer():
    global peer
    name = nameEntry.get()
    port = portEntry.get()
    if (name != "" and port != ""):
        try:
            print("Starting Peer...")
            nameEntry.configure(state = 'readonly')
            portEntry.configure(state = 'readonly')
            runPeerBtn.configure(state = 'disable')
            peer = Peer(name, int(port))
            peer.startPeer()
            l4 = tk.Label(master, text = peer.IP, font = ("Helvetica", 11))
            l4.place(x = 450, y = 61)
            updateListFile()
        except:
            return
    else:
        print("Missing value !")

def updateListFile():
    global peer
    global listFile
    if (peer == None):
        return
    if (listFile != None):
        listbox.delete(0, "end")
        for peerBtn in peerBtns:
            peerBtn.destroy()
        #listFile = peer.getListFile()
        i = 0
        for fname in listFile:
            listbox.insert(i, ' ' + fname)
            i += 1

def showListPeer(e):
    str = listbox.get(listbox.curselection())
    fname = str.replace(" ", "")
    print(fname)
    #listPeer = peer.getListPeer(fname)
    listPeer = [{"name":"abc", "IP": "10.10.01.01", "port": 1234}, {"name":"def", "IP": "192.127.10.00", "port": 5678}]
    for peerBtn in peerBtns:
        peerBtn.destroy()
    i = 0
    for peerData in listPeer:
        name = peerData["name"]
        IP = peerData["IP"]
        port = peerData["port"]
        peerBtn = ttk.Button(master, text = name, style = 'my.TButton', takefocus = 0, command = lambda: requestFile(IP, port, fname))
        peerBtn.place(x = 460, y = (i + 1)*40 + 120)
        peerBtns.append(peerBtn)
        i += 1

def requestFile(IP, port, fname):
    try:
        peer.requestFile(IP, port, fname)
    except:
        return
    
def publishFile():
    global peer
    if (peer == None):
        return
    lname = lnameEntry.get()
    fname = fnameEntry.get()
    if (lname != "" and fname != ""):
        peer.publishFile(lname, fname)
    else:
        print("Missing value !")

def on_closing():
    global peer
    if (peer != None):
        peer.endSystem()
    master.destroy()
    

master = tk.Tk()
master.title('Peer')
master.geometry("650x450")
master.resizable(0, 0)

#
appTitle = tk.Label(master, text = "File Sharing App", font=("Helvetica", 25, "bold"), width = 33, background ="#b8f89e", anchor="center")
appTitle.place(x = 0, y = 0)

l1 = tk.Label(master, text = "Name", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "Port", font = ("Helvetica", 11))
l3 = tk.Label(master, text = "IP:", font = ("Helvetica", 11))
l1.place(x = 20, y = 60)
l2.place(x = 280, y = 60)
l3.place(x = 420, y = 60)
nameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 20)
portEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 7)
nameEntry.place(x = 70, y = 60)
portEntry.place(x = 320, y = 60)
style = ttk.Style()
style.configure('my.TButton', font=('Helvetica', 10))
runPeerBtn = ttk.Button(master, text = "Run", style='my.TButton', width = 8, takefocus = 0, command = RunPeer)
runPeerBtn.place(x = 560, y = 58)

l5 = tk.Label(master, text = "List File:", font = ("Helvetica", 11))
l5.place(x = 20, y = 130)
showListFile = ttk.Button(master, text = "Refresh", style = 'my.TButton', takefocus = 0, command = updateListFile)
showListFile.place(x = 275, y = 125)

fileArea = tk.Frame(master, background="white")
fileArea.place(x = 20, y = 155)
scroll = ttk.Scrollbar(fileArea)
listbox = tk.Listbox(fileArea, yscrollcommand = scroll.set, font = ("Helvetica", 14), width = 30, height = 7, selectbackground='#b8f89e', selectforeground='black', activestyle='none', highlightthickness=0, borderwidth=0, selectmode = "single")
listbox.bind("<<ListboxSelect>>", showListPeer)
scroll.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

l6 = tk.Label(master, text = "Users has the file", font = ("Helvetica", 11))
l6.place(x = 450, y = 127)

#
l7 = tk.Label(master, text = "Publish File:", font = ("Helvetica", 11))
l7.place(x = 20, y = 365)
l8 = tk.Label(master, text = "lname", font = ("Helvetica", 11))
l9 = tk.Label(master, text = "fname", font = ("Helvetica", 11))
l8.place(x = 20, y = 390)
l9.place(x = 230, y = 390)
lnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 15)
fnameEntry = ttk.Entry(master, font = ("Helvetica", 11), width = 15)
lnameEntry.place(x = 70, y = 390)
fnameEntry.place(x = 280, y = 390)
publishBtn = ttk.Button(master, text = "Publish", style='my.TButton', width = 8, takefocus = 0, command = publishFile)
publishBtn.place(x = 500, y = 388)

master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()