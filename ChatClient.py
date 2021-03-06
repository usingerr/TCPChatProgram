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
unexpectedDisconnect = False;
isConnected = True;

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def receiveMessage(connection):
    while True:
        try:
            r, w, x = select.select((connection,), (connection,), (), 0);
            message = connection.recv(1024).decode();
            if message:
                print(message);
            else:
                break;
        except select.error:
            break;
    
def dispatcher():                                # listen until process killed
    _thread.start_new(receiveMessage, (clientSocket,));
    message = '';
    while(message != "!leave"):
        try:
            r, w, x = select.select((clientSocket,), (clientSocket,), (), 0);
            message = input("ME: ");
            clientSocket.send(message.encode());
        except select.error:
            break;
        
dispatcher();
print("\nThe session has ended.")

#If the client opts to leave on it's own, then wait for the server to close its socket.
#Otherwise, just close the socket from the get go.
clientSocket.close();