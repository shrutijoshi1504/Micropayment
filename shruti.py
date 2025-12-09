from web3 import Web3

# 1. SETUP
SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"  # Or your Alchemy URL
# YOUR REAL PRIVATE KEY (Add 0x if missing)
ACCOUNT_PRIVATE_KEY = "20b2efb52d2a3e9975c485c40062c9ea15682023a70e595f851cfb2923cabdf5"
# SAME ADDRESS AS HTML
CONTRACT_ADDRESS = "0x0d50184B87354eD6B314CB33AA6aA3DFCF42D33A"

CONTRACT_ABI = [
    {"inputs": [], "name": "getBalance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "pay", "outputs": [], "stateMutability": "payable", "type": "function"}
]

# 2. CONNECT
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
my_account = w3.eth.account.from_key(ACCOUNT_PRIVATE_KEY)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

print(f"--- Python Payment Bot ---")
print(f"Bot Address: {my_account.address}")


# 3. SEND PAYMENT
def send_payment():
    amount_eth = 0.0001
    print(f"Sending {amount_eth} ETH to contract...")

    tx = contract.functions.pay().build_transaction({
        'from': my_account.address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'nonce': w3.eth.get_transaction_count(my_account.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, ACCOUNT_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Tx Sent! Hash: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Success! Money deposited.")


if __name__ == "__main__":
    send_payment()