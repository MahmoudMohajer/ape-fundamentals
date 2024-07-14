
from ape import project, accounts, networks, Contract
from dotenv import load_dotenv 
import os 
import json

# Load environment variables from .env file
load_dotenv()

def read_json(filename):
    with open(filename) as f:
        json_file = json.load(f)
    return json_file

def main():
    # Retrieve Sepolia RPC URL from environment variables
    sepolia_api_key = os.getenv("SEPOLIA_RPC_URL")
    passphrase= os.getenv("PASSPHRASE")
    
    # Construct network name string for Sepolia testnet
    network_name = f"ethereum:sepolia:{sepolia_api_key}"
    
    # Set up and use the specified network
    with networks.parse_network_choice(network_name) as network:
        # Load your account (make sure it's properly configured in Ape)
        account = accounts.load("ape_demo")
        account.set_autosign(True, passphrase)

        FAUCET_ADDRESS = "0xC959483DBa39aa9E78757139af0e9a2EDEb3f42D"
        faucet_abi = read_json("./.build/abi/faucet.json")
        faucet_contract = Contract(FAUCET_ADDRESS, abi=faucet_abi)

        # Minting USDC
        USDC_ADDRESS = "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8"
        amount = 10000 * 10**6

        tx = faucet_contract.mint(USDC_ADDRESS, account.address, amount, sender=account)

        print(f"USDC minted. Transaction hash: {tx.txn_hash}")

        # let's check our USDC balance 
        usdc_contract = Contract(USDC_ADDRESS)

        balance = usdc_contract.balanceOf(account.address) / 10**6
        print(f"USDC balance: {balance}")


