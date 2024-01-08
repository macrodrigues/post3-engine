""" This script has several functions to launch charts and wordlouds for
the textual analysis """
# pylint: disable=W0108
import langid
from neattext.pipeline import TextPipeline
from neattext.functions import remove_html_tags, remove_urls, remove_puncts
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from wordcloud import WordCloud


def clean_text(x):
    """This function uses neattext functions to clean descriptions, bodys and
    titles"""
    clean_pipe = TextPipeline(
        steps=[
            remove_puncts,
            remove_html_tags,
            remove_urls])

    return clean_pipe.fit(str(x))


def detect_language(x):
    """ Function to detect the language"""
    if x is None:
        return None
    else:
        res = langid.classify(x)
        return res[0]


def create_lang_bar_chart(df):
    """creates a bar chart showing the languages used in
    the articles' dataset"""
    df = pd.DataFrame(df['lang'].value_counts())
    df = df.head(10)

    colors_traces = [
        '#0073f1',
        '#0e81ff',
        '#2a90ff',
        '#479fff',
        '#63aeff',
        '#80bcff',
        '#9ccbff',
        '#b8daff',
        '#d4e9ff',
        '#f1f8ff']

    data = go.Bar(
            x=df.index,
            y=df['count'],
            marker_color=colors_traces,
            hovertemplate="""<br>Language: %{x}
            <br>Counts: %{y}
            <extra></extra>""")

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                bargap=0.1,
                width=500,
                height=400,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Counts',
                    title_standoff=40,
                    showgrid=False,
                    side='left'),
                xaxis=dict(
                    title='Language',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': data, 'layout': layout})
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'})
    return fig


def create_box_chart(df):
    """ Create a boxplot chart with the lengths of characters for body,
    title and descriptions"""
    df['len_body'] = df['body'].apply(lambda x: len(x))
    df['len_title'] = df['title'].apply(lambda x: len(x))
    df['len_description'] = df['description'].apply(lambda x: len(x))
    data_1 = go.Box(
            y=df['len_body'],
            quartilemethod="linear",
            name="Bodies",
            marker_color='#007aff'
            )

    data_2 = go.Box(
            y=df['len_description'],
            quartilemethod="linear",
            name="Descriptions",
            marker_color='#49a0ff'
            )

    data_3 = go.Box(
            y=df['len_title'],
            quartilemethod="linear",
            name="Titles",
            marker_color='#92c6ff'
            )

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                width=500,
                height=400,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Text Length',
                    title_standoff=40,
                    showgrid=False,
                    type='log',
                    side='left'),
                xaxis=dict(
                    title='Text Types',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': [data_1, data_2, data_3], 'layout': layout})
    return fig


def create_wordcloud_titles(df):
    """ Creates a wordcloud for the titles """
    word_cloud = WordCloud(
        collocations=False,
        background_color='rgba(255, 255, 255, 0)',
        colormap='Blues',
        mode="RGBA", width=500, height=300).generate(
            " ".join(list(df.title.values)))

    return word_cloud.to_image()


def create_wordcloud_description(df):
    """ Creates a wordcloud for the descriptions """
    # Replace 'nan' strings with actual NaN values
    df['description'].replace('nan', pd.NA, inplace=True)

    # Drop rows with NaN values in the 'description' column
    df.dropna(subset=['description'], inplace=True)
    word_cloud = WordCloud(
        collocations=False,
        background_color='rgba(255, 255, 255, 0)',
        colormap='Blues',
        mode="RGBA", width=500, height=300).generate(
            " ".join(list(df.description.values)))

    return word_cloud.to_image()


def gen_layout_textual(df):
    """Generate Layout For the Textual Analysis"""

    df['description'] = df['description'].apply(clean_text)
    df['lang'] = df['description'].apply(detect_language)

    layout = html.Div([
                dcc.Loading([
                    html.Div([
                        html.Div([
                            html.H1(
                                'Languages Present in the Articles',
                                className="chart-title"
                                ),
                            dcc.Graph(
                                id="graph-networks",
                                figure=create_lang_bar_chart(df)),
                        ], className="chart-container"),
                    ], className='collections-container'),
                    html.Div([
                        html.Div([
                            html.H1(
                                'Textual Lengths of the Articles',
                                className="chart-title"
                                ),
                            dcc.Graph(
                                id="graph-networks",
                                figure=create_box_chart(df)),
                        ], className="chart-container"),
                    ], className='collections-container'),
                    html.Div([
                        html.Div([
                            html.H1(
                                'Most Common Words in Titles',
                                className="chart-title"
                                ),
                            html.Img(
                                id="wordcloud",
                                src=create_wordcloud_titles(df)),
                        ], className="chart-container"),
                    ], className='collections-container'),
                    html.Div([
                        html.Div([
                            html.H1(
                                'Most Common Words in Descriptions',
                                className="chart-title"
                                ),
                            html.Img(
                                id="wordcloud",
                                src=create_wordcloud_description(df)),
                        ], className="chart-container"),
                    ], className='collections-container'),
                ], id="loading-sub-layout", type="default"),
            ], className='fade-in column')

    return layout
