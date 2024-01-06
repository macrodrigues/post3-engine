# Post3 Engine

![alt text](static/images/post3_logo.png)

[Post3](https://bento.me/post3) is a project that aims at exploring Writing NFTs from web3 Publishing Platforms like [Mirror](https://mirror.xyz/post3.eth) and [Paragraph](https://paragraph.xyz/@post3).

Post3 publishes weekly insightful reports about what happened in the web3 realm. For that, it uses Web Scraping and GraphQL to extract data from [Arweave](https://www.arweave.org/). The data is cleaned and uploaded to the [Ocean Market](https://market.oceanprotocol.com/profile/post3.eth) so other analysts can acquire the datasets and draw their own conclusions.

You can learn more about Post3, by visiting its [landing page](https://bento.me/post3).

Post3 Engine, is a platform to upload Ocean Datasets and obtain interactive dashboards, for a better visualization experience.


### The Flow

The datasets are extracted using GraphQL and Web Scraping techniques. They are cleaned and uploaded to Arweave through [Akord](https://v2.akord.com/) and the [Ocean Uploader](https://uploader.oceanprotocol.com/).

Once uploaded, the scripts in the **ocean_handler** folder are used to seamlessly  submit the dataset for a specific price in the Ocean Marketplace, without the need to open the marketplace on a browwser.

By using **Flask** and **Dash Plotly** a platform was created (Post3 Engine) from where the users can easily buy a dataset and then pick one of the available models to draw insights from it.

In the future, premium models can be bought in the Ocean Market and used in the Post3 Engine.


### Ocean Tools

The goal of Post3 is to harness the power of Writing NFTs thourgh dashboarding and other tools. For that it needs datasets. [Ocean Protocol](https://oceanprotocol.com/) seemed the most obvious platform to upload the datasets, since it is the main one for web3 projects and presents developer tools that ease the process of uploading.

At the moment Post3 only submits one or two datasets per week, but more are on the radar, and for that automation is key.

You can use the set of functions built in Post3 Engine in your own datasets, you only need to adapt certain parameters.

Let's take a look at the different functions in the **upload_utils.py** file:

- **make_config():** this function uses Infura's RPC to make a configuration and creates ocean objects to perform further actions. To use it you need an infura token.

- **create_asset_from_arweave():** this function creates the data NFT in the Ocean Market without a price and takes several parameters such as the author's name, the title of the asset, the description, tags, the publish address and the arweave TX ID.

- **post_for_sale():** once submitted, we need to make the asset available to buy. For that we use the create_exchange() function from the ocean library to set the datatoken at a specific price. Then we mint it and approve it.

- **save_data():** this function saves some key parameters from the datatoken to a .csv file. This can be useful for further work, for instance to create a database of the assets that were submitted and/or acquired.

In the **upload_dataset.py**, we basically use the functions already mentioned plus the **eth_account** library to call the publishing address. By running this script we upload the dataset to the Ocean Market.
