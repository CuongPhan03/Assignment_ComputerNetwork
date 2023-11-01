from threading import Thread
import socket
import json
import copy

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    FORMAT = "utf8"
    SIZE = 1024
    listFile = []
    jsonPeerDatas = []
    peerId = 0
    serverSocket = None
    listSocket = []
    allThreads = []
    endAllThread = False

    def startServer(self):
        binder = Thread(target=self.listenMessage)
        self.allThreads.append(binder)
        binder.start()

    def listenMessage(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.IP, self.PORT))
        self.listSocket.append(self.serverSocket)
        self.serverSocket.listen()
        print('Server is running...')
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
                    self.jsonPeerDatas.append(jsonData)
                    ID = copy.deepcopy(self.peerId)
                    jsonData["ID"] = ID
                    mess = json.dumps({"ID": ID, "action": "resRegister"})
                    connection.send(mess.encode(self.FORMAT))
                    self.peerId += 1
                elif (jsonData["action"] == "publishFile"):
                    index = jsonData["ID"]
                    fname = jsonData["fname"]
                    self.jsonPeerDatas[index]["listFile"].append(fname)
                    fname_exist = False
                    for fileName in self.listFile:
                        if (fname == fileName):
                            fname_exist = True
                            break
                    if (fname_exist == False):
                        self.listFile.append(fname)
                elif (jsonData["action"] == "reqListFile"):
                    self.sendListFile(connection)
                elif (jsonData["action"] == "reqListPeer"):
                    self.sendListPeer(connection, jsonData["fname"])
                elif (jsonData["action"] == "publishFile"):
                    self.sendListPeer(connection, jsonData["fname"])
            except:
                continue

    def sendListPeer(self, connection, fname):
        listPeer = []
        for jsonPeerData in self.jsonPeerDatas:
            for fileName in jsonPeerData["listFile"]:
                if (fileName == fname):
                    data = {"name": jsonPeerData["name"], "ID": jsonPeerData["ID"],"IP": jsonPeerData["IP"], "port": jsonPeerData["port"]}
                    listPeer.append(data)
        sendDatas = json.dumps({"action": "resListPeer", "listPeer": listPeer})
        connection.send(sendDatas.encode(self.FORMAT))

    def sendListFile(self, connection):
        listFile = copy.deepcopy(self.listFile)
        sendDatas = json.dumps({"action": "resListFile", "listFile": listFile})
        connection.send(sendDatas.encode(self.FORMAT))

    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True
