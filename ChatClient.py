# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 13:21:20 2018

@author: usingerr

Network Programming Fall 2018
Final Project - Chat Program
Ross Usinger, Nick Scalese
Client
"""

import socket
serverName = '127.0.0.1'
serverPort = 9999



while (sentence!='exit'):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('Server says:', modifiedSentence.decode())
    clientSocket.close()
    sentence = input('Input lowercase sentence:')