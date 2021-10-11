from flask import Flask, request
from flask_api import status
from socket import *
from waitress import serve

app = Flask(__name__)

# Fibonacci function taken from https://www.geeksforgeeks.org/python-program-for-n-th-fibonacci-number/
FibArray = [0, 1]
def fib(n):
    if (n < 0):
        print("Incorrect input")
    elif (n <= len(FibArray)):
        return FibArray[n-1]
    else:
        temp_fib = fib(n-1)+fib(n-2)
        FibArray.append(temp_fib)
        return temp_fib

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
        hostname    = reqdata.get('hostname', '400_error')
        ip          = reqdata.get('ip',       '400_error')
        as_ip       = reqdata.get('as_ip',    '400_error')
        as_port     = reqdata.get('as_port',  '400_error')
        all_args = [hostname, ip, as_ip, as_port]
        if len([k for k in all_args if k == '400_error']) > 0:
            return "Bad request: missing args in JSON payload", status.HTTP_400_BAD_REQUEST
        
        # if we got JSON with all args, proceed to register with AS

        # first, create UDP socket
        server_name     = as_ip
        server_port     = as_port
        client_socket   = socket(AF_INET, SOCK_DGRAM)
        
        # format the data payload - newline between fields (it seems?)
        payload = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname, ip)

        # now send the registration request:
        client_socket.sendto(payload.encode(),(server_name, int(server_port)))

        # look for success and then respond with 201
        srv_resp, _ = client_socket.recvfrom(2048) # should be sufficient buffer I think
        if (int(srv_resp.decode()) == 201):
            return "Registration successful", status.HTTP_201_CREATED
        else:
            return "Error encountered during registration", status.HTTP_500_INTERNAL_SERVER_ERROR
    # if we didn't get a JSON payload, respond with error
    else:
        return "Bad request: payload not in JSON format", status.HTTP_400_BAD_REQUEST

@app.route('/fibonacci/', methods=['GET'])
def fibonacci():
    # get number parameter; if missing, flag an error
    number = request.args.get('number',   default='400_error')
    if (number == '400_error'):
        return "Bad request: missing number parameter in query string", status.HTTP_400_BAD_REQUEST
    # make sure we can use it as an int
    try:
        number = int(number)
    except:
        return "Passed number could not be coerced to integer", status.HTTP_400_BAD_REQUEST
    # otherwise process the request
    else:
        res = fib(number)
        return str(res), status.HTTP_200_OK

# serve app via waitress on port 9090
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=9090)
