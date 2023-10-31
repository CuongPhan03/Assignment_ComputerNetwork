from tkinter import * 
from tkinter.ttk import *
from ServerClass import Server
from tkinter import filedialog
from threading import Thread
import copy

server = None
flag = True

def RunServer():
    global flag
    global server
    if (flag == False):
        return
    server = Server()
    server.startServer()
        

def on_closing():
    global server
    global flag
    flag = False
    if (server != None):
        server.endSystem()
    master.destroy()
    
master = Tk()
master.title('File Sharing Application')
master.geometry("600x500")
master.resizable(0, 0)

# Server
runServerButton = Button(master,text="Run",command=RunServer)
runServerButton.place(x=250,y = 100)

master.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()