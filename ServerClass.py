from threading import Thread
import socket
import json
import copy

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    FORMAT = "utf8"
    SIZE = 1024
    listFile = []       # [fname1, fname2]
    jsonPeerDatas = []  # [{"name": , "IP": , "port": , "action": , "listFile": [fname, ]}, ]
    peerId = 0
    serverSocket = None
    listSocket = []
    allThreads = []
    endAllThread = False

    def __init__(self, port):
        self.PORT = port

    def startServer(self):
        binder = Thread(target=self.listenMessage)
        self.allThreads.append(binder)
        binder.start()

    def listenMessage(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.IP, self.PORT))
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
                    self.sendListFile(connection)
                elif (jsonData["action"] == "reqListPeer"):
                    # jsonData = {"action": "reqListPeer", "fname": }
                    self.sendListPeer(connection, jsonData["fname"])
            except:
                continue
    
    def handleRegister(self, connection, jsonData):
        for jsonPeerData in self.jsonPeerDatas:
            if (jsonData["IP"] == jsonPeerData["IP"] and jsonData["port"] == jsonPeerData["port"]):
                print("Address existed !")
                mess = json.dumps({"registerSucceed": False, "action": "resRegister"})
                connection.send(mess.encode(self.FORMAT))
                return
        print(jsonData["name"] + " joined.")
        self.jsonPeerDatas.append(jsonData)
        jsonData["ID"] = self.peerId
        mess = json.dumps({"registerSucceed": True, "ID": self.peerId, "action": "resRegister"})
        connection.send(mess.encode(self.FORMAT))
        self.peerId += 1

    def handlePublish(self, jsonData):
        index = jsonData["ID"]
        fname = jsonData["fname"]
        print(jsonData["name"] + " published " + fname)
        self.jsonPeerDatas[index]["listFile"].append(fname)
        for fileName in self.listFile:
            if (fname == fileName):
                return
        self.listFile.append(fname)

    def sendListPeer(self, connection, fname):
        listPeer = []
        for jsonPeerData in self.jsonPeerDatas:
            for fileName in jsonPeerData["listFile"]:
                if (fileName == fname):
                    data = {"name": jsonPeerData["name"], "ID": jsonPeerData["ID"], "IP": jsonPeerData["IP"], "port": jsonPeerData["port"]}
                    listPeer.append(data)
        sendDatas = json.dumps({"action": "resListPeer", "listPeer": listPeer})
        connection.send(sendDatas.encode(self.FORMAT))

    def sendListFile(self, connection):
        listFile = copy.deepcopy(self.listFile)
        sendDatas = json.dumps({"action": "resListFile", "listFile": listFile})
        connection.send(sendDatas.encode(self.FORMAT))

    def endSystem(self):
        print("Server off.")
        self.endAllThread = True
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
