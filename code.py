import json
from web3 import Web3
# We DO NOT need any middleware for Sepolia

# --- 1. CONFIGURATION: FILL THESE 3 VALUES! ---

# (A) Get this from Alchemy or Infura (for the Ethereum Sepolia network)
SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

# (B) The private key of your test wallet (prefix with '0x')
# NEVER use a real wallet's private key!
ACCOUNT_PRIVATE_KEY = "0x20b2efb52d2a3e9975c485c40062c9ea15682023a70e595f851cfb2923cabdf5"

# (C) The address your contract was deployed to ON SEPOLIA
CONTRACT_ADDRESS = "0x5a24bAA368Db89d7aB4313f84AC63a8b4b422813"

# (D) The ABI (This should be the same as before)
CONTRACT_ABI = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "Payment",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "getBalance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "pay",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
] 

# --- 2. CONNECT TO THE BLOCKCHAIN ---

print("Connecting to Sepolia node...")
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

if not w3.is_connected():
    print("Error: Could not connect to the Sepolia node.")
    exit()

print(f"Connected! Chain ID: {w3.eth.chain_id}")

# Set up your account
my_account = w3.eth.account.from_key(ACCOUNT_PRIVATE_KEY)
w3.eth.default_account = my_account.address
print(f"Using account address: {my_account.address}")

# --- 3. LOAD THE SMART CONTRACT ---

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
print(f"Contract loaded at address: {CONTRACT_ADDRESS}")

# --- 4. DEFINE FUNCTIONS ---

def get_balance():
    """Reads and prints the contract's current balance."""
    print("\nAttempting to read contract balance...")
    try:
        balance_wei = contract.functions.getBalance().call()
        balance_eth = w3.from_wei(balance_wei, 'ether')
        print(f"Success! Contract balance: {balance_eth} ETH")
        return balance_eth
    except Exception as e:
        print(f"Error reading balance: {e}")

def send_payment(amount_eth_str):
    """Sends a payment transaction to the contract."""
    print(f"\nAttempting to send {amount_eth_str} ETH...")
    try:
        amount_wei = w3.to_wei(amount_eth_str, 'ether')
        
        tx = contract.functions.pay().build_transaction({
            'from': my_account.address,
            'value': amount_wei,
            'nonce': w3.eth.get_transaction_count(my_account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, ACCOUNT_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent. Hash: {tx_hash.hex()}")

        print("Waiting for transaction receipt...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"Success! Payment complete. Block: {tx_receipt.blockNumber}")
        get_balance() # Show new balance
    
    except Exception as e:
        print(f"Error sending payment: {e}")

def withdraw_funds():
    """Attempts to withdraw all funds (only owner can do this)."""
    print("\nAttempting to withdraw funds (must be owner)...")
    try:
        tx = contract.functions.withdraw().build_transaction({
            'from': my_account.address,
            'nonce': w3.eth.get_transaction_count(my_account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, ACCOUNT_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Withdrawal transaction sent. Hash: {tx_hash.hex()}")
        
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Success! Withdrawal complete. Block: {tx_receipt.blockNumber}")
        get_balance() # Show new balance

    except Exception as e:
        print(f"Error withdrawing funds (are you the owner?): {e}")


# --- 5. RUN THE SCRIPT ---

if __name__ == "__main__":

    # 1. Always check the balance first
    get_balance()

    # 2. Choose what to do. Uncomment *one* of the lines below:

    send_payment("0.001")

    #withdraw_funds()

    #SEPOLIA_RPC_URL="https://sepolia.gateway.tenderly.co/"
    #PRIVATE_KEY="0x20b2efb52d2a3e9975c485c40062c9ea15682023a70e595f851cfb2923cabdf5"
