# Import necessary modules from ape framework and other libraries
from ape import project, accounts, networks
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
        # Load a pre-existing account named "ape_demo"
        account = accounts.load("ape_demo")

        # Calculate initial token supply: 1 million tokens with 18 decimal places
        initial_supply = 1_000_000 * 10**18 # minting 1 million tokens
        
        # Deploy the ERC20 contract named "Ape" with the initial supply
        erc20_contract = account.deploy(project.Ape, initial_supply) 

        # Print the address of the deployed contract
        print(f"Contract deployed at {erc20_contract.address}")

# Execute main() function if this script is run directly
if __name__ == "__main__":
    main()