from web3 import Web3
from Deploy import deploy_contract
import os


contract_file = "./src/newContract.sol"
account = os.getenv("ANVIL_ACCOUNT")
private_key = os.getenv("ANVIL_PRIVATE_KEY")
provider = os.getenv("LOCAL_PROVIDER")

chain_id = 31337
    
connection = Web3(Web3.HTTPProvider(provider))
contract_address, abi = deploy_contract(contract_file, "newContract", account, private_key, provider, chain_id)



new_Contract = connection.eth.contract(address=contract_address, abi = abi)
nonce = connection.eth.get_transaction_count(account)
new_id_value = 5341
transaction = new_Contract.functions.updateID(new_id_value).build_transaction(
    {
            "chainId":chain_id,
            "gasPrice":connection.eth.gas_price,
            "from":account,
            "nonce":nonce
    }
)

signed_txn = connection.eth.account.sign_transaction(transaction, private_key = private_key)
print("Updated sotred value ")
tx_hash = connection.eth.send_raw_transaction(signed_txn.raw_transaction)

tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
print("Updated")

updated_value = new_Contract.functions.viewMyId().call()
print("Updtaed value" , updated_value) 