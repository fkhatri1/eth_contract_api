import os
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError
from typing import List, Any

class InvalidFunction(Exception):
    """Bad func"""

class EthRPCClient():
    def __init__(self):
        apiKey = os.environ.get("ALCHEMY_KEY")
        self.web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/'+apiKey))

    @staticmethod
    def encode_args(func_sig: str, args: List[Any]):

        func_name, arg_types_str = func_sig.replace(")", "").split("(")
        arg_types = arg_types_str.split(",")

        # For simplicity, I'm supporting only uint, address, bool types for now. 
        # Can be easily expanded to support all types here: https://docs.soliditylang.org/en/v0.7.0/abi-spec.html#types

        args_encoded = []
        for i in range(0, len(args)):
            if arg_types[i] in ("uint", "uint256"):
                args_encoded.append(f"{args[i]:#0{514}x}"[2:])
            elif arg_types[i] == "uint32":
                args_encoded.append(f"{args[i]:#0{66}x}"[2:])
            elif arg_types[i] in ("uint8", "bool"):
                args_encoded.append(f"{args[i]:#0{18}x}"[2:])
            elif arg_types[i] == "address":
                addr = ""
                if args[i][0:2] == "0x":
                    addr = args[i][2:]
                else:
                    addr = args[i]
                args_encoded.append(addr.rjust(64, '0'))
            
        args_string = "".join(args_encoded)

        return args_string
    
    @staticmethod
    def get_func_selector(func_sig: str):   
        from Crypto.Hash import keccak
        k = keccak.new(digest_bits=256)
        sig_bytes = bytes(func_sig, 'utf-8')
        k.update(sig_bytes)
        print(k.hexdigest()[0:8])
        return k.hexdigest()[0:8]

    def call(self, contract: str, function: str, args: List = [], return_type = "string"):
        print(function)
        print(type(function))
        print(args)
        print(type(args))
        
        func_selector = EthRPCClient.get_func_selector(function)
        encoded_args = EthRPCClient.encode_args(function, args)

        data = None
        try:
            data = self.web3.eth.call({
                    'to': contract,
                    'data': f"0x{func_selector}{encoded_args}"
                    }) 
            
        except ContractLogicError:
            print(f"invalid function for contract: {function}")
            raise InvalidFunction
        
        if return_type == "string":
            print(f"data: {data}")
            s = bytes.decode(data, "unicode_escape")
            s = s.replace("\n", "")[1:]
            print(f"|{s}|")
            return data.decode('utf-8').strip().replace("\n","")
        elif return_type == "address":
            return data.hex()
        elif return_type in ("bool", "int"):
            return int.from_bytes(data, byteorder='big')

