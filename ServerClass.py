from threading import Thread
import socket
import json

class Server:
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    serverSocket = None
    listSocket = []
    jsonPeerDatas = []
    allThreads = []
    endAllThread = False
    
    def startServer(self):
        binder = Thread(target=self.listenRegistration)
        self.allThreads.append(binder)
        binder.start()

    def listenRegistration(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listSocket.append(self.serverSocket)
        self.serverSocket.bind(self.ADDR)
        self.serverSocket.listen()

        print('Server is running...')
        while (self.endAllThread == False):
            #self.sendListPeer()
            try:
                conn, addr = self.serverSocket.accept()
            except:
                break
            if (conn):
                print("Have an user connnected")
                try:
                    data = conn.recv(1024).decode(self.FORMAT)
                    rawData = data.replace('}', ', "listFile": []}')
                    print(rawData)
                    self.jsonPeerDatas.append(rawData)
                except:
                    continue

    def sendListPeer(self, IP, port, fname):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listSocket.append(clientSocket)
        clientSocket.connect((IP, port))
        datas = '{"data":['
        i = 0
        for jsonPeerData in self.jsonPeerDatas:
            if (fname in jsonPeerData):
                jsonData = json.loads(jsonPeerData)
                rawData = '{"name":"' + jsonData["name"] + '", "IP":"' + jsonData["IP"] + '", "port":' + str(jsonData["port"]) + '}'
                if i != 0: 
                    datas += ', '
                datas += rawData
                i += 1
        datas += ']}'
        clientSocket.send(datas.encode(self.FORMAT))
        print("Send success")

    def sendListFile(self):
        pass

    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True
    
    