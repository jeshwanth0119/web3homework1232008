from web3 import Web3
from Compile import Compile_Solidity
from typing import Tuple
import os



def deploy_contract(contract_file: str, contract_name: str, account: str, private_key: str, provider: str, chain_id : int ) : 


 
    compiled_sol = Compile_Solidity(contract_file)

    #Get the ABI and Byte code
    abi = compiled_sol["contracts"][contract_file][contract_name]["abi"]
    byte_code = compiled_sol["contracts"][contract_file][contract_name]["evm"]["bytecode"]["object"]

    connection = Web3(Web3.HTTPProvider(provider))
   
    

    contract = connection.eth.contract(abi=abi, bytecode=byte_code)
    nonce = connection.eth.get_transaction_count(account)


    transaction = contract.constructor().build_transaction(
        {
            "chainId":chain_id,
            "gasPrice":connection.eth.gas_price,
            "from":account,
            "nonce":nonce
        }
    )

    signed_txn = connection.eth.account.sign_transaction(transaction, private_key = private_key)

    tx_hash = connection.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
    return (tx_receipt.contractAddress, abi)
if __name__ == "__main__":
     contract_file = "./src/newContract.sol"
     account = os.getenv("ANVIL_ACCOUNT")
     private_key = os.getenv("ANVIL_PRIVATE_KEY")
     provider = os.getenv("LOCAL_PROVIDER").format("holesky")
     print(provider)
     chain_id = 31337
     contract_address, abi = deploy_contract(contract_file,"newContract",account,private_key,provider,chain_id)
     print(f"Contract deployed at {contract_address}")