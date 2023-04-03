import json
from alchemy_client import EthRPCClient

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/contract/<contract_address>')
def rpc(contract_address):
    try:
        func = request.args.get('func')
        arguments = json.loads(request.args.get('args', "[]"))
        return_type = request.args.get('return_type')
    except KeyError:
        return "invalid request"
    
    rpc = EthRPCClient()
    res = rpc.call(contract_address, func, arguments, return_type)

    return str(res)

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=3001)