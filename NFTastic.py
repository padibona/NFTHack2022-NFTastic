import requests
import json
import streamlit as st
import pandas as pd


# Generic GET call
def get_api_call(url):
    response = requests.get(url)
    return response
# covalent API key (not ideal hardcoding) TODO - put into .env file and import into code from there.
key = "ckey_b40694ee8531497b822f4b9953f"

# pull initial chains data to populate the first dropdown on the left.
url_chains = "https://api.covalenthq.com/v1/chains/?quote-currency=USD&format=JSON&key=" + key
response_chains = get_api_call(url_chains)
response_chains_dict = response_chains.json()

# This writing to file area is ideally not needed, but we added this to get around flapping API stability (503's)
with open('chains.json', 'w') as file:
    json.dump(response_chains_dict, file)

with open('chains.json', 'r') as file:
    chains_dict = json.load(file)
    chains_list = chains_dict['data']['items']
    # List to populate dataframe for chains
    chains = []
    for x in chains_list:
        if x['name'] is not None:
            # Here are keys for each chain TODO - Possible pull out logo and any other info for sidebar. Use st.image from streamlit
            # dict_keys(['name', 'chain_id', 'is_testnet', 'db_schema_name', 'label', 'logo_url'])
            chain = x['label'], x['chain_id']
            chains.append(chain)
    df_chains = pd.DataFrame(chains, columns=['Chain', 'Chain ID'])

# Populate sidebar with the Dataframe of chain data
chain_option = st.sidebar.selectbox("Select Chain", df_chains)

# Create list of Dicts from the list of tuples - TODO - see if we can remove this step by manipulating data better earlier.
list_of_chain_dicts = []
for y in chains:
    chain_name = y[0]
    chain_id2 = y[1]
    list_of_chain_dicts.append({"Chain Name": chain_name, "Chain ID": chain_id2})

# Pull out the chain ID from the list of dicts if it matches the dropdown choice (dynamic)
chainz = next(item for item in list_of_chain_dicts if item["Chain Name"] == chain_option)
chain_id3 = chainz['Chain ID']

# Make the nft_market API call to pull the list of collections
url_nft_market = "https://api.covalenthq.com/v1/" + chain_id3 + "/nft_market/?key=" + key
print(url_nft_market)
response_collections = get_api_call(url_nft_market)
response_collections = response_collections.json()

# This writing to file area is ideally not needed, but we added this to get around flapping API stability (503's)
# TODO - remove file work here
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

# Populate sidebar with Collections Dataframe
collection_option = st.sidebar.selectbox("Select NFT Collection", df_collections)
# Title for App
st.title('NFTastic - NFT Analytics\n' + chain_option + ' - ' + collection_option)

#Add numeric input widget for data filters
days_count = st.sidebar.number_input('# of days for graph', min_value=1, max_value=365, value=30, step=1)

# Create list of Dicts from the list of tuples TODO - see if we can remove this step by manipulating data better earlier.
list_of_collections_dicts = []
for c in collections:
    collection_name = c[0]
    collection_address = c[1]
    list_of_collections_dicts.append({"Collection": collection_name, "Collection Contract Address": collection_address})
# Pull out collection contract address for nft_market/collection API call
collectionz = next(item for item in list_of_collections_dicts if item["Collection"] == collection_option)
collection_contract_address = collectionz['Collection Contract Address']

# Make nft_market/collection call to pull time series data for the collection chosen in the dropdown.
url_collection = "https://api.covalenthq.com/v1/" + chain_id3 + "/nft_market/collection/" + collection_contract_address + "/?key=" + key + "format=json"
print(url_collection)
collection_historical = get_api_call(url_collection)
collection_historical = collection_historical.json()

# Pull out Time series data
collection_data_list = collection_historical['data']['items']
df_collections = pd.DataFrame(collection_data_list, columns=['chain_id', 'collection_name','collection_address',
                                                             'collection_ticker_symbol', 'opening_date',
                                                             'volume_wei_day', 'volume_quote_day',
                                                             'average_volume_wei_day', 'average_volume_quote_day',
                                                             'unique_token_ids_sold_count_day', 'floor_price_wei_7d',
                                                             'floor_price_quote_7d', 'gas_quote_rate_day', 'quote_currency'])

# Display general info on sidebar - TODO add market cap, all time txn count, all time unique token id sales, unique wallet purchase price, and max price 
st.sidebar.write('NFT Symbol' + ' - ' + df_collections['collection_ticker_symbol'].iloc[0]) 
st.sidebar.write('Contract address' + ' - ' + df_collections['collection_address'].iloc[0]) 
st.sidebar.write('Launch Date' + ' - ' + df_collections['opening_date'].iloc[0])

# Pulled out what we saw as critical data, into a cleaner Dataframe
df_collections = df_collections[['collection_name', 'opening_date', 'collection_ticker_symbol', 'volume_quote_day',
                                 'average_volume_quote_day', 'unique_token_ids_sold_count_day',
                                 'floor_price_quote_7d', 'gas_quote_rate_day']]
df_collections = df_collections.set_index(['opening_date'])
days_count = 0 - days_count
df_collections = df_collections.iloc[days_count:]
print(df_collections.tail(days_count))
# fixing this due to bug in streamlit
#df_collections = df_collections.astype(str)
#print(df_collections.head(10))

# Function signature
# st.bokeh_chart(figure, use_container_width=False)
#
# Parameters
# figure (bokeh.plotting.figure.Figure)
#
# A Bokeh figure to plot.
#
# use_container_width (bool)
#
# If True, set the chart width to the column width. This takes precedence over Bokeh's native width value.
#
# To show Bokeh charts in Streamlit, call `st.bokeh_chart` (null)
#
# No description
#
# wherever you would call Bokeh's `show`. (null)
#
# title_string = 'Weekly Floor Prices over time for ' + df_collections['collection_name']
#
# # No description
# p = figure(
#     title=title_string,
#     x_axis_label='Date',
#     y_axis_label='Floor Prices')
#
# # x = dates
# x = df_collections['opening_date']
# print(x)
# # y = value
# y = df_collections['floor_price_quote_7d']
# print(y)
# p.line(x, y, legend_label='Trend', line_width=2)
# st.bokeh_chart(p, use_container_width=False)

# chart_data = pd.DataFrame(
#     y,
#     columns=['a', 'b', 'c'])
# st.line_chart(data=None, width=0, height=0, use_container_width=True)
st.write('7 Day Floor Price USD')
st.line_chart(df_collections['floor_price_quote_7d'], use_container_width=False, width=1000, height=500)
st.write('Volume USD')
st.line_chart(df_collections['volume_quote_day'], use_container_width=False, width=1000, height=500)
st.write('Average Volume USD')
st.line_chart(df_collections['average_volume_quote_day'], use_container_width=False, width=1000, height=500)
st.write('Number of Unique Tokens Sold')
st.line_chart(df_collections['unique_token_ids_sold_count_day'], use_container_width=False, width=1000, height=500)
st.write('Gas Rate USD')
st.line_chart(df_collections['gas_quote_rate_day'], use_container_width=False, width=1000, height=500)
