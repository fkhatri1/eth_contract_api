import pytest
from alchemy_client import EthRPCClient, InvalidFunction


@pytest.fixture
def rpc():
   return EthRPCClient()

@pytest.fixture
def contract():
   return "0xdAC17F958D2ee523a2206206994597C13D831ec7"


def test_get_func_selector():
   assert EthRPCClient().get_func_selector("balanceOf(address)") == "70a08231"
   assert EthRPCClient().get_func_selector("decimals()") == "313ce567"

def test_encode_args():
    func_sig = "myfunc(uint32,bool)"
    test_args = [69, True]
    assert EthRPCClient.encode_args(func_sig, test_args) == "00000000000000000000000000000000000000000000000000000000000000450000000000000001"

def test_call_address(rpc, contract):
    func_sig = "getOwner()"
    assert rpc.call(contract, func_sig, [], "address").lower() == "0x000000000000000000000000c6cde7c39eb2f0f0095f41570af89efc2c1ea828"
    
def test_call_bool(rpc, contract):
    func_sig = "deprecated()"
    assert rpc.call(contract, func_sig, [], "bool") == 0

def test_call_bool_arg(rpc, contract):
    func_sig = "isBlackListed(address)"
    args = ["0x956230E0340a8888513303A5B2ca06dA0e7567E5"]
    assert rpc.call(contract, func_sig, args, "bool") == 0

def test_call_int(rpc, contract):
    func_sig = "totalSupply()"
    assert rpc.call(contract, func_sig, [], "int") == 35283904986788565
    
def test_call_string(rpc, contract):
    func_sig = "name()"
    assert "Tether USD" in rpc.call(contract, func_sig, [], "string")

def test_call_shib(rpc):
    contract = "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"
    func_sig = "name()"
    args = []
    assert "SHIBA INU" in rpc.call(contract, func_sig, args, "string")

def test_call_shib_bal(rpc):
    shib = "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"
    func_sig = "balanceOf(address)"
    args = ["0x39bE25dDf6F7F5955bBDb8CC65Ca999746FD1a6A"]
    assert rpc.call(shib, func_sig, args, "int") > 0

def test_call_shib_allowance(rpc):
    shib = "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"
    func_sig = "allowance(address,address)"
    args = ["0x39bE25dDf6F7F5955bBDb8CC65Ca999746FD1a6A", "0x67ED47fCE644879Cb7e217663E79750522297b33"]
    assert rpc.call(shib, func_sig, args, "int") == 0
       
def test_call_bad_func(rpc, contract):
    with pytest.raises(InvalidFunction):
        func_sig = "bad_func()"
        rpc.call(contract, func_sig, [], "string")
    
