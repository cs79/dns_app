from flask import Flask, request
from flask_api import status
from waitress import serve
import requests
from socket import *

app = Flask(__name__)

# test route to make sure we can access this
@app.route('/')
def hello_world():
    return 'Hello world!'

# fibonacci route per Lab specifications
@app.route('/fibonacci/', methods=['GET'])
def fibonacci():
    # get parameters from route access; if missing, flag an error
    hostname    = request.args.get('hostname', '400_error')
    fs_port     = request.args.get('fs_port',  '400_error')
    number      = request.args.get('number',   '400_error')
    as_ip       = request.args.get('as_ip',    '400_error')
    as_port     = request.args.get('as_port',  '400_error')
    
    # check for bad requests
    all_params  = [hostname, fs_port, number, as_ip, as_port]
    if len([k for k in all_params if k == '400_error']) > 0:
        return "Bad request: missing params in query string", status.HTTP_400_BAD_REQUEST

    # otherwise, process the request and return the Fibonacci number

    # first, need to query the AS (DNS) to find FS - need payload in "request" format
    payload = "TYPE=A\nNAME={}".format(hostname)
    # create UDP socket
    server_name     = as_ip
    server_port     = as_port
    client_socket   = socket(AF_INET, SOCK_DGRAM)
    # send payload
    client_socket.sendto(payload.encode(),(server_name, int(server_port)))
    # get response
    srv_resp, _ = client_socket.recvfrom(2048)
    resp = srv_resp.decode()
    rdict = dict([i.split('=') for i in resp.split('\n')])
    fs_addr = rdict['VALUE']

    # then need to call FS to get the value
    fib_resp = requests.get("http://{}:{}/fibonacci?number={}".format(fs_addr, int(fs_port), int(number)))

    # then return it to the user
    return fib_resp.text, status.HTTP_200_OK


# serve app via waitress on port 8080
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
