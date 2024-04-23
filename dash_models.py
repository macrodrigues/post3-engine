""" This script instantiates the route containin the models and dashboards """
# pylint: disable=W0612
# pylint: disable=W0603
# pylint: disable=W0602
import base64
import io
from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from models.collections_n_revenue import gen_layout_col_rev
from models.collections_n_revenue import gen_df_sort_collections
from models.collections_n_revenue import gen_df_sort_revenue
from models.collections_n_revenue import create_collections_authors_figure
from models.collections_n_revenue import create_collections_entries_figure
from models.collections_n_revenue import create_revenue_authors_figure
from models.collections_n_revenue import create_revenue_entries_figure
from models.collections_n_revenue import gen_table
from models.textual_analysis import gen_layout_textual
from models.explorer import gen_layout_explorer, gen_table_explorer

# VARIABLES
df = pd.DataFrame()
year = datetime.today().year
footer = f"Running in {year}. Built with ❤️ for Web3 enthusiasts."

external_stylesheets = [
    "https://fonts.googleapis.com"
    "/css2?family=Bayon&family=Gruppo&family=Poppins:wght@300&display=swap",
    dbc.themes.BOOTSTRAP
]


def dash_app_models(flask_app, path):
    """Launch Dash app on Flask server.

    Route for models page.

    """
    app = Dash(
        __name__,
        server=flask_app,  # rendered by the flask app
        url_base_pathname=path,  # the flask route for this page
        external_stylesheets=external_stylesheets  # bootstrap components
    )

    app._favicon = "assets/favicon.ico"
    app.title = 'Post3 Engine'

    app.layout = html.Div([
                    html.Div([
                        html.Div([
                            html.A([
                                html.Img(
                                    src='assets/post3_logo.png',
                                    className='img-style')], href='/')
                            ], className='image-container'),
                        html.H1([
                            'Post',
                            html.Span('3', className="three-title"),
                            html.Span('Engine', className="engine-word")
                        ], className="engine-title")
                    ], className="logo-title-container"),
                    html.Div([
                        dcc.Upload(
                            id='upload-dataset',
                            className='upload-specs',
                            children=html.Div([
                                'Submit a ',
                                html.Span(
                                    children='dataset',
                                    className='dataset-string')])
                        ),
                        html.H1(
                            "Choose a Model",
                            className="title-models"
                        ),
                        dcc.Dropdown(
                            id='models-dropdown',
                            options=[
                                'Explorer',
                                "Collections & Revenue",
                                'Textual Analysis'
                                ],
                            className="dropdown-models"
                        ),
                    ], className="upload-container"),
                    dcc.Loading([
                        html.Div(id='dynamic-layout')],
                        id="loading-output",
                        className='loading-element',
                        type="circle"
                    ),
                    html.Div([
                        html.Footer([
                            html.P(footer)
                        ])
                    ], className="footer-section")
                ], className='fade-in')

    @app.callback(
        Output('dynamic-layout', 'children'),
        [
            Input(
                component_id='models-dropdown',
                component_property='value'),
            Input(
                component_id='upload-dataset',
                component_property='filename'),
            Input(
                component_id='upload-dataset',
                component_property='contents')])
    def upload_file(selected_model, uploaded_filename, uploaded_content):
        """ This function renders a layout for the selected model. It takes the
        model and the dataset as inputs."""
        if uploaded_filename is not None and uploaded_content is not None:
            content_type, content_string = uploaded_content.split(',')
            decoded = base64.b64decode(content_string)
            if 'json' in uploaded_filename:
                global df
                df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
                models = {
                    'Explorer': gen_layout_explorer(df),
                    "Collections & Revenue": gen_layout_col_rev(df),
                    "Textual Analysis": gen_layout_textual(df)
                }

                return models[selected_model]

    @app.callback(
        [
            Output('graph-collections-authors', 'figure'),
            Output('graph-collections-entries', 'figure'),
            Output('graph-revenue-authors', 'figure'),
            Output('graph-revenue-entries', 'figure'),
            Output('table-collections', 'children'),
            Output('table-revenue', 'children'),
        ],
        Input('slider-collections-authors', 'value')
    )
    def update_collections_authors_figure(selected_date_range):
        """ This function updates the charts and tables, by using a
        Range Slider as input. """
        global df
        df_collected = gen_df_sort_collections(df)
        df_revenue = gen_df_sort_revenue(df)
        start = selected_date_range[0]
        end = selected_date_range[-1]
        dates = sorted(df['date'].unique())
        dates = dates[start:end]
        filt_df_collected = df_collected[
            df_collected['date'].isin(dates)]
        filt_df_revenue = df_revenue[
            df_revenue['date'].isin(dates)]

        return [
            create_collections_authors_figure(filt_df_collected),
            create_collections_entries_figure(filt_df_collected),
            create_revenue_authors_figure(filt_df_revenue),
            create_revenue_entries_figure(filt_df_revenue),
            gen_table(filt_df_collected),
            gen_table(filt_df_revenue),
            ]

    @app.callback(
        [
            Output('table-tags', 'children'),
        ],
        Input('tags-dropdown-explorer', 'value')
    )
    def update_articles_explorer(selected_tags):
        """ This function updates the table in the explorer to showcase the
        articles according to the selected tag/tags"""
        global df

        # Filter the DataFrame to select only the rows containing the tags
        filtered_df = df[df['tags'].apply(
            lambda x: any(tag in x for tag in selected_tags))]

        return [gen_table_explorer(gen_df_sort_collections(filtered_df))]

    return app.server
