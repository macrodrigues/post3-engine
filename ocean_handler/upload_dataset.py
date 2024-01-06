# pylint: disable=E1120
import os
import dotenv
from eth_account.account import Account
from upload_utils import make_config, create_asset_from_arweave, post_for_sale
PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(f"{PATH}/keys.env")

# VARIABLES OF DATASET
TITLE = "Post3 Dataset | Mirror Entries from Week 52 2023"
AUTHOR = "Post3"
DESCRIPTION = "Some dataset"
TAGS = ['dataset', 'data-nft', 'data-analysis', 'data-mining']


# create ocean objects
ocean, ocean_obj = make_config(
    os.getenv('INFURA_TOKEN'),
    'mumbai')

# call address
my_private_key = os.getenv('REMOTE_TEST_PRIVATE_KEY1')
my_address = Account.from_key(private_key=my_private_key)

if __name__ == '__main__':
    # create dataset
    data_nft, datatoken, ddo = create_asset_from_arweave(
        ocean,
        name=TITLE,
        publish_address=my_address,
        arweave_id=os.getenv('ARWEAVE_ID'),
        author=AUTHOR,
        description=DESCRIPTION,
        tags=TAGS)

    # post for a price
    post_for_sale(
        ocean_obj,
        datatoken,
        publish_address=my_address,
        price=100,
        n_datatokens=10)
