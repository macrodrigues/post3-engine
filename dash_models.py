import os
import base64
import io
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from collections_n_revenue import gen_layout_col_rev
from collections_n_revenue import gen_df_sort_collections, gen_df_sort_revenue
from collections_n_revenue import create_collections_authors_figure
from collections_n_revenue import create_collections_entries_figure
from collections_n_revenue import create_revenue_authors_figure
from collections_n_revenue import create_revenue_entries_figure, gen_table
from collections_n_revenue import create_pie_networks


# DUMMY DF
df = pd.DataFrame()

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Bayon&family=Gruppo&family=Poppins:wght@300&display=swap",
    dbc.themes.BOOTSTRAP
]

models = [
    "Collections and Revenue",
    "Textual Analysis"
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

    # layout for collections and revenue
    layout_textual = html.Div([
                        html.H1('come-me as flores')
                    ], className='fade-in')

    app.layout = html.Div([
                    html.Div([
                        html.Div([
                            html.Img(
                                src='assets/post3_logo.png',
                                className='img-style')
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
                                'Submit the ',
                                html.Span(
                                    children='Ocean Dataset',
                                    className='ocean-dataset-string')])
                        ),
                        html.H1(
                            "Pick a Model",
                            className="title-models"
                        ),
                        dcc.Dropdown(
                            id='models-dropdown',
                            options=models,
                            value=models[0],
                            className="dropdown-models"
                        ),
                    ], className="upload-container"),
                    html.Div(id='dynamic-layout')
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
        if uploaded_filename is not None and uploaded_content is not None:
            content_type, content_string = uploaded_content.split(',')
            decoded = base64.b64decode(content_string)
            if 'csv' in uploaded_filename:
                global df
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                if selected_model == "Collections and Revenue":
                    return gen_layout_col_rev(df)
                if selected_model == "Textual Analysis":
                    return layout_textual


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

    return app.server
