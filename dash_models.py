import os
import base64
import io
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Bayon&family=Gruppo&family=Poppins:wght@300&display=swap",
    dbc.themes.BOOTSTRAP
]


models = [
    "Collections and Revenue",
    "Textual Analysis"
]

def create_collections_authors_figure(df):
    df = df.head(10)
    data = go.Bar(
            x=df['collections'],
            y=df['author'],
            meta=df['revenue'],
            hovertemplate="""<br>Author/Publication: %{y}
            <br>Collections:%{x}
            <br>Revenue:%{meta}
            <extra></extra>""",
            orientation='h',
            marker=dict(
                color=df['revenue'],  # Use 'Revenue' values as the color
                colorscale='agsunset',  # Choose a color scale
                cmin=df['revenue'].min(),
                cmax=df['revenue'].max(),
                colorbar=dict(
                    title='Revenue')))

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                bargap=0.1,
                width=550,
                height=400,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Authors',
                    title_standoff=40,
                    showgrid=False,
                    side='left'),
                xaxis=dict(
                    title='Collections',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': data, 'layout': layout})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


def gen_df_grouped_author(df):
    """ This function groups the dataframe by collections"""
    df = df[['author', 'price', 'collections', 'revenue']]
    df = df.groupby('author').sum().sort_values(
        by=['collections'],
        ascending=False)
    df['revenue'] = round(df['revenue'], 4)
    df.reset_index(inplace=True)
    return df


def gen_df_sort_collections(df):
    """ Make dataframe sorted by collections"""
    df = df.sort_values(by='collections', ascending=False)
    df['revenue'] = round(df['revenue'], 4)
    return df


def gen_df_sort_revenue(df):
    """ Make dataframe sorted by revenue"""
    df = df.sort_values(by='revenue', ascending=False)
    df['revenue'] = round(df['revenue'], 4)
    return df


# layout for collections and revenue
def gen_layout_col_rev(df):
    """ Generate Layout For the Collections and revenue Charts"""
    layout = html.Div([
                html.Div([
                    html.Div([
                        html.H1(
                            'Collections by Authors/Publications',
                            className="chart-title"
                            ),
                        dcc.Graph(
                            id="graph-collections-authors",
                            figure=create_collections_authors_figure(df))
                    ], className="collections-authors-container"),
                    html.Div([
                        html.H1(
                            'Collections by Entries',
                            className="chart-title"
                            ),
                        dcc.Graph(
                            id="graph-collections-entries",
                            figure=create_collections_authors_figure(df))
                    ], className="collections-authors-container"),
                ], className='collections-container'),
                html.Div([
                    html.Div([
                        html.H1('Revenue by Authors/Publications'),
                        dcc.Graph(
                            id="graph-revenue-authors",
                            figure=create_collections_authors_figure(df)
                            )
                    ]),
                    html.Div([
                        html.H1('Revenue by Entries'),
                        dcc.Graph(
                            id="graph-revenue-entries",
                            figure=create_collections_authors_figure(df)
                            )
                    ])
                ], className='revenue-container')
            ], className='fade-in')

    return layout


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
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                df_grouped_author = gen_df_grouped_author(df)
                df_collected = gen_df_sort_collections(df)
                df_revenue = gen_df_sort_revenue(df)
                if selected_model == "Collections and Revenue":
                    return gen_layout_col_rev(df_grouped_author)
                if selected_model == "Textual Analysis":
                    return layout_textual

    return app.server
