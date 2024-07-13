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
 

        # Load your account (make sure it's properly configured in Ape)
        sender = accounts.load("ape_demo")

        # Load the ERC20 token contract
        token_address = "0x782bcc137E81B53e4D50fF340688451278BD2575"  # Ape ERC20 token address 
        token = Contract(token_address) 

        # Define recipient and amount
        recipient = "0x54980B1504DB6782da1a0DA87B803bB0A7A1C00F"  # Replace with the actual recipient address
        amount = 1000 * 10**18  # Amount in wei (e.g., 1 token with 18 decimals)

        # Transfer the tokens
        tx = token.transfer(recipient, amount, sender=sender)

        print(f"Tokens sent. Transaction hash: {tx.txn_hash}")

if __name__ == "__main__":
    main()