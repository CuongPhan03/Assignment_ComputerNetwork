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
    ServerConnSocket = None
    listSocket = []
    allThreads = []
    endAllThread = False
    
    def __init__(self, name, port):
        self.name = name
        self.port = port
    
    def startPeer(self):
        register = Thread(target=self.runPeer)
        self.allThreads.append(register)
        register.start()

    def runPeer(self):
        # register address
        self.ServerConnSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerConnSocket.connect((self.ServerIP, self.ServerPort))
        self.listSocket.append(self.ServerConnSocket)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.port, "action": "register"})
        self.ServerConnSocket.send(data.encode(self.FORMAT))
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

    def getListPeer(self, fname):
        # code
        data 
        return data

    def getListFile(self):
        # code
        data
        return data
    
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
        pass

    def sendFile(self, connection, fname):
        mess = json.dumps({"name": self.name, "action": "resFile", "fname": fname})
        connection.send(mess.encode(self.FORMAT))
        # code

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