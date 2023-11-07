from ServerClass import Server
import copy
import time

server = None

PORT = input('Server port: ')
server = Server(int(PORT))
print('Server IP: ', server.IP)
server.startServer()
while (server.endAllThread == None):
    time.sleep(0.01)

while (server.endAllThread == False):
    try:
        command = input('Type your command:\n')
    except:
        break
    arr = command.split(' ')
    if (len(arr) == 2):
        if (arr[0] == 'ping'):
            server.ping(arr[1])
        elif (arr[0] == 'discover'):
            peerDatas = copy.deepcopy(server.jsonPeerDatas)
            for i in range(len(peerDatas)):
                if (peerDatas[i]["name"] == arr[1]):
                    print('  hostname:', peerDatas[i]["name"], ', list file:', peerDatas[i]["listFile"])
                    break
                elif (i == len(peerDatas) - 1):
                    print(arr[1], ' not found !')
        else:
            print('Wrong command !')
    else:
        print('Wrong command !')

server.endSystem()