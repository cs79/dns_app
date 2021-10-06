from flask import Flask, request
from flask_api import status
from waitress import serve

app = Flask(__name__)

HOSTNAME = 'fibonacci.com'

# test route to make sure we can access this
@app.route('/')
def hello_world():
    return 'Hello world!'

# fibonacci route per Lab specifications
@app.route('/fibonacci/', methods=['GET'])
def fibonacci():
    # get parameters from route access; if missing, flag an error
    hostname    = request.args.get('hostname', default='400_error')
    fs_port     = request.args.get('fs_port',  default='400_error')
    number      = request.args.get('number',   default='400_error')
    as_ip       = request.args.get('as_ip',    default='400_error')
    as_port     = request.args.get('as_port',  default='400_error')
    
    # check for bad requests
    all_params  = [hostname, fs_port, number, as_ip, as_port]
    if len([k for k in all_params if k == '400_error']) > 0:
        return "Bad request: missing params in query string", status.HTTP_400_BAD_REQUEST

    # otherwise, process the request and return the Fibonacci number

    # first, need to query the AS (DNS) to find FS

    # then need to call FS to get the value

    # then return it to the user



# serve app via waitress on port 8080
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)