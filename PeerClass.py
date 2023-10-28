from threading import Thread
import tkinter as tk
import socket
import json
import os

class Peer:
    listSocket = []
    IP = socket.gethostbyname(socket.gethostname())
    allThreads = []
    endAllThread = False
    filename = ""
    ports = []
    listPeers = ""
    ServerPort = 5000
    ServerIP = socket.gethostbyname(socket.gethostname())
    FORMAT = "utf-8"
    
    def __init__(self,name,port,text):
        self.port = port
        self.name = name
        self.text = text

    def recv_input_stream(self, connection, IP):
        print("Connection from: " + str(IP))
        while True:
            if (self.endAllThread == True):
                break
            try:
                data = connection.recv(1024).decode(self.FORMAT)
                if (not(data)):
                    return -1
                jsonMessage = json.loads(data)
                print(jsonMessage)
               
                if(jsonMessage["type"] == "file"):
                    self.filename = jsonMessage["filename"]
                    self.text.configure(state='normal')
                    self.text.insert(tk.END,"<"+jsonMessage["name"]+ "> : send you " + self.filename +" check your folder\n")
                    self.text.configure(state='disable')
                elif(jsonMessage["type"] == "central"):
                    self.listPeers = jsonMessage["listPeers"]
            except:
                continue
    
    def registerPort(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.IP, self.port))
        serverSocket.listen()
        centralSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        centralSocket.connect((self.ServerIP, self.ServerPort))
        data =  '{"name":"' + self.name + '", "IP":"' + self.IP +'", "port":' + str(self.port) + '}'
        centralSocket.send(data.encode(self.FORMAT))
        '''while (True):
            if (self.endAllThread == True):
                break
            conn, addr = serverSocket.accept()  # accept new connection
            acceptThread = Thread(target=self.acceptConnection,args=(conn,addr))
            self.allThreads.append(acceptThread)
            acceptThread.start()'''
        
    def getListPeer(self):
        pass

    def connectToPeer(self):
        pass
    
    def acceptConnection(self,connection, IP):
        while True:
            if (self.endAllThread == True):
                break
            input_stream = Thread(target=self.recv_input_stream, args=(connection,IP))
            receiveFileStream = Thread(target=self.handleReceiveFile, args=(connection,))
            receiveFileStream.start()
            input_stream.start()
            self.allThreads.append(input_stream)
            self.allThreads.append(receiveFileStream)
            receiveFileStream.join()
            input_stream.join()

    def publishFile(self):
        pass

    def handleSendFile(self,filePath):
        filename = filePath.split('/')[-1]
        self.text.configure(state='normal')  
        self.text.insert(tk.END,"<You> : send an " + filename +" to your friend\n")
        self.text.configure(state='disable')
        data =  '{ "name":"'+self.name+'", "type":"file", "filename":"'+filename+'"}'
        for client in self.listSocket:
            client.send(data.encode('utf-8'))
        for client in self.listSocket:
            try:
                f = open(filePath,'rb')
                print("Start sending file")
                while (True):
                    l = f.read(1024)
                    if (not(l)):
                        break
                    client.send(l)
                    print('Sending...')
                f.close()
                print("Done Sending")
                client.shutdown(socket.SHUT_WR)
            except:
                pass
        self.listSocket = []
        for port in self.ports:
            sender = Thread(target=self.setUpSendMessage,args=(self.IP,port))
            self.allThreads.append(sender)
            sender.start()

    def handleReceiveFile(self,connection):
        while True:
            try:
                try: 
                    os.mkdir(self.name) 
                except: 
                    pass
                f = open(self.name+"/"+self.filename,'wb')
                print('Start Receiving')
                while (True):
                    print("Receiving...")
                    l = connection.recv(1024)
                    if (not(l)):
                        break
                    f.write(l)
                f.close()
                print("Done Receiving") 
                self.filename = ""
            except:
                continue

    def setUpSendMessage(self,IP,port):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((IP, int(port)))
        self.listSocket.append(clientSocket)
        print("Connect to " + str(port))

    def startServer(self):
        binder = Thread(target=self.registerPort)
        self.allThreads.append(binder)
        binder.start()

    def startClient(self,port):
        sender = Thread(target=self.setUpSendMessage,args=(self.IP,port))
        self.ports.append(port)
        self.allThreads.append(sender)
        sender.start()

    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True