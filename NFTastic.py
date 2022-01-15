# curl -X GET https://api.covalenthq.com/v1/1/block_v2/5000000/ \
#                       -u ckey_b40694ee8531497b822f4b9953f:
# -H 'Content-Type: application/json'
# # The colon prevents curl from asking for a password.
# https://api.covalenthq.com/v1/1/nft_market/?key=ckey_b40694ee8531497b822f4b9953f

# Currently supports 1 for Ethereum Mainnet, 137 for Polygon/Matic Mainnet, 80001 for Polygon/Matic Mumbai Testnet, 56 for Binance Smart Chain, 43114 for Avalanche C-Chain Mainnet, 43113 for Fuji C-Chain Testnet, and 250 for Fantom Opera Mainnet.
import requests
import json
import streamlit as st


def nft_market(url):
    response = requests.get(url)
    return response


st.title('NFTastic - NFT Analytics')
chain_id = "137"
key = "ckey_b40694ee8531497b822f4b9953f"

url = "https://api.covalenthq.com/v1/" + chain_id + "/nft_market/?key=" + key

response = nft_market(url)
response = response.json()
print(type(response))
#print(response)
#balances = cov.ClassA.get_token_balances_for_address(chain_id, "0x55EA3A3E91457591878ea48C87E12C9FF91E69De", nft=True, )
#print(balances.content)
with open('nft_market_polygon.json', 'w') as file:
    json.dump(response, file)

with open('nft_market_polygon.json', 'r') as file:
    data_dict = json.load(file)
    items_list = data_dict['data']['items']
    collections = []
    for x in items_list:
        if x['collection_name'] !=None:
            print(x['collection_name'], x['collection_address'])
            line = x['collection_name'], x['collection_address']
            collections.append(line)
    print(collections)
    print(type(collections))

st.selectbox
