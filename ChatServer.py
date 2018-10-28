# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 13:18:57 2018

@author: usingerr

Network Programming Fall 2018
Final Project - Chat Program
Ross Usinger, Nick Scalese
Server
"""

import socket
serverPort = 9999

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while True:
     connectionSocket, addr = serverSocket.accept()
     print ('Connected with ' + addr[0] + ':' + str(addr[1]))
     sentence = connectionSocket.recv(1024).decode()
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())
     connectionSocket.close()