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
serverName = '10.200.27.215'
serverPort = 9999

sentence = input('Input lowercase sentence:')
while (sentence!='exit'):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())
    clientSocket.close()
    sentence = input('Input lowercase sentence:')