import json


def read_json(filename):
    with open(filename) as f:
        json_string = json.load(f)
    result = [json.loads(abi_string) for abi_string in json_string]
    return result

def get_functions_from_abi(token_abi):
    # Get the ABI from the contract
    abi = token_abi 
    
    # Filter for function entries in the ABI
    functions = [item for item in token_abi if item['type'] == 'function']
    
    return functions

def is_read_function(func):
    # Check if the function is constant, view, or pure
    return func.get('stateMutability') in ['view', 'pure'] or func.get('constant', False)

def main():
   
    token_abi = read_json("./.build/abi/Ape.json")

        # Get functions from ABI
    functions = get_functions_from_abi(token_abi)

    print("Contract functions:")
    for func in functions:
        name = func['name']
        inputs = ', '.join([f"{inp['type']} {inp['name']}" for inp in func['inputs']])
        outputs = ', '.join([out['type'] for out in func['outputs']])
        read_or_write = "Read" if is_read_function(func) else "Write"
        print(f"- {name}({inputs}) returns ({outputs}) - {read_or_write}")

if __name__ == "__main__":
    main()