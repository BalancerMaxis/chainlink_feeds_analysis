from web3 import Web3
from bal_tools import Web3RpcByChain, Web3Rpc
import json
import os


# Define the minimal ABIs as constants
RATE_PROVIDER_ABI = json.loads('[{"constant":true,"inputs":[],"name":"pricefeed","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]')
FEED_ABI = json.loads('[{"constant":true,"inputs":[],"name":"description","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
w3 = Web3RpcByChain(os.environ['DRPC_KEY'])

def main():
    ## Accepts a DRPC API key as an environment variable
    w3_by_chain=Web3RpcByChain(os.environ['DRPC_KEY'])
    # open registry.json
    # open a csv file with headers  chain, rate_provider, feed_address, feed_description
    # loop through all of the chains
    # look through all of the rate providers
    # check if each reate provider has chainlink as one of the warnings
    # if so, connect to it using web3, call: pricefeed(), which returns an address as a result
    # connect to the pricefeed contract using the address
    # call description() which returns a string
    # write the chain, rate_provider, feed_address, feed_description to the csv file
    # save and close the csv file

    with open('registry.json') as f:
        registry = json.load(f) # load the json file
    # open a csv file with headers  chain, rate_provider, feed_address, feed_description
    with open('feeds.csv', 'w') as f:
        f.write('chain,rate_provider,feed_address,feed_description\n')
        print('chain,rate_provider,feed_address,feed_description')
        for chain in registry:
            print(chain)
            for rate_provider_address, info in registry[chain].items():
                ## Handle Chainlink  tagged rate providers
                #if 'chainlink' in info['warnings'] or 'legacy' in info['warnings']:
                if True:
                    rate_provider_address = Web3.to_checksum_address(rate_provider_address)
                    print(f"{rate_provider_address}({info['warnings']})")
                    w3 = w3_by_chain[chain]
                    rate_provider = w3.eth.contract(rate_provider_address, abi=RATE_PROVIDER_ABI)
                    try:
                        pricefeed_address = Web3.to_checksum_address(rate_provider.functions.pricefeed().call())
                    except:
                        # Not chainlink
                        continue
                    pricefeed = w3.eth.contract(pricefeed_address, abi=FEED_ABI)
                    try:
                        feed_description = pricefeed.functions.description().call()
                    except:
                        # Feed without a description???
                        print(f"Warning: Feed {chain}:{pricefeed_address} from rate provider {rate_provider_address} has no description function")
                        continue
                    print(f'{chain},{rate_provider_address},{pricefeed_address},{feed_description}')
                    f.write(f'{chain},{rate_provider_address},{pricefeed_address},{feed_description}+{'(legacy)' if 'legacy' in info['warnings'] else ''}\n')
        f.close()

    # run main when called
if __name__ == '__main__':
    main()