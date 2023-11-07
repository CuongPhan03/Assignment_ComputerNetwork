from threading import Thread
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
            print("Fail connection !")
            return
        try:
            self.PeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.PeerSocket.bind((self.IP, self.PORT))
        except:
            self.endSystem()
            print("Unavailable address !")
            return
        self.endAllThread = False
        # register address
        self.listSocket.append(self.ServerConnection)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.PORT, "action": "register", "listFile": []})
        self.ServerConnection.send(data.encode(self.FORMAT))
        print("Peer is running...")
        # listen message
        self.listSocket.append(self.PeerSocket)
        self.PeerSocket.listen()
        receiver1 = Thread(target = self.listenServer)
        receiver2 = Thread(target = self.listenRes)
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
                receiver3 = Thread(target = self.listenReq, args=(conn,))
                self.allThreads.append(receiver3)
                receiver3.start()

    def listenServer(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.ServerConnection.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "resRegister"):
                    self.ID = jsonData["ID"]
                elif (jsonData["action"] == "resListFile"):
                    # jsonData = {"action": "resListFile", "listFile": [fname1, ]}
                    for fname in jsonData["listFile"]:
                        print(' ', fname)
                elif (jsonData["action"] == "resListPeer"):
                    # jsonData = {"action": "resListPeer", "listPeer": [{"name": , "ID": , "IP": , "port":}, ]}
                    print("  Other Users has the file: ")
                    self.listPeerServer = []
                    for peerData in jsonData["listPeer"]:
                        print('  ', peerData["name"])
                        self.listPeerServer.append(peerData)
                        
            except:
                continue

    def listenReq(self, connection):
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
                if (jsonData["action"] == "ping"):
                    print("\nPinging from Server...")
                    mess = json.dumps({"IP": self.IP, "port": self.PORT, "action": "resPing"})
                    connection.send(mess.encode(self.FORMAT))
            except:
                continue

    def listenRes(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.connectSocket.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "resFile"):
                    # jsonData = {"name": , "action": "resFile", "status": , "fname": }
                    if (jsonData["status"] == "ok"):
                        self.receiveFile(jsonData["fname"], jsonData["name"])
                    else:
                        print("File not found !")
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
        path = os.path.join(self.name, lname)
        if os.path.isfile(path):
            mess = json.dumps({"name": self.name , "action": "resFile", "status": "ok", "fname": fname})
            connection.send(mess.encode(self.FORMAT))
            time.sleep(0.1)
            with open(path, "rb") as file:
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
            print("File not found !")
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
        
    def requestListFile(self):
        mess = json.dumps({"name": self.name, "action": "reqListFile"})
        self.ServerConnection.send(mess.encode(self.FORMAT))

    def showMyFiles(self):
        print("  Published files: ")
        for i in range(len(self.listFile["lname"])):
            print("    lname: ", self.listFile["lname"][i], "  ->  ", "fname: ", self.listFile["fname"][i])
        print("  Private files: ")
        for lname in os.listdir(self.name):
            count = 0
            for i in range(len(self.listFile["lname"])):
                if (lname != self.listFile["lname"][i]):
                    count +=1
                else: 
                    break
            if count == len(self.listFile["lname"]):
                print("    lname: ", lname)

    def fetch(self, fname, hostname):
        if (hostname == self.name):
            print("You can't dowload your file !")
            return
        IP = None
        port = None
        for peerData in self.listPeerServer:
            if (hostname == peerData["name"]):
                IP = peerData["IP"]
                port = peerData["port"]
                break
        if (IP == None or port == None):
            print(hostname, " not found !")
            return
        self.connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSocket.connect((IP, port))
        self.listSocket.append(self.connectSocket)
        mess = json.dumps({"name": self.name, "action": "reqFile", "fname": fname})
        self.connectSocket.send(mess.encode(self.FORMAT))

    def publish(self, lname, fname):
        for name in self.listFile["lname"]:
            if (lname == name):
                print("File published before !")
                return
        for name in self.listFile["fname"]:
            if (fname == name):
                print("File published before !")
                return
        self.listFile["lname"].append(lname)
        self.listFile["fname"].append(fname)
        mess = json.dumps({"ID": self.ID, "action": "publishFile", "fname": fname})
        self.ServerConnection.send(mess.encode(self.FORMAT))
        print("Publish '" + fname + "' successfully")
        
    def requestListPeer(self, fname):
        path = os.path.join(self.name, fname)
        if os.path.isfile(path):
            print("File existed in local ! ")
            return
        mess = json.dumps({"action": "reqListPeer", "fname": fname})
        self.ServerConnection.send(mess.encode(self.FORMAT))

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