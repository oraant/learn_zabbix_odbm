import socket
import os

if __name__ == '__main__':
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/453zcv")

    instr = raw_input()
    client.send(instr)
    print client.recv(1024)

    client.close()
