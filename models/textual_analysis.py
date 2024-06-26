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
    languages = {
        'en': 'English',
        'zh': 'Chinese',
        'es': 'Spanish',
        'hi': 'Hindi',
        'ar': 'Arabic',
        'pt': 'Portuguese',
        'bn': 'Bengali',
        'ru': 'Russian',
        'ja': 'Japanese',
        'pa': 'Punjabi',
        'ms': 'Malay',
        'fr': 'French',
        'de': 'German',
        'ur': 'Urdu',
        'te': 'Telugu',
        'vi': 'Vietnamese',
        'ko': 'Korean',
        'it': 'Italian',
        'ta': 'Tamil',
        'tr': 'Turkish',
        'th': 'Thai',
        'gu': 'Gujarati',
        'pl': 'Polish',
        'uk': 'Ukrainian',
        'ro': 'Romanian',
        'nl': 'Dutch',
        'mr': 'Marathi',
        'el': 'Greek',
        'hu': 'Hungarian',
        'cs': 'Czech',
        'sv': 'Swedish',
        'he': 'Hebrew',
        'fi': 'Finnish',
        'da': 'Danish',
        'ml': 'Malayalam',
        'sk': 'Slovak',
        'bg': 'Bulgarian',
        'hr': 'Croatian',
        'lt': 'Lithuanian',
        'sl': 'Slovenian',
        'et': 'Estonian',
        'lv': 'Latvian',
        'sq': 'Albanian',
        'sr': 'Serbian',
        'is': 'Icelandic',
        'ga': 'Irish',
        'mk': 'Macedonian',
        'mt': 'Maltese',
        'eu': 'Basque',
        'bs': 'Bosnian',
        'cy': 'Welsh',
        'lb': 'Luxembourgish',
        'mi': 'Maori',
        'fy': 'Frisian',
        'af': 'Afrikaans',
        'zu': 'Zulu',
        'so': 'Somali',
        'sw': 'Swahili',
        'ha': 'Hausa',
        'yo': 'Yoruba',
        'ig': 'Igbo',
        'am': 'Amharic',
        'az': 'Azerbaijani',
        'ka': 'Georgian',
        'hy': 'Armenian',
        'km': 'Khmer',
        'lo': 'Lao',
        'mn': 'Mongolian',
        'my': 'Burmese',
        'si': 'Sinhala',
        'fil': 'Filipino',
        'ceb': 'Cebuano',
        'haw': 'Hawaiian',
    }

    df['lang'] = df['lang'].map(languages)
    df = pd.DataFrame(df['lang'].value_counts())
    df = df.head(10)

    colors_traces = [
        '#ffac05',
        '#ffb41d',
        '#ffbc36',
        '#ffc450',
        '#ffcd69',
        '#ffd582',
        '#ffdd9b',
        '#ffe6b4',
        '#ffeecd',
        '#fff6e6']

    data = go.Bar(
            x=df['count'],
            y=df.index,
            marker_color=colors_traces,
            orientation='h',
            hovertemplate="""<br>Language: %{y}
            <br>Number of Articles: %{x}
            <extra></extra>""")

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
                bargap=0.1,
                bargroupgap=0.1,
                showlegend=False,  # table being used for legend
                template='plotly_white',
                yaxis=dict(
                    title='Languages',
                    title_standoff=40,
                    showgrid=False,
                    side='left'),
                xaxis=dict(
                    title='Counts',
                    autorange=True,
                    showgrid=False))

    fig = go.Figure({'data': data, 'layout': layout})
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="white")
        )
    return fig


def create_box_chart(df):
    """ Create a boxplot chart with the lengths of characters for body,
    title and descriptions"""

    df['body'] = df['body'].astype(str)
    df['len_body'] = df['body'].apply(lambda x: len(x))
    df['len_title'] = df['title'].apply(lambda x: len(x))
    df['len_description'] = df['description'].apply(lambda x: len(x))
    data_1 = go.Box(
            y=df['len_body'],
            quartilemethod="linear",
            name="Bodies",
            marker_color='#ffac05'
            )

    data_2 = go.Box(
            y=df['len_description'],
            quartilemethod="linear",
            name="Descriptions",
            marker_color='#ffc450'
            )

    data_3 = go.Box(
            y=df['len_title'],
            quartilemethod="linear",
            name="Titles",
            marker_color='#ffdd9b'
            )

    layout = go.Layout(
                margin=dict(l=20, r=20, t=20, b=20),
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
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="white")
        )
    return fig


def create_wordcloud_titles(df):
    """ Creates a wordcloud for the titles """
    word_cloud = WordCloud(
        collocations=False,
        background_color='rgba(255, 255, 255, 0)',
        colormap='Blues',
        mode="RGBA", width=300, height=280).generate(
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
        mode="RGBA", width=300, height=280).generate(
            " ".join(list(df.description.values)))

    return word_cloud.to_image()


def gen_layout_textual(df):
    """Generate Layout For the Textual Analysis"""

    df['description'] = df['description'].apply(clean_text)
    df['lang'] = df['description'].apply(detect_language)

    layout = dcc.Loading([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H1(
                                'Languages of the Week',
                                className="chart-title"
                                ),
                            dcc.Graph(
                                id="graph-networks-languages",
                                figure=create_lang_bar_chart(df),
                                style={
                                    'width': '80vw',
                                    'height': '70vw',
                                    'margin': 'auto'}),
                        ], className="chart-container"),
                    ], className='collections-container'),
                    html.Div([
                        html.Div([
                            html.H1(
                                'Textual Lengths',
                                className="chart-title"
                                ),
                            dcc.Graph(
                                id="graph-networks-lengths",
                                figure=create_box_chart(df),
                                style={
                                    'width': '80vw',
                                    'height': '70vw',
                                    'margin': 'auto'}),
                        ], className="chart-container"),
                    ], className='collections-container'),
                    html.Div([
                        html.Div([
                            html.H1(
                                'Titles Wordcloud',
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
                                'Descriptions Wordcloud',
                                className="chart-title"
                                ),
                            html.Img(
                                id="wordcloud",
                                src=create_wordcloud_description(df)),
                        ], className="chart-container"),
                    ], className='collections-container'),
                ], className='fade-in column')
            ], id="loading-sub-layout", type="circle"),

    return layout
