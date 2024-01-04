import os
import base64
import io
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


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


def create_collections_authors_figure(df):
    """ Create collections per authors/publications bar plot"""
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
                colorscale='peach',  # Choose a color scale
                cmin=df['revenue'].min(),
                cmax=df['revenue'].max(),
                colorbar=dict(
                    thickness=15,
                    title='Revenue (ETH)')))

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


def create_collections_entries_figure(df):
    """ Create collections per entries bar plot"""
    df = df.head(10)

    short_labels = [
        title[:10] + '...' if len(title) > 10
        else title for title in df['title']]
    data = go.Bar(
            x=df['collections'],
            y=short_labels,
            meta=df['author'],
            customdata=df['title'],
            hovertemplate="""<br>Title: %{customdata}
            <br>Author: %{meta}
            <br>Collections: %{x}
            <extra></extra>""",
            orientation='h',
            marker=dict(
                color=df['revenue'],  # Use 'Revenue' values as the color
                colorscale='peach',  # Choose a color scale
                cmin=df['revenue'].min(),
                cmax=df['revenue'].max(),
                colorbar=dict(
                    thickness=15,
                    title='Revenue (ETH)')))

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                bargap=0.1,
                width=550,
                height=400,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Entries',
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


def create_revenue_authors_figure(df):
    """ Create revenue per authors/publications bar plot"""
    df = df.head(10)
    data = go.Bar(
            x=df['revenue'],
            y=df['author'],
            meta=df['collections'],
            hovertemplate="""<br>Author/Publication: %{y}
            <br>Revenue:%{x}
            <br>Collections:%{meta}
            <extra></extra>""",
            orientation='h',
            marker=dict(
                color=df['collections'],
                colorscale='peach',  # Choose a color scale
                cmin=df['collections'].min(),
                cmax=df['collections'].max(),
                colorbar=dict(
                    thickness=15,
                    title='Collections')))

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
                    title='Revenue (ETH)',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': data, 'layout': layout})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


def create_revenue_entries_figure(df):
    """ Create revenue per entries bar plot"""
    df = df.head(10)

    short_labels = [
        title[:10] + '...' if len(title) > 10
        else title for title in df['title']]
    data = go.Bar(
            x=df['revenue'],
            y=short_labels,
            meta=df['author'],
            customdata=df['title'],
            hovertemplate="""<br>Title: %{customdata}
            <br>Author: %{meta}
            <br>Revenue: %{x}
            <extra></extra>""",
            orientation='h',
            marker=dict(
                color=df['collections'],
                colorscale='peach',
                cmin=df['collections'].min(),
                cmax=df['collections'].max(),
                colorbar=dict(
                    thickness=15,
                    title='Collections')))

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                bargap=0.1,
                width=550,
                height=400,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Entries',
                    title_standoff=40,
                    showgrid=False,
                    side='left'),
                xaxis=dict(
                    title='Revenue (ETH)',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': data, 'layout': layout})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return fig


def gen_table(df):
    categories_dict = {
        i+1: {'title': title, 'link': link}
        for i, (title, link)
        in enumerate(zip(
            df.head(10).title.values, df.head(10).link.values))}

    rows = []
    for k, v in categories_dict.items():
        row = html.Tr([
            html.Td(
                str(k) + ": ",
                style={'color': 'rgba(255, 172, 5, 1.00)'}),
            html.Td(html.A(v['title'], href=v['link'], target='_blank'))
        ])
        rows.append(row)

    table_body = [
        html.Tbody(rows, className='table-body')]

    return table_body


# layout for collections and revenue
def gen_layout_col_rev(df):
    """ Generate Layout For the Collections and revenue Charts"""

    df_collected = gen_df_sort_collections(df)
    df_revenue = gen_df_sort_revenue(df)

    layout = html.Div([
                dcc.RangeSlider(
                    id='slider-collections-authors',
                    marks=sorted(df['date'].unique()),
                    step=1,
                    value=[0, len(df['date'].unique())],
                    className='range-slider'
                ),
                html.Div([
                    html.Div([
                        html.H1(
                            'Authors/Publications with the most Collections',
                            className="chart-title"
                            ),
                        dcc.Graph(
                            id="graph-collections-authors",
                            figure=create_collections_authors_figure(
                                df_collected)),
                    ], className="chart-container"),
                    html.Div([
                        html.H1(
                            'Authors/Publications with the most revenue',
                            className="chart-title"),
                        dcc.Graph(
                            id="graph-revenue-authors",
                            figure=create_revenue_authors_figure(
                                df_revenue)
                            )
                    ], className="chart-container"),
                ], className='collections-container'),
                html.Div([
                    html.Div([
                        html.H1(
                            'Most Collected Articles',
                            className="chart-title"
                            ),
                        dcc.Graph(
                            id="graph-collections-entries",
                            figure=create_collections_entries_figure(
                                df_collected)),
                    ], className="chart-container"),
                    html.Table(
                        gen_table(df_collected),
                        id='table-collections',
                    ),
                ], className='collections-container'),
                html.Div([
                    html.Div([
                        html.H1(
                            'Entries with the most Revenue',
                            className="chart-title"),
                        dcc.Graph(
                            id="graph-revenue-entries",
                            figure=create_revenue_entries_figure(
                                df_revenue)
                            )
                    ], className="chart-container"),
                    html.Table(
                        gen_table(df_revenue),
                        id='table-revenue',
                    ),
                ], className='collections-container')
            ], className='fade-in column')

    return layout