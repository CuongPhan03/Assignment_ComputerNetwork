from threading import Thread
from tkinter.messagebox import showerror, showwarning, showinfo, askquestion
import socket
import json
import os
import time

class Peer:
    IP = socket.gethostbyname(socket.gethostname()) 
    # port lay tu input
    FORMAT = "utf8"
    SIZE = 1024
    PeerSocket = None
    ServerConnection = None
    connectSocket = None
    listFile = {"lname": [], "fname": []}
    listFileServer = []  # [fname1, fname2]
    listPeerServer = []  # [{"name": , "ID": ,"IP": , "port":}, ]
    listSocket = []
    allThreads = []
    endAllThread = None
    
    def __init__(self, serverIP, severPort ,name, port):
        self.ServerIP = serverIP
        self.ServerPort = severPort
        self.name = name
        self.PORT = port
        self.ID = None
    
    def startPeer(self):
        register = Thread(target = self.runPeer)
        self.allThreads.append(register)
        register.start()

    def runPeer(self):
        try: 
            self.ServerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ServerConnection.connect((self.ServerIP, self.ServerPort))
        except:
            self.endSystem()
            showerror("Error", "  Fail connection !   ")
            return
        try:
            self.PeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.PeerSocket.bind((self.IP, self.PORT))
        except:
            self.endSystem()
            showerror("Error", "  Unavailable address ! ")
            return
        self.endAllThread = False
        # register address
        self.listSocket.append(self.ServerConnection)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.PORT, "action": "register", "listFile": []})
        self.ServerConnection.send(data.encode(self.FORMAT))

        # listen message
        self.listSocket.append(self.PeerSocket)
        self.PeerSocket.listen()
        receiver1 = Thread(target = self.listenServer)
        receiver2 = Thread(target = self.listenPeerRes)
        self.allThreads.append(receiver1)
        self.allThreads.append(receiver2)
        receiver1.start()
        receiver2.start()
        while (self.endAllThread == False):
            try:
                conn, addr = self.PeerSocket.accept()
            except:
                break
            if (conn):
                receiver3 = Thread(target = self.listenPeerReq, args=(conn,))
                self.allThreads.append(receiver3)
                receiver3.start()

    def listenServer(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.ServerConnection.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "resRegister"):
                    print("Peer is running...")
                    self.ID = jsonData["ID"]
                elif (jsonData["action"] == "resListFile"):
                    # jsonData = {"action": "resListFile", "listFile": [fname, ]}
                    self.listFileServer = []
                    for fname in jsonData["listFile"]:
                        self.listFileServer.append(fname)
                elif (jsonData["action"] == "resListPeer"):
                    # jsonData = {"action": "resListPeer", "listPeer": [{"name": , "ID": , "IP": , "port":}, ]}
                    self.listPeerServer = []
                    for peerData in jsonData["listPeer"]:
                        self.listPeerServer.append(peerData)
            except:
                continue

    def listenPeerReq(self, connection):
        while(self.endAllThread == False):
            try:
                receiveData = connection.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "reqFile"):
                    # jsonData = {"name": , "action": "reqFile", "fname": }
                    peerName = jsonData["name"]
                    fname = jsonData["fname"]
                    print(jsonData["name"] + " requests " + fname)
                    sender = Thread(target = self.sendFile, args=(connection, fname, peerName))
                    self.allThreads.append(sender)
                    sender.start()
            except:
                continue

    def listenPeerRes(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.connectSocket.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "resFile"):
                    # jsonData = {"name": , "action": "resFile", "status": , "fname": }
                    if (jsonData["status"] == "yes"):
                        self.receiveFile(jsonData["fname"], jsonData["name"])
                    elif (jsonData["status"] == "no"):
                        showerror("Error", "  " + jsonData["name"] + " refused to send '" + jsonData["fname"] + "' !  ")
                    else:
                        showerror("Error", "  File not found !  ")
                    self.connectSocket.close()
                    self.connectSocket = None
            except:
                continue

    def sendFile(self, connection, fname, peerName):
        i = 0
        lname = None
        for filename in self.listFile["fname"]:
            if (filename == fname):
                lname = self.listFile["lname"][i]
                break
            i += 1
        if os.path.isfile(lname):
            res = askquestion("Request", peerName + " requests " + fname)
            if res == 'yes':
                mess = json.dumps({"name": self.name , "action": "resFile", "status": "yes", "fname": fname})
                connection.send(mess.encode(self.FORMAT))
                time.sleep(0.1)
                with open(lname, "rb") as file:
                    while True:
                        try:
                            data = file.read(self.SIZE)
                            if (not data):
                                break
                            print("Sending " + fname + " to " + peerName + "...")
                            connection.send(data)
                        except:
                            continue
                    print("Done Sending.")
            else:
                mess = json.dumps({"name": self.name , "action": "resFile", "status": "no", "fname": fname})
                connection.send(mess.encode(self.FORMAT))        
        else:
            showerror("Error", "  File not found !  ")
            mess = json.dumps({"name": self.name , "action": "resFile", "status": "notfound", "fname": fname})
            connection.send(mess.encode(self.FORMAT))

    def receiveFile(self, fname, peerName):
        self.connectSocket.settimeout(0.7)
        if not os.path.isdir(self.name): 
            os.mkdir(self.name)
        path = os.path.join(self.name, fname)
        with open(path, 'wb') as file:
            while True:
                try:
                    print("Receiving " + fname + " from " + peerName + "...")
                    data = self.connectSocket.recv(self.SIZE)
                    file.write(data)
                except socket.timeout:
                    break
            file.close()
            print("Done Receiving.")
            showinfo("Infomation", "  Done Receiving.  ") 
        
    def reqListFile(self):
        sender = Thread(target = self.requestListFile)
        self.allThreads.append(sender)
        sender.start()
        
    def requestListFile(self):
        mess = json.dumps({"name": self.name, "action": "reqListFile"})
        self.ServerConnection.send(mess.encode(self.FORMAT))

    def reqListPeer(self, fname):
        sender = Thread(target = self.requestListPeer, args = (fname,))
        self.allThreads.append(sender)
        sender.start()
        
    def requestListPeer(self, fname):
        mess = json.dumps({"action": "reqListPeer", "fname": fname})
        self.ServerConnection.send(mess.encode(self.FORMAT))

    def requestFile(self, IP, port, fname, peerName):
        if (self.connectSocket != None):
            showwarning("Warning", "  Busy !   ")
            return
        path = os.path.join(self.name, fname)
        if os.path.isfile(path):
            showwarning("Warning", "  File existed in local ! ")
            return
        connect = Thread(target = self.startConnection, args = (IP, port, fname))
        self.allThreads.append(connect)
        connect.start()

    def startConnection(self, IP, port, fname):
        self.connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSocket.connect((IP, port))
        self.listSocket.append(self.connectSocket)
        mess = json.dumps({"name": self.name, "action": "reqFile", "fname": fname})
        self.connectSocket.send(mess.encode(self.FORMAT))

    def publFile(self, lname, fname):
        for name in self.listFile["lname"]:
            if (lname == name):
                showwarning("Warning", "  File published before ! ")
                return
        for name in self.listFile["fname"]:
            if (fname == name):
                showwarning("Warning", "  File published before ! ")
                return
        publisher = Thread(target = self.publishFile, args = (lname, fname))
        self.allThreads.append(publisher)
        publisher.start()

    def publishFile(self, lname, fname):
        self.listFile["lname"].append(lname)
        self.listFile["fname"].append(fname)
        mess = json.dumps({"ID": self.ID, "action": "publishFile", "fname": fname})
        self.ServerConnection.send(mess.encode(self.FORMAT))
        showinfo("Infomation", "  Publish '" + fname + "' successfully")
        
    def endSystem(self):
        if (self.ID != None):
            mess = json.dumps({"ID": self.ID, "action": "leaveNetwork"})
            self.ServerConnection.send(mess.encode(self.FORMAT))
        self.endAllThread = True
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread