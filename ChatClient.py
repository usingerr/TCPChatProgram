# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 13:21:20 2018

@author: usingerr

Network Programming Fall 2018
Final Project - Chat Program
Ross Usinger, Nick Scalese
Client
"""

import socket;
import _thread;

serverName = '127.0.0.1'
serverPort = 3333

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
isConnected = True;

def receiveMessage(connection):
    while True:
        if isConnected:
            message = connection.recv(1024).decode();
            print(message);
        else:
            break;
    
def dispatcher():                                # listen until process killed
    _thread.start_new(receiveMessage, (clientSocket,));
    message = input("ME: ");
    while(message != "!leave"):
        clientSocket.send(message.encode());
        message = input("ME: ");
    global isConnected;
    isConnected = False;
        
dispatcher();

clientSocket.close();