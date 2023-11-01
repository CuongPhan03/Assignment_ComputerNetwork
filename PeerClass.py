from threading import Thread
import tkinter as tk
import socket
import json
import os
import time

class Peer:
    IP = socket.gethostbyname(socket.gethostname()) 
    # port lay tu input
    ServerIP = socket.gethostbyname(socket.gethostname()) # test 2 may thi dung IP cua sever
    ServerPort = 5000
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
    endAllThread = False
    
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.ID = None
    
    def startPeer(self):
        register = Thread(target = self.runPeer)
        self.allThreads.append(register)
        register.start()

    def runPeer(self):
        # register address
        try:
            self.ServerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ServerConnection.connect((self.ServerIP, self.ServerPort))
        except:
            print("Fail connection !")
            return
        self.listSocket.append(self.ServerConnection)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.port, "action": "register", "listFile": []})
        self.ServerConnection.send(data.encode(self.FORMAT))
        # listen message
        try:
            self.PeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.PeerSocket.bind((self.IP, self.port))
        except:
            print("Unavailable address !")
            return
        self.listSocket.append(self.PeerSocket)
        self.PeerSocket.listen()
        print("Peer " + self.name + " is running...")
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
                    # jonsData = {"ID": , "action": "resRegister"}
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
                    # jsonData = {"name": , "action": "resFile", "fname": }
                    self.receiveFile(jsonData["fname"], jsonData["name"])
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
            mess = json.dumps({"name": self.name ,"action": "resFile", "fname": fname})
            connection.send(mess.encode(self.FORMAT))
            time.sleep(0.01)
            with open(path, "rb") as file:
                while True:
                    data = file.read(self.SIZE)
                    if (not data):
                        break
                    print("Sending " + fname + " to " + peerName + "...")
                    connection.send(data)
                    time.sleep(0.01)
                print("Done Sending !")
        else:
            print("File not found")

    def receiveFile(self, fname, peerName):
        self.connectSocket.settimeout(0.2)
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
            print("Done Receiving !") 
        self.connectSocket.close()
        self.connectSocket = None
        
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
            print("Busy !")
            return
        path = os.path.join(self.name, fname)
        if os.path.isfile(path):
            print("File existed in local !")
            return
        print("Request " + fname + " from " + peerName)
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
        path = os.path.join(self.name, lname)
        if os.path.isfile(path):
            for name in self.listFile["lname"]:
                if (lname == name):
                    print("File existed on server !")
                    return
            for name in self.listFile["fname"]:
                if (fname == name):
                    print("File existed on server !")
                    return
        else:
            print("File doesn't exists in local")
            return
        publisher = Thread(target = self.publishFile, args = (lname, fname))
        self.allThreads.append(publisher)
        publisher.start()

    def publishFile(self, lname, fname):
        self.listFile["lname"].append(lname)
        self.listFile["fname"].append(fname)
        mess = json.dumps({"name": self.name, "ID": self.ID, "action": "publishFile", "fname": fname})
        self.ServerConnection.send(mess.encode(self.FORMAT))
        print("Publish " + fname + " successfully")
        
    def endSystem(self):
        print("Peer off !")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True