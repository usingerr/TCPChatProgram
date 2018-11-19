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
import select;
import _thread;

serverName = '127.0.0.1'
serverPort = 3333

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
isConnected = True;

def receiveMessage(connection):
    while True:
        r, w, x = select.select((connection,), (), (), 0);
        if isConnected:
            if not r:
                break;
            message = connection.recv(1024).decode();
            if message:
                print(message);
        else:
            break;
    
def dispatcher():                                # listen until process killed
    _thread.start_new(receiveMessage, (clientSocket,));
    message = input("ME: ");
    while(message != "!leave"):
        r, w, x = select.select((clientSocket,), (), (), 0);
        if not r:
            break;
        clientSocket.send(message.encode());
        message = input("ME: ");
    global isConnected;
    isConnected = False;
        
dispatcher();
print("\nThe session has ended.")

clientSocket.close();