from ape import project, accounts, networks, Contract
from dotenv import load_dotenv 
import os 
import json
import time

# Load environment variables from .env file
load_dotenv()

def read_json(filename):
    with open(filename) as f:
        json_file = json.load(f)
    return json_file

def main():
    # Retrieve Sepolia RPC URL from environment variables
    sepolia_api_key = os.getenv("SEPOLIA_RPC_URL")
    
    # Construct network name string for Sepolia testnet
    network_name = f"ethereum:sepolia:{sepolia_api_key}"
    
    # Set up and use the specified network
    with networks.parse_network_choice(network_name) as network:
        # Load your account (make sure it's properly configured in Ape)
        account = accounts.load("ape_demo")

        ape_token_contract = Contract("0x782bcc137E81B53e4D50fF340688451278BD2575") # Replace with your contract address
        usdc_token_contract = Contract("0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8")

        UniswapV2Router_address = "0xC532a74256D3Db42D0Bf7a0400fEFDbad7694008"
        UniswapV2Router_abi = read_json("./.build/abi/UniswapV2Router.json")
        UniswapV2Router_contract = Contract(UniswapV2Router_address, abi=UniswapV2Router_abi)

        ape_amount = 100_000 * 10**18
        usdc_amount = 10_000 * 10**6
        ape_min_amount = 95_000 * 10**18
        usdc_min_amount = 9_500 * 10**6
        deadline = int(time.time()) + 60 * 20

        tx_ape_approve = ape_token_contract.approve(UniswapV2Router_address, ape_amount, sender=account)

        tx_usdc_approve = usdc_token_contract.approve(UniswapV2Router_address, usdc_amount, sender=account)

        tx_add_liquidity = UniswapV2Router_contract.addLiquidity(ape_token_contract.address,
                                                                 usdc_token_contract.address,
                                                                 ape_amount,
                                                                 usdc_amount,
                                                                 ape_min_amount,
                                                                 usdc_min_amount,
                                                                 account.address, # recipient of LP tokens
                                                                 deadline,
                                                                 sender=account
                                                                )

        print(f"Transaction hash: {tx_add_liquidity.txn_hash}")
        
         