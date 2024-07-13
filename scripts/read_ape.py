from ape import project, accounts, networks, Contract
from dotenv import load_dotenv 
import os 

# Load environment variables from .env file
load_dotenv()

def main():
    # Retrieve Sepolia RPC URL from environment variables
    sepolia_api_key = os.getenv("SEPOLIA_RPC_URL")
    
    # Construct network name string for Sepolia testnet
    network_name = f"ethereum:sepolia:{sepolia_api_key}"
    
    # Set up and use the specified network
    with networks.parse_network_choice(network_name) as network:
        # Load the ERC20 token contract
        token_address = "0x782bcc137E81B53e4D50fF340688451278BD2575"  # Ape ERC20 token address 
        token = Contract(token_address) 

        # Reading token details
        name = token.name()
        symbol = token.symbol()
        decimals = token.decimals()
        total_supply = token.totalSupply() / 10**decimals 
        balanceOf_this_address = token.balanceOf("0x54980B1504DB6782da1a0DA87B803bB0A7A1C00F") / 10**decimals

        print(f"Token name: {name}")
        print(f"Token symbol: {symbol}")
        print(f"Token decimals: {decimals}")
        print(f"Total supply: {total_supply}")
        print(f"balance of 0x54...0A7A1C00F: {balanceOf_this_address}")
