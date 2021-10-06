from flask import Flask, request
from flask_api import status
from socket import *
from waitress import serve

app = Flask(__name__)

# globals
SERVER_NAME = 'as_flask' # or whatever we name the service in Kubernetes
SERVER_PORT = 53533

# test route to make sure we can access this
@app.route('/')
def hello_world():
    return 'Hello world!'

# registration route
@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        # parse request data
        reqdata     = request.get_json()
        hostname    = reqdata.get('hostname', default='400_error')
        ip          = reqdata.get('ip',       default='400_error')
        as_ip       = reqdata.get('as_ip',    default='400_error')
        as_port     = reqdata.get('as_port',  default='400_error')
        all_args = [hostname, ip, as_ip, as_port]
        if len([k for k in all_args if k == '400_error']) > 0:
            return "Bad request: missing args in JSON payload", status.HTTP_400_BAD_REQUEST
        
        # if we got JSON with all args, proceed to register with AS

        # first, create UDP socket
        server_name     = SERVER_NAME
        server_port     = SERVER_PORT
        client_socket   = socket(AF_INET, SOCK_DGRAM)
        
        # format the data payload
        payload = "TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"

        # now send the registration request:


    else:
        return "Bad request: payload not in JSON format", status.HTTP_400_BAD_REQUEST

# serve app via waitress on port 9090
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=9090)