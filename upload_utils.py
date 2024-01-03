""" This script as several functions to a create a datatoken and submit it
with a price in the Ocean Market"""
import csv
from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.ocean.util import to_wei


# Configuration for Polygon - Mumbai
def make_config(token, net='mumbai'):
    """ This function uses an RPC to make a configuration, which is wrapped
    with the Ocean class. It returns an OCEAN object."""
    networks = {
        'mumbai': "https://polygon-mumbai.infura.io/v3/",
        'polygon': " https://polygon-mainnet.infura.io/v3/"
    }
    config = get_config_dict(f"{networks[net]}{token}")
    ocean = Ocean(config)
    ocean_obj = ocean.OCEAN_token
    return ocean, ocean_obj


# Create data_NFT, datatoken and ddo
def create_asset_from_arweave(ocean, name, publish_address, arweave_id,
                              author, description, tags):
    """ This function creates a data NFT, a datatoken and a ddo from several
    inputs using the ocean instance. The datatoken is a Arweave asset """

    # create metadata
    metadata = ocean.assets.__class__.default_metadata(
        name, {"from": publish_address})
    metadata.update({
        'description': description,
        'author': author,
        'tags': tags,
    })

    # create arweave asset
    data_nft, datatoken, ddo = ocean.assets.create_arweave_asset(
        name, arweave_id, {"from": publish_address}, metadata=metadata)

    return data_nft, datatoken, ddo


# Post on Ocean Market
def post_for_sale(ocean_obj, datatoken, publish_address, price, n_datatokens):
    """" This function submits the datatoken to the Ocean Market at a certain
    price. """
    exchange = datatoken.create_exchange(
        {"from": publish_address}, to_wei(price), ocean_obj.address)
    datatoken.mint(
        publish_address, to_wei(n_datatokens), {"from": publish_address})
    datatoken.approve(
        exchange.address, to_wei(n_datatokens), {"from": publish_address})
    return exchange


# append to csv and return dictionary
def save_data(datatoken, exchange, output_path):
    """ This function creates a dictionary based on data from the datatoken
    and the exchange objects. Saves a list of details to a csv file and returns
    the dictionary."""

    details = {}
    details['datatoken_title'] = datatoken.name()
    details['datatoken_address'] = exchange.details.datatoken
    details['price'] = float(exchange.details.bt_supply*10**(-18))
    details['datatoken_owner'] = exchange.details.owner
    with open(output_path, mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(list(details.values()))

    return details
