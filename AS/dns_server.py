from socket import *
import pandas as pd
import os
from flask_api import status

# globals
SERVER_PORT = 53533
DB_FILENAME = '/db/db.csv'

# simple socket server application
server_port     = SERVER_PORT
server_socket   = socket(AF_INET, SOCK_DGRAM) # UDP socket
server_socket.bind(('', server_port))

# main loop
while True:
    msg, client_addr = server_socket.recvfrom(2048) # not sure what buffer size is needed...
    msg = msg.decode()
    # parse the decoded message in sent format
    pdict = dict([i.split('=') for i in msg.split('\n')])
    name = pdict['NAME'] # will always need this

    # "register" if the message is a registration message
    if ('VALUE' in pdict.keys()):
        addr = pdict['VALUE']
        if (os.path.exists(DB_FILENAME)):
            # open and update
            df = pd.read_csv(DB_FILENAME, index_col=0)
            # see if we need to overwrite
            if (name in df['name'].values):
                df[df['name'] == name, 'address'] = addr
            # otherwise just append a new entry (for different name)
            else:
                df = df.append({'name': name, 'address': addr}, ignore_index=True)
            # write back to "disk" in either case
            df.to_csv(DB_FILENAME)
        else:
            # create and save at path
            df = pd.DataFrame(columns=['name', 'address'])
            df = df.append({'name': name, 'address': addr}, ignore_index=True)
            df.to_csv(DB_FILENAME)

        # if we haven't errored out during registration, respond with 201
        resp = status.HTTP_201_CREATED
        server_socket.sendto(str(resp).encode(), client_addr)

    # respond to "DNS query" if the message is in that format
    else:
        # assume message is properly formatted for now; look up value
        df = pd.read_csv(DB_FILENAME, index_col=0)
        ip = df[df['name'] == name]['address'][0]
        resp = 'TYPE=A\nNAME={}\nVALUE={}\nTTL=10'.format(name, ip)
        server_socket.sendto(resp.encode(), client_addr)
