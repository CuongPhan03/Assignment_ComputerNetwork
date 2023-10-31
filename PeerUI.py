from tkinter import * 
from tkinter.ttk import *
from PeerClass import Peer
from tkinter import filedialog
from threading import Thread
import copy

peer = None
flag = True
friendList = None
friends = []

def updateFriendList():
    pass
    '''global peer
    global friendList
    global friends
    if (peer != None):
        friendList = peer.listPeers.split(';')
    print(friendList)
    if (len(friends) != 0):
        friends = []
    if (friendList != None):
        for i in range(0,len(friendList) - 1):
            friend = friendList[i].split(":")
            friends.append(copy.deepcopy(friend))
        for i in range(0,len(friends)):
            Button(master, text=friends[i][0],command = lambda b=friends[i][1]: ConnectToPeer(b)).place(x=500,y = (i + 1)*50 + 100)'''

def RunPeer():
    global flag
    global peer
    print("Starting Server")
    if (flag == False):
        return
    if (nameEntry.get() != "" and portEntry.get() != "" and flag):
        try:
            nameEntry.configure(state='readonly')
            portEntry.configure(state='readonly')
            peer = Peer(nameEntry.get(), int(portEntry.get()),text)
            print("Create Server")
            peer.startPeer()
            print("Run Server")
            flag = False
        except Exception:
            print("Fail Server")
            return
        
def ConnectToPeer(IP, port):
    global flag
    global peer

    print("Starting client")
    if (flag == True or peer == None):
        return
    try:
        peer.connectToPeer(IP, port)
        print("Run client")
    except Exception:
        print("Fail client")
        return
        
def OpenFile():
    filepath = filedialog.askopenfilename()
    fileBox.configure(state='normal')  
    fileBox.delete(0,END)
    fileBox.insert(0,filepath)
    fileBox.configure(state='readonly')
    pass

def SendFile():
    global peer
    if (peer == None):
        return
    try:
        if (fileBox.get() != ""):
            peer.sendFile(fileBox.get())
    except:
        return

def on_closing():
    global peer
    global flag
    flag = False
    if (peer != None):
        peer.endSystem()
    master.destroy()
    
master = Tk()
master.title('File Sharing Application')
master.geometry("600x500")
master.resizable(0, 0)

# Server
l1 = Label(master, text = "Name:",width=10)
l2 = Label(master, text = "Port:",width=10)
l1.place(x = 10, y = 10)
l2.place(x = 280, y = 10)
nameEntry = Entry(master,width=30)
portEntry = Entry(master,width=10)
nameEntry.place(x=60,y=10)
portEntry.place(x=320,y=10)
runServerButton = Button(master,text="Run",command=RunPeer)
runServerButton.place(x=400,y = 10)

# Create an object of tkinter ImageTk
appTitle = Label(master, text = "File Sharing Application",width=30, font=("Helvetica", 25,"bold"),background ="#53f5f0", anchor="center")
appTitle.place(x = 25, y = 45)

chatArea = Frame(master,width = 100,height  = 300)
scroll=Scrollbar(chatArea)
text=Text(chatArea, font=("Georgia, 12"), yscrollcommand=scroll.set,width= 50, height=17)
chatArea.place(x=20,y = 100)
scroll.pack(side=RIGHT)
text.pack(side=LEFT)
text.configure(state='disable')

# send file
l4 = Label(master, text = "File:",width=10)
l4.place(x = 20, y = 420)
fileBox = Entry(master,width=35)
fileBox.place(x=80,y=420)
fileBox.configure(state='readonly')
addFileButton = Button(master,text="Browser",command=OpenFile)
addFileButton.place(x=300,y = 420)
sendFileButton = Button(master,text="Send",command=SendFile)
sendFileButton.place(x=400,y = 420)

#Online user
showOnlineUser = Button(master,text="Show online user",command=updateFriendList)
showOnlineUser.place(x=490,y = 100)

master.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()