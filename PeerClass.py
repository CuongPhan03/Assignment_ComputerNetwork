from threading import Thread
import tkinter as tk
import socket
import json
import os

class Peer:
    IP = socket.gethostbyname(socket.gethostname()) 
    # port lay tu input
    ServerIP = socket.gethostbyname(socket.gethostname()) # test 2 may thi dung IP cua sever
    ServerPort = 5000
    FORMAT = "utf-8"
    SIZE = 1024
    PeerSocket = None
    listSocket = []
    allThreads = []
    endAllThread = False
    
    def __init__(self, name, port, text):
        self.port = port
        self.name = name
        self.text = text
    
    def startPeer(self):
        register = Thread(target=self.runPeer)
        self.allThreads.append(register)
        register.start()

    def runPeer(self):
        # register address
        registerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        registerSocket.connect((self.ServerIP, self.ServerPort))
        self.listSocket.append(registerSocket)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.port, "action": "register"})
        registerSocket.send(data.encode(self.FORMAT))
        # listen message
        self.PeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PeerSocket.bind((self.IP, self.port))
        self.listSocket.append(self.PeerSocket)
        self.PeerSocket.listen()
        print('Peer is running...')
        while (not(self.endAllThread)):
            try:
                conn, addr = self.PeerSocket.accept()
            except:
                break
            if (conn):
                try:
                    receiveData = conn.recv(self.SIZE).decode(self.FORMAT)
                    jsonData = json.loads(receiveData)
                    fname = jsonData["fname"]
                    if (jsonData["action"] == "reqFile"):
                        sender = Thread(target=self.sendFile, args=(conn, fname))
                        self.allThreads.append(sender)
                        sender.start()
                    elif (jsonData["action"] == "resFile"):
                        self.receiveFile(conn, fname)
                except:
                    continue

    def getListPeer(self, connection):
        # code
        
        peerList = []
        for socket in self.listSocket:
            if socket != connection:
                peerList.append(socket.getpeername())
        return peerList

    def getListFile(self, connection):
        # code

        fileList = os.listdir(self.name)
        return fileList
    
    def requestFile(self, IP, port, fname):
        connect = Thread(target=self.startConnection, args=(IP, port, fname))
        self.allThreads.append(connect)
        connect.start()

    def startConnection(self, IP, port, fname):
        connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectSocket.connect((IP, port))
        mess = json.dumps({"name": self.name, "action": "reqFile", "fname": fname})
        connectSocket.send(mess.encode(self.FORMAT))

    def publishFile(self, lname, fname):
        # code

        path = os.path.join(self.name, lname)
        if os.path.isfile(path):
            return "File already exists"
        else:
            with open(path, "w") as file:
                file.write(self.text)
            return "File published successfully"
        

    def sendFile(self, connection, fname):
        # code

        path = os.path.join(self.name, fname)
        if os.path.isfile(path):
            mess = json.dumps({"name": self.name, "action": "resFile", "fname": fname})
            connection.send(mess.encode(self.FORMAT))
            with open(path, "rb") as file:
                data = file.read(self.SIZE)
                while data:
                    connection.send(data)
                    data = file.read(self.SIZE)
            print("Send succeed")
        else:
            print("File not found")
        connection.close()

        print("Send succeed")
        connection.close()

    def receiveFile(self, connection, fname):
        while True:
            try:
                f = open(self.name + "/" + fname, 'wb')
                while (True):
                    print("Receiving...")
                    try:
                        file = connection.recv(self.SIZE)
                        f.write(file)
                        f.close()
                        print("Done Receiving") 
                        connection.close()
                        break
                    except:
                        continue
            except:
                continue
        
    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True