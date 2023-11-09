from PeerClass import Peer
import copy
import time

peer = None
    
serverPort = input('Server port: ' )
serverIP = input('Server IP: ' )
peerName =  input('Peer name: ' )
peerPort = input('Peer port: ' )
peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
print('Peer IP: ', peer.IP)
peer.startPeer()
while (peer.endAllThread == None):
    time.sleep(0.01)

while (peer.endAllThread == False):
    try:
        command = input('Type your command:\n')
    except:
        break
    arr = command.split(' ')
    if (arr[0] == 'publish' and len(arr) == 3):
        peer.publish(arr[1], arr[2])
    elif (arr[0] == 'files' and len(arr) == 2):
        if (arr[1] == 'server'):
            peer.requestListFile()
        elif (arr[1] == 'local'):
            peer.showMyFiles()
    elif (arr[0] == 'fetch' and len(arr) == 2):
        peer.requestListPeer(arr[1])
        time.sleep(0.1)
        inputpeer = input('You want to fetch from: ')
        peer.fetch(arr[1], inputpeer)
    else:
        print('Wrong command !')
    
peer.endSystem()