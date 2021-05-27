from time import sleep
import pickle
import socket
from JoyStickModule import getJS
from Setting import HOST,PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' + str(server_address))
s.connect(server_address)
record = 0
try:
    while True:
        joyVal = getJS()
        if joyVal['share'] == 1:
            if record == 0:
                print('Recording Started ...')
            record += 1
            sleep(0.300)
        if record == 1:
            s.sendall(pickle.dumps(joyVal))
            data = s.recv(1024)
            print('Server: ', data.decode("utf8"))

        elif record == 2:
            s.sendall(pickle.dumps(joyVal))
            data = s.recv(1024)
            print('Server: ', data.decode("utf8"))
            print('Stop send')
            record = 0


finally:
    s.close()