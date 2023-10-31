from threading import Thread
import socket
import json

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    FORMAT = "utf-8"
    SIZE = 1024
    listFile = {"datas":[]}
    serverSocket = None
    listSocket = []
    jsonPeerDatas = []
    allThreads = []
    endAllThread = False
    
    def startServer(self):
        binder = Thread(target = self.listenMessage)
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
                try:
                    receiveData = conn.recv(self.SIZE).decode(self.FORMAT)
                    jsonData = json.loads(receiveData)
                    if (jsonData["action"] == "register"):
                        jsonData["connection"] = conn
                        self.jsonPeerDatas.append(jsonData)
                    elif (jsonData["action"] == "publish"):
                        self.listFile["datas"].append(jsonData["fname"])
                    elif (jsonData["action"] == "reqListFile"):
                        self.sendListFile(conn)
                    elif (jsonData["action"] == "reqListPeer"):
                        self.sendListPeer(conn, jsonData["fname"])
                except:
                    continue

    def sendListPeer(self, connection, fname):
        datas = {"datas":[]}
        for jsonPeerData in self.jsonPeerDatas:
            if (fname in jsonPeerData):
                jsonData = json.loads(jsonPeerData)
                data = {"name": jsonData["name"], "IP": jsonData["IP"], "port": jsonData["port"]}
                datas["datas"].append(data)
        sendDatas = json.dumps(datas)
        connection.send(sendDatas.encode(self.FORMAT))

    def getListPeer(self):
        for peer in self.listFile:
            pass

    def getPeerInfo(self, connection):
        pass

    def sendListFile(self, connection):
        # code
        pass
    
    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True
    
    