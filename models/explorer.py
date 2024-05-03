""" Script to launch the explorer search engine """
from dash import html, dcc
import dash_bootstrap_components as dbc


def gen_df_sort_collections(df):
    """ Make dataframe sorted by collections"""
    df = df.sort_values(by='collections', ascending=False)
    df['revenue'] = round(df['revenue'], 4)
    return df


def gen_table_explorer(df):
    """ Generate table with the entries and hyperlinks"""

    categories_dict = {
        i+1: {'title': title,
              'link': link,
              'author': author,
              'author_link': author_link}
        for i, (title, link, author, author_link)
        in enumerate(zip(
            df.head(30).title.values,
            df.head(30).link.values,
            df.head(30).author.values,
            df.head(30).author_link.values))}

    rows = []
    for k, v in categories_dict.items():
        row = html.Tr([
            dbc.Button([
                html.Td(
                    html.P(
                        v['title'],
                        style={'color': 'white'}),
                    style={'text-align': 'left', 'width': '200px'}),
                html.Td(
                    children=v['author'],
                    style={
                        'color': 'rgba(255, 172, 5, 1.00)',
                        'text-align': 'right'})],
                href=v['link'],
                target='_blank',
                className='button-explorer-table')
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
                        html.P(
                            'Select one or more tags',
                            className='tags-search-title'),
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
