# curl -X GET https://api.covalenthq.com/v1/1/block_v2/5000000/ \
#                       -u ckey_b40694ee8531497b822f4b9953f:
# -H 'Content-Type: application/json'
# # The colon prevents curl from asking for a password.
# https://api.covalenthq.com/v1/1/nft_market/?key=ckey_b40694ee8531497b822f4b9953f

# Currently supports 1 for Ethereum Mainnet, 137 for Polygon/Matic Mainnet, 80001 for Polygon/Matic Mumbai Testnet, 56 for Binance Smart Chain, 43114 for Avalanche C-Chain Mainnet, 43113 for Fuji C-Chain Testnet, and 250 for Fantom Opera Mainnet.
import requests
import json
import streamlit as st
import numpy as np
import pandas as pd


def get_api_call(url):
    response = requests.get(url)
    return response


st.sidebar.title('NFTastic - NFT Analytics')
# TODO - Change static chain_id to a list of chain IDs pulled from the response_chains_dict variable
chain_id = "137"
key = "ckey_b40694ee8531497b822f4b9953f"

url_chains = "https://api.covalenthq.com/v1/chains/?quote-currency=USD&format=JSON&key=" + key


response_chains = get_api_call(url_chains)
response_chains_dict = response_chains.json()


with open('chains.json', 'w') as file:
    json.dump(response_chains_dict, file)

with open('chains.json', 'r') as file:
    chains_dict = json.load(file)
    #print(chains_dict.keys())
    #print(chains_dict['data'].keys())
    chains_list = chains_dict['data']['items']
    chains = []
    for x in chains_list:
        if x['name'] is not None:
            # print(x.keys())
            # dict_keys(['name', 'chain_id', 'is_testnet', 'db_schema_name', 'label', 'logo_url'])
            # print(x['collection_name'], x['collection_address'])
            chain = x['label'], x['chain_id']
            chains.append(chain)
    df_chains = pd.DataFrame(chains, columns=['Chain', 'Chain ID'])



# st.selectbox(label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)

chain_option = st.sidebar.selectbox("Chain", df_chains)
# Create list of Dicts from the list of tuples
list_of_chain_dicts = []
for y in chains:
    chain_name = y[0]
    chain_id2 = y[1]
    list_of_chain_dicts.append({"Chain Name": chain_name, "Chain ID": chain_id2})
# print(list_of_chain_dicts)
chainz = next(item for item in list_of_chain_dicts if item["Chain Name"] == chain_option)
chain_id3 = chainz['Chain ID']
print(chain_id3)
# list(filter(lambda chain: chain['Chain Name'] == chain_option, list_of_chain_dicts))
# list(filter(lambda person: person['name'] == 'Pam', people))

url_nft_market = "https://api.covalenthq.com/v1/" + chain_id3 + "/nft_market/?key=" + key
print(url_nft_market)
response_collections = get_api_call(url_nft_market)
response_collections = response_collections.json()

with open('nft_market.json', 'w') as file:
    json.dump(response_collections, file)

with open('nft_market.json', 'r') as file:
    data_dict = json.load(file)
    items_list = data_dict['data']['items']
    collections = []
    for x in items_list:
        if x['collection_name'] is not None:
            # print(x['collection_name'], x['collection_address'])
            collection = x['collection_name'], x['collection_address']
            collections.append(collection)
    df_collections = pd.DataFrame(collections, columns=['Collection', 'Collection Contract Address'])
    # print(df_collections)
collection_option = st.sidebar.selectbox("NFT Collections", df_collections)
