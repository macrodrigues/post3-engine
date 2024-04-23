""" Script to launch the explorer search engine """
from dash import html, dcc


def gen_df_sort_collections(df):
    """ Make dataframe sorted by collections"""
    df = df.sort_values(by='collections', ascending=False)
    df['revenue'] = round(df['revenue'], 4)
    return df


def gen_table_explorer(df):
    """ Generate table with the entries and hyperlinks"""
    categories_dict = {
        i+1: {'title': title, 'link': link}
        for i, (title, link)
        in enumerate(zip(
            df.head(30).title.values, df.head(30).link.values))}

    rows = []
    for k, v in categories_dict.items():
        row = html.Tr([
            html.Td(
                str(k) + ": ",
                style={'color': 'rgba(255, 172, 5, 1.00)'}),
            html.Td(
                html.A(
                    v['title'], href=v['link'],
                    target='_blank',
                    style={'color': 'white'}))
        ])

        rows.append(row)

    table_body = [
        html.Tbody(rows, className='table-body')]

    return table_body


def gen_layout_explorer(df):
    """ Generate Layout for the Explorer"""

    df = gen_df_sort_collections(df)

    # Step 1: Extract all the tags from the 'Tags' column
    all_tags = df['tags'].explode()

    # Step 2: Count the occurrences of each tag
    tag_counts = all_tags.value_counts()

    # Step 3: Sort the tags based on their occurrences
    sorted_tags = tag_counts.index.tolist()

    # Step 4: Select the top 30 tags
    top_30_tags = sorted_tags[:50]

    layout = dcc.Loading([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='tags-dropdown-explorer',
                            multi=True,
                            options=top_30_tags,
                            className="dropdown-models"
                        ),
                    ], className="upload-container"),
                    html.Div([
                        html.Div([
                            html.Table(
                                gen_table_explorer(df),
                                id='table-tags',
                                style={
                                    'width': '80vw',
                                    'height': '70vw',
                                    'margin': 'auto'}),
                        ])
                    ], className='collections-container'),
                ], className='fade-in column')
            ], id="loading-sub-layout", type="circle")

    return layout
