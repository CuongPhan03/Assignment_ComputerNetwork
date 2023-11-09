from threading import Thread
import socket
import json
import copy

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    FORMAT = "utf8"
    SIZE = 1024
    listFile = []       # [fname1, fname2]
    jsonPeerDatas = []  # [{"ID": , "name": , "IP": , "port": , "action": , "listFile": [fname, ]}, ]
    peerId = 0
    serverSocket = None
    listSocket = []
    allThreads = []
    endAllThread = None

    def __init__(self, port):
        self.PORT = port

    def startServer(self):
        binder = Thread(target = self.listenMessage)
        self.allThreads.append(binder)
        binder.start()

    def listenMessage(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.IP, self.PORT))
        except:
            print("Fail binding address !")
            self.endSystem()
            return
        self.endAllThread = False
        self.listSocket.append(self.serverSocket)
        self.serverSocket.listen()
        print("Server is running...")
        while (self.endAllThread == False):
            try:
                conn, addr = self.serverSocket.accept()
            except:
                break
            if (conn):
                receiver = Thread(target = self.receiveMessage, args=(conn,))
                self.allThreads.append(receiver)
                receiver.start()
            
    def receiveMessage(self, connection):
        while (self.endAllThread == False):
            try:
                receiveData = connection.recv(self.SIZE).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "register"):
                    # jsonData = {"name": , "IP": , "port": , "action": "register", "listFile": []}
                    self.handleRegister(connection, jsonData)
                elif (jsonData["action"] == "publishFile"):
                    # jsonData = {"name": , "ID": , "action": "publishFile", "fname": }
                    self.handlePublish(jsonData)
                elif (jsonData["action"] == "reqListFile"):
                    # jsonData = {"name": , "action": "reqListFile"}
                    print(jsonData["name"], "request list file.")
                    self.sendListFile(connection)
                elif (jsonData["action"] == "reqListPeer"):
                    # jsonData = {"action": "reqListPeer", "fname": }
                    self.sendListPeer(connection, jsonData["fname"])
                elif (jsonData["action"] == "leaveNetwork"):
                    # jsonData = {"ID": , "action": "leaveNetwork"}
                    self.handleLeave(connection, jsonData["ID"])
            except:
                continue
    
    def handleRegister(self, connection, jsonData):
        print(jsonData["name"] + " joined.")
        jsonData["ID"] = self.peerId
        self.jsonPeerDatas.append(jsonData)
        mess = json.dumps({"ID": self.peerId, "action": "resRegister"})
        connection.send(mess.encode(self.FORMAT))
        self.peerId += 1

    def handlePublish(self, jsonData):
        index = 0
        for peerData in self.jsonPeerDatas:
            if (peerData["ID"] == jsonData["ID"]):
                break
            index += 1
        fname = jsonData["fname"]
        print(self.jsonPeerDatas[index]["name"] + " published " + fname)
        self.jsonPeerDatas[index]["listFile"].append(fname)
        for fileName in self.listFile:
            if (fname == fileName):
                return
        self.listFile.append(fname)

    def sendListPeer(self, connection, fname):
        listPeer = []
        for peerData in self.jsonPeerDatas:
            for fileName in peerData["listFile"]:
                if (fileName == fname):
                    data = {"name": peerData["name"], "ID": peerData["ID"], "IP": peerData["IP"], "port": peerData["port"]}
                    listPeer.append(data)
        sendData = json.dumps({"action": "resListPeer", "listPeer": listPeer})
        connection.send(sendData.encode(self.FORMAT))

    def sendListFile(self, connection):
        listFile = copy.deepcopy(self.listFile)
        sendData = json.dumps({"action": "resListFile", "listFile": listFile})
        connection.send(sendData.encode(self.FORMAT))

    def ping(self, hostname):
        peerIP = None
        peerPort = None
        for peerData in self.jsonPeerDatas:
            if (hostname == peerData["name"]):
                peerIP = peerData["IP"]
                peerPort = peerData["port"]
                break
        if (peerIP == None or peerPort == None):
            print(hostname, " not found !")
            return
        try:
            pingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pingSocket.connect((peerIP, peerPort))
        except:
            print("Fail connection !")
            return
        print("Pinging " + hostname + ' [' + peerIP + ', ' + str(peerPort) + '] ...')
        mess = json.dumps({"action": "ping"})
        pingSocket.send(mess.encode(self.FORMAT))
        receiveData = pingSocket.recv(self.SIZE).decode(self.FORMAT)
        jsonData = json.loads(receiveData)
        if (jsonData["action"] == "resPing"):
            print("Reply from [" + jsonData["IP"] + ', ' + str(jsonData["port"]) + '] : OK')

    def handleLeave(self, connection, ID):
        index = 0
        peerListFile = None
        for peerData in self.jsonPeerDatas:
            if (peerData["ID"] == ID):
                peerListFile = copy.deepcopy(peerData["listFile"])
                break
            index += 1
        print(self.jsonPeerDatas[index]["name"]  + " leave.")
        self.jsonPeerDatas.pop(index)
        datasString = json.dumps(self.jsonPeerDatas)
        for peerFname in peerListFile:
            if (peerFname not in datasString):
                self.listFile.remove(peerFname)
        connection.close()

    def endSystem(self):
        self.endAllThread = True
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
