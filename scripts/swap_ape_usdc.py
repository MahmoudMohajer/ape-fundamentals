from ape import project, accounts, networks, Contract
from dotenv import load_dotenv 
import os 
import json
import time
from decimal import Decimal

# Load environment variables from .env file
load_dotenv()

def read_json(filename):
    with open(filename) as f:
        json_file = json.load(f)
    return json_file

def calculate_amount_out_min(router, amount_in, path, slippage_tolerance=0.005):
    amounts = router.getAmountsOut(amount_in, path)
    expected_amount_out = amounts[-1]
    slippage_amount = int(expected_amount_out * Decimal(slippage_tolerance))
    return expected_amount_out - slippage_amount


def main():
    sepolia_api_key = os.getenv("SEPOLIA_RPC_URL")
    passphrase= os.getenv("PASSPHRASE")
    
    network_name = f"ethereum:sepolia:{sepolia_api_key}"
    
    with networks.parse_network_choice(network_name) as network:
        account = accounts.load("ape_demo")
        account.set_autosign(True, passphrase)

        ape_contract = Contract("0x782bcc137E81B53e4D50fF340688451278BD2575")
        usdc_contract = Contract("0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8")

        UniswapV2Router_address = "0xC532a74256D3Db42D0Bf7a0400fEFDbad7694008"
        UniswapV2Router_abi = read_json("./.build/abi/UniswapV2Router.json")
        UniswapV2Router_contract = Contract(UniswapV2Router_address, abi=UniswapV2Router_abi)

        amountIn = 10_000 * 10**18
        path = [ape_contract.address, usdc_contract.address]
        # Get the expected amount out and apply slippage tolerance
        amountOutMin = calculate_amount_out_min(UniswapV2Router_contract, amountIn, path)

        # Print the current price
        expected_out = UniswapV2Router_contract.getAmountsOut(10**18, path)[-1]
        price_per_token = expected_out / 10**6  
        print(f"Current price: 1 APE = {price_per_token} USDC")

        deadline = int(time.time()) + 60 * 20

        previous_ape_balance = ape_contract.balanceOf(account.address) / 10**18
        previous_usdc_balance = usdc_contract.balanceOf(account.address) / 10**6

        # Approve if needed
        allowance = ape_contract.allowance(account.address, UniswapV2Router_address)
        if allowance < amountIn:
            tx = ape_contract.approve(UniswapV2Router_address, amountIn, sender=account)

        # Swap transaction
        tx = UniswapV2Router_contract.swapExactTokensForTokens(amountIn,
                                                               amountOutMin,
                                                                path,
                                                                account.address,
                                                                deadline, 
                                                                sender=account)

        print(f"Swap completed. Transaction hash: {tx.txn_hash}")

        new_ape_balance = ape_contract.balanceOf(account.address) / 10**18
        new_usdc_balance = usdc_contract.balanceOf(account.address) / 10**6

        print(f"Previous APE balance: {previous_ape_balance}")
        print(f"Previous USDC balance: {previous_usdc_balance}")
        print(f"New APE balance: {new_ape_balance}")
        print(f"New USDC balance: {new_usdc_balance}")
        print(f"Swapped {previous_ape_balance - new_ape_balance} APE for {new_usdc_balance - previous_usdc_balance} USDC")