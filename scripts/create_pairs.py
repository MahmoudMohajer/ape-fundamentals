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
    
    # Construct network name string for Sepolia testnet
    network_name = f"ethereum:sepolia:{sepolia_api_key}"
    
    # Set up and use the specified network
    with networks.parse_network_choice(network_name) as network:
        # Load your account (make sure it's properly configured in Ape)
        account = accounts.load("ape_demo")

        Ape_address = "0x782bcc137E81B53e4D50fF340688451278BD2575"
        USDC_address = "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8"
        
        UniswapV2factory_address = "0x7E0987E5b3a30e3f2828572Bb659A548460a3003"
        UniswapV2Factory_abi = read_json("./.build/abi/UniswapV2Factory.json") 
        UniswapV2Factory_contract = Contract(UniswapV2factory_address, abi=UniswapV2Factory_abi) 

        tx = UniswapV2Factory_contract.createPair(Ape_address, USDC_address, sender=account)

        print(f"Pair created. Pair Address: {UniswapV2Factory_contract.getPair(Ape_address, USDC_address)}")




