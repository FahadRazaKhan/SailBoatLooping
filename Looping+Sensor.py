# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:56:33 2017

@author: fahad

This is Client File used to connect with the Server (RPi) and start the Looping 
Program. 
"""



import socket
import sys
import time


TCP_IP = '192.168.31.148' # IP address of the Server
TCP_PORT = 50007
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Client socket is created')
try:
    s.connect((TCP_IP, TCP_PORT))
    print('Connected')
except:
    print('An Error Occured!')
    sys.exit()


MESSAGE = input('Please press Y to Start or N if you dont want to...  ')
message_bytes = MESSAGE.encode('utf-8') ## Converting into Bytes
s.sendall(message_bytes)
time.sleep(0.2) ## 0.2 second delay
while True:
    
    data = s.recv(BUFFER_SIZE)
    if data is None:
        pass
    else:
        dataDecode= str(data.decode('utf-8')) # converting Decoded data in String
        print (data.decode('utf-8'),"\n")
        if dataDecode == 'Motors Stopped, and Looping Finished' or dataDecode == 'Program Aborted!':
            print('Closing Connection...')
            break
        
    
    time.sleep(0.5) # Running While loop once per 1/2 second

time.sleep(0.5)
s.close()
time.sleep(0.5) ## 0.5 second delay
print('Communication Closed \n')