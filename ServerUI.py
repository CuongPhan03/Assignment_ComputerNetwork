import tkinter as tk
import tkinter.ttk as ttk 
from ServerClass import Server

server = None
listPeer = [{"name": "fdgfdg", "IP":"123.22.4.14", "port":213, "connection": "conn", "listFile":["asf", "ae"]},
            {"name": "augsu", "IP":"123.22.4.14", "port":213, "connection": "conn", "listFile":["dfgd", "ahte"]}]

def RunServer():
    global server
    server = Server()
    server.startServer()
    l3 = tk.Label(master, text = server.PORT, font = ("Helvetica", 11))
    l4 = tk.Label(master, text = server.IP, font = ("Helvetica", 11))
    l3.place(x = 60, y = 60)
    l4.place(x = 190, y = 60)
    runServerBtn.configure(state = 'disable')

def updateListUser():
    global server
    if (server == None):
        return
    if (listPeer != None):
        listbox.delete(0, "end")
        info.delete(0, "end")
        #listPeer = server.getListPeer()
        i = 0
        for peer in listPeer:
            listbox.insert(i, ' ' + peer["name"])
            i += 1

def showPeerInfo(e):
    global server
    index = listbox.curselection()[0]
    peer = listPeer[index]
    #server.getPeerInfo(peer["connection"])
    info.configure(state = "normal")
    info.delete(1.0, "end")
    info.insert("end", " name:    " + peer["name"] + "\n")
    info.insert("end", " port:       " + str(peer["port"]) + "\n")
    info.insert("end", " IP:         " + peer["IP"] + "\n")
    info.insert("end", " List file:\n")
    for fname in peer["listFile"]:
        info.insert("end", "      " + fname +"\n")

    info.configure(state = "disable")


def on_closing():
    global server
    if (server != None):
        server.endSystem()
    master.destroy()
    

master = tk.Tk()
master.title('Server')
master.geometry("650x450")
master.resizable(0, 0)

# 
appTitle = tk.Label(master, text = "File Sharing App", font=("Helvetica", 25, "bold"), width = 33, background ="#b8f89e", anchor="center")
appTitle.place(x = 0, y = 0)

style = ttk.Style()
style.configure('my.TButton', font=('Helvetica', 10))
runServerBtn = ttk.Button(master, text = "Run", style='my.TButton', width = 8, takefocus = 0, command = RunServer)
runServerBtn.place(x = 433, y = 58)

l1 = tk.Label(master, text = "Port:", font = ("Helvetica", 11))
l2 = tk.Label(master, text = "IP:", font = ("Helvetica", 11))
l1.place(x = 20, y = 60)
l2.place(x = 165, y = 60)

#
l5 = tk.Label(master, text = "Users:", font = ("Helvetica", 11))
l5.place(x = 20, y = 130)
showListFile = ttk.Button(master, text = "Refresh", style = 'my.TButton', takefocus = 0, command = updateListUser)
showListFile.place(x = 188, y = 125)

userArea = tk.Frame(master, background="white")
userArea.place(x = 20, y = 155)
scroll1 = ttk.Scrollbar(userArea)
listbox = tk.Listbox(userArea, yscrollcommand = scroll1.set, font = ("Helvetica", 14), width = 22, height = 8, selectbackground='#b8f89e', selectforeground='black', activestyle='none', highlightthickness=0, borderwidth=0, selectmode = "single")
listbox.bind("<<ListboxSelect>>", showPeerInfo)
scroll1.pack(side = "right", fill = "y")
listbox.pack(side = "left", padx = 5, pady = 5)

#
l5 = tk.Label(master, text = "Infomation", font = ("Helvetica", 11))
l5.place(x = 430, y = 130)

infoArea = tk.Frame(master, background="white")
infoArea.place(x = 320, y = 155)
scroll2 = ttk.Scrollbar(infoArea)
info = tk.Text(infoArea, font=("Helvetica", 14), yscrollcommand = scroll2.set, state = "disable", width = 25, height = 11, borderwidth = 0)
scroll2.pack(side = "right", fill = "y")
info.pack(side = "left", padx = 5, pady = 5)

master.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()