from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_URL')))
        with open('contract_abi.json') as f:
            self.abi = json.load(f)
        self.contract = self.w3.eth.contract(
            address=os.getenv('CONTRACT_ADDRESS'),
            abi=self.abi
        )
        self.account = os.getenv('DEPLOYER_ADDRESS')
        self.private_key = os.getenv('DEPLOYER_PRIVATE_KEY')
        self.chain_id = int(os.getenv('CHAIN_ID', 1337))  # Default Ganache chain ID

    def log_computation(self, data_hash, result_hash):
        data_hash_bytes = bytes.fromhex(data_hash) if data_hash != "0"*64 else bytes(32)
        result_hash_bytes = bytes.fromhex(result_hash) if result_hash != "0"*64 else bytes(32)
        
        tx_dict = {
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': self.chain_id
        }
        
        tx = self.contract.functions.logComputation(
            data_hash_bytes,
            result_hash_bytes
        ).build_transaction(tx_dict)
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        return self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    def verify_computation(self, data_hash, result_hash):
        """Verify if computation results match on blockchain"""
        try:
            data_hash_bytes = bytes.fromhex(data_hash)
            result_hash_bytes = bytes.fromhex(result_hash)
            return self.contract.functions.verifyComputation(
                data_hash_bytes,
                result_hash_bytes
            ).call()
        except Exception as e:
            print(f"Verification error: {str(e)}")
            return False