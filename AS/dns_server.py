from socket import *
import pandas as pd

# globals
SERVER_PORT = 53533

# simple socket server application
server_port     = SERVER_PORT
server_socket   = socket(AF_INET, SOCK_DGRAM) # UDP socket
server_socket.bind('', server_port)

# main loop
while True:
    msg, client_addr = server_socket.recvfrom(2048) # not sure what buffer size is needed...
    msg = msg.decode()
    # parse the message if it is in some weird format

    # "register" if the message is a registration message

    # respond to "DNS query" if the message is in that format