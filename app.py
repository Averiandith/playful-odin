import pandas as pd

from preprocessing import data_preprocessing

from plots.box_whisker import box_whisker_sentiment
from plots.piechart import piechart_hashtags, piechart_mentions
from plots.barchart import barchart_top_words, barchart_influence
from plots.table import table_stats

"""
TODO:
1. Smoothing (time curve)
2. API calling
"""

# Initializing Variables
user_1 = "Boris Johnson"
user_1_tweet_replies_file = "data/BorisJohnson's_tweet_replies.csv"
user_1_hashtags_file = "data/BorisJohnson's_hashtags_past_30_days.csv"
user_1_mentions_file = "data/BorisJohnson's_mentions_past_30_days.csv"
user_1_frequency_words_file = "data/BorisJohnson's_tweets_replies_highest_frequency_words.csv"
user_1_stats_file = "data/BorisJohnson's_stats.csv"

user_2 = "Donald Trump"
user_2_tweet_replies_file = "data/realDonaldTrump's_tweet_replies.csv"
user_2_hashtags_file = "data/realDonaldTrump's_hashtags_past_30_days.csv"
user_2_mentions_file = "data/realDonaldTrump's_mentions_past_30_days.csv"
user_2_frequency_words_file = "data/realDonaldTrump's_tweets_replies_highest_frequency_words.csv"
user_2_stats_file = "data/realDonaldTrump's_stats.csv"

# Dash 
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.title='Twitter Dashboard'

app.layout = html.Div(children = [

    html.H2(style = {'textAlign': 'center', 'fontFamily': "Sans-Serif"},
    children = "Twitter Dashboard"),

    html.Div([
        dcc.Tabs(
            id = 'tab-input',
            value = '1',
            children = [
                dcc.Tab(label = F"{user_1} vs {user_2}", value = '1'),
                dcc.Tab(label = F"{user_1} Sentiment & Influence", value = '2'),
                dcc.Tab(label = F"{user_2} Sentiment & Influence", value = '3')
            ]
        ),

        html.Div(id = 'tab-output')
    ], style = {
        'width': '100%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    })

])

###################################################################
# Tab Control's Callback

user_1_data = data_preprocessing(user_1_tweet_replies_file, user_1_hashtags_file, user_1_mentions_file, user_1_frequency_words_file, user_1_stats_file)
user_2_data = data_preprocessing(user_2_tweet_replies_file, user_2_hashtags_file, user_2_mentions_file, user_2_frequency_words_file, user_2_stats_file)

@app.callback(Output('tab-output', 'children'), [Input('tab-input', 'value')])
def display_content(value):
    """
    Callback function to receive tab value and display output on the page.
    """

    if value == '1':
        return (
            html.Br(),

            html.H5(style = {'textAlign': 'center', 'fontFamily': "Sans-Serif"},
            children = "Profiles Particulars At A Glance"),

            html.Div([dcc.Graph(id = 'table_users', figure = table_stats(user_1_data['stats_data'], user_2_data['stats_data'], user_1, user_2))]),

            html.H5(style = {'textAlign': 'center', 'fontFamily': "Sans-Serif"},
            children = "Top 10 Words That Follower's Used To Reply"),

            html.Div([
                html.Div([dcc.Graph(id = 'bar_chart_freq_words_user_1', figure = barchart_top_words(user_1_data['freq_words_data'], user_1))]),
                html.Div([dcc.Graph(id = 'bar_chart_freq_words_user_2', figure = barchart_top_words(user_2_data['freq_words_data'], user_2))])
            ], style = {'columnCount': 2}),
            
            html.H5(style = {'textAlign': 'center', 'fontFamily': "Sans-Serif"},
            children = "Top 5 Hashtags (past 30 days)"),

            html.Div([
                html.Div([dcc.Graph(id = 'pie_chart_hashtags_user_1', figure = piechart_hashtags(user_1_data['hashtags_data'], user_1))]),
                html.Div([dcc.Graph(id = 'pie_chart_hashtags_user_2', figure = piechart_hashtags(user_2_data['hashtags_data'], user_2))])
            ], style = {'columnCount': 2}),

            html.H5(style = {'textAlign': 'center', 'fontFamily': "Sans-Serif"},
            children = "Top 5 Mentions (past 30 days)"),

            html.Div([
                html.Div([dcc.Graph(id = 'pie_chart_mentions_user_1', figure = piechart_mentions(user_1_data['mentions_data'], user_1))]),
                html.Div([dcc.Graph(id = 'pie_chart_mentions_user_2', figure = piechart_mentions(user_2_data['mentions_data'], user_2))])
            ], style = {'columnCount': 2})
        )

    elif value == '2':
        return (
            html.Div([dcc.Graph(id = 'box_whisker_replies_sentiment_user_1', figure = box_whisker_sentiment(user_1_data['noun'], user_1_data['tweet_score'], user_1_data['details']))]),

            html.Div([dcc.Graph(id = 'bar_chart_avg_influence', figure = barchart_influence(user_1_data['noun_label'], user_1_data['influence_label']))]),

            html.Div([
                html.Div([dcc.Graph(id = 'scatter_plot_time_influence_user_1')]),
                html.Div([dcc.Slider(
                    id = 'scatter_plot_time_influence_slider_user_1',
                    min = 1,
                    max = len(user_1_data['parent_tweet_id'])-1,
                    value = 1,
                    marks = {str(tweet): str(tweet) for tweet in range(len(user_1_data['parent_tweet_id'])-1)},
                    step = None,
                    )
                ])
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div(style = {'textAlign': 'left', 'fontFamily': "Sans-Serif"},
            children = "Influence Score is calculated using this formula: ((likes_given + tweet_count) / account_age) * followers_to_following_ratio"),
            html.Div(style = {'textAlign': 'left', 'fontFamily': "Sans-Serif"},
            children = "If the account is very active and have a healthy followers to following ratio, it will have a high Influence Score.")
        )

    elif value == '3':
         return (
            html.Div([dcc.Graph(id = 'box_whisker_replies_sentiment_user_2', figure = box_whisker_sentiment(user_2_data['noun'], user_2_data['tweet_score'], user_2_data['details']))]),

            html.Div([dcc.Graph(id = 'bar_chart_avg_influence', figure = barchart_influence(user_2_data['noun_label'], user_2_data['influence_label']))]),

            html.Div([
                html.Div([dcc.Graph(id = 'scatter_plot_time_influence_user_2')]),
                html.Div([dcc.Slider(
                    id = 'scatter_plot_time_influence_slider_user_2',
                    min = 1,
                    max = len(user_2_data['parent_tweet_id'])-1,
                    value = 1,
                    marks = {str(tweet): str(tweet) for tweet in range(len(user_2_data['parent_tweet_id'])-1)},
                    step = None,
                    )
                ])
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div(style = {'textAlign': 'left', 'fontFamily': "Sans-Serif"},
            children = "Influence Score is calculated using this formula: ((likes_given + tweet_count) / account_age) * followers_to_following_ratio"),
            html.Div(style = {'textAlign': 'left', 'fontFamily': "Sans-Serif"},
            children = "If the account is very active and have a healthy followers to following ratio, it will have a high Influence Score.")
        )

###################################################################
# Scatter Plot's Callback (Influence & Time)

@app.callback(Output('scatter_plot_time_influence_user_1', 'figure'), [Input('scatter_plot_time_influence_slider_user_1', 'value')])

def update_figure(selected_idx):
    """
    Callback function to update influence plot based on given tweet index.
    """

    # Callback to select which index to reference
    selected_parent_id = user_1_data['parent_tweet_id'][selected_idx]

    # Get all the id that matches with the parent_id (selected_parent_id)
    filtered_data = []
    for item in user_1_data['data']:
        if item[1] == str(selected_parent_id):
            filtered_data.append(item)

    # Gather all time stamps
    time_stamp = [item[2] for item in filtered_data]

    # Gather all influence score
    influence_score = [item[8] for item in filtered_data]

    # Smoothing (Moving Average)
    df = pd.DataFrame(influence_score)
    df['MA1'] = df.rolling(window = 2).mean()    

    traces = []
    traces.append(dict(
        x = time_stamp,
        y = influence_score,
        mode = 'markers',
        line = dict(color = 'rgb(255, 128, 171)'),
        name = 'Actual Traces'
    ))

    traces.append(dict(
        x = time_stamp,
        y = df['MA1'],
        mode = 'lines',
        line = dict(color = 'rgb(0, 200, 83)'),
        name = "Moving Average"
    ))

    return {
        'data': traces,
        'layout': dict(
            title = {
                'text': "Replies Influence Score Over Time"
            },      
            xaxis = {'title': 'Time'},
            yaxis = {'title': 'Influence Score'}
        )
    }


@app.callback(Output('scatter_plot_time_influence_user_2', 'figure'), [Input('scatter_plot_time_influence_slider_user_2', 'value')])
def update_figure_2(selected_idx):
    """
    Callback function to update influence plot based on given tweet index. (tab2)
    """
    # Callback to select which index to reference
    selected_parent_id = user_2_data['parent_tweet_id'][selected_idx]

    # Get all the id that matches with the parent_id (selected_parent_id)
    filtered_data = []
    for item in user_2_data['data']:
        if item[1] == str(selected_parent_id):
            filtered_data.append(item)

    # Gather all time stamps
    time_stamp = [item[2] for item in filtered_data]

    # Gather all influence score
    influence_score = [item[8] for item in filtered_data]

    # Smoothing (Moving Average)
    df = pd.DataFrame(influence_score)
    df['MA1'] = df.rolling(2).mean()    

    traces = []
    traces.append(dict(
        x = time_stamp,
        y = influence_score,
        mode = 'markers',
        line = dict(color = 'rgb(255, 128, 171)'),
        name = 'Actual Traces'
    ))

    traces.append(dict(
        x = time_stamp,
        y = df['MA1'],
        mode = 'lines',
        line = dict(color = 'rgb(0, 200, 83)'),
        name = "Moving Average"
    ))

    return {
        'data': traces,
        'layout': dict(
            title = {
                'text': "Replies Influence Score Over Time"
            },
            xaxis = {'title': 'Time'},
            yaxis = {'title': 'Influence Score'}
        )
    }

###################################################################
if __name__ == "__main__":
    app.run_server()  



    
    
    
