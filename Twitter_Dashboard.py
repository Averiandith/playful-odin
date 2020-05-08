import csv
import datetime
import pandas as pd
import numpy as np
from Csv_Files import *

import plotly.figure_factory as ff
import plotly.graph_objs as go
import chart_studio.plotly as py
from chart_studio.plotly import iplot

###################################################################
## Future tasks
# Smoothing (time curve)
# API calling in the future

# Initializing Variables
user_1 = "Boris Johnson"
user_1_tweet_replies_file = "BorisJohnson's_tweet_replies.csv"
user_1_hashtags_file = "BorisJohnson's_hashtags_past_30_days.csv"
user_1_mentions_file = "BorisJohnson's_mentions_past_30_days.csv"
user_1_frequency_words_file = "BorisJohnson's_tweets_replies_highest_frequency_words.csv"
user_1_stats_file = "BorisJohnson's_stats.csv"

user_2 = "Donald Trump"
user_2_tweet_replies_file = "realDonaldTrump's_tweet_replies.csv"
user_2_hashtags_file = "realDonaldTrump's_hashtags_past_30_days.csv"
user_2_mentions_file = "realDonaldTrump's_mentions_past_30_days.csv"
user_2_frequency_words_file = "realDonaldTrump's_tweets_replies_highest_frequency_words.csv"
user_2_stats_file = "realDonaldTrump's_stats.csv"

# Initializing Colors
colors = ['hsl('+str(h)+',70%'+',70%)' for h in np.linspace(0, 360, 15)]
pie_colors_amber = ['rgb(255, 111, 0)', 'rgb(255, 143, 0)', 'rgb(255, 193, 7)', 'rgb(255, 224, 130)', 'rgb(255, 248, 225)']
pie_colors_blue = ['rgb(1, 87, 155)', 'rgb(3, 155, 229)', 'rgb(3, 169, 244)', 'rgb(79, 195, 247)', 'rgb(179, 229, 252)']
pie_colors_purple = ['rgb(49, 27, 146)', 'rgb(81, 45, 168)', 'rgb(103, 58, 183)', 'rgb(149, 117, 205)', 'rgb(209, 196, 233)']

####################################################################
# Preprocessing Data

def unique(a_list):
    """
    Troll Function to only select unique elements (noob and lazy sia).
    """
    result = []
    for item in a_list:
        if item not in result:
            result.append(item)
    return result


def data_preprocessing(tweet_replies_file, hashtags_file, mentions_file, frequency_words_file, stats_file):
    """
    Function to preprocess all data for the plots/tables.
    """

    with open(tweet_replies_file, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    parent_tweet_id = []
    # populate parent_tweet_id array
    for i in range(1, len(data)):
        item = data[i]
        if item[1] == 'None':
            # change 'None' to 0 for simple comparison later 
            parent_tweet_id.append(0)
        else:
            # accept if it's a number
            parent_tweet_id.append(int(item[1]))

    # select the unique ids
    parent_tweet_id = unique(parent_tweet_id) 

    # get noun of the tweet
    noun = []
    for parent_tweet in parent_tweet_id:
        for item in data:
            if item[1] == str(parent_tweet):
                noun.append(item[7])

    noun = unique(noun)
    noun.insert(0, 'Parent_Tweets')

    tweet_score = []
    details = []

    for parent_id in parent_tweet_id:
        temp = []
        temp2 = []

        for i in range(1, len(data)):
            item = data[i]

            # None comment means it belongs to main user
            if item[1] == 'None':
                if parent_id == 0:
                    temp.append(str(item[5]))
                    temp2.append({'account_name': item[3], 'tweet': item[4], 'tweet_score': item[5], 'sentiment': item[6], 'influence': item[8]})
            
            elif int(item[1]) == parent_id:
                temp.append(str(item[5]))
                temp2.append({'account_name': item[3], 'tweet': item[4], 'tweet_score': item[5], 'sentiment': item[6], 'influence': item[8]})

        tweet_score.append(temp)
        details.append(temp2)

    # Preprocessing Data influence average 
    influence_collection = []
    for item in details:    
        for _ in item:
            influence_individual = [float(z['influence']) for z in item]
        influence_collection.append(influence_individual)

    noun_label = [noun[y] for y in range(1, len(noun))]
    influence_temp = [influence_collection[x] for x in range(1, len(influence_collection))]

    influence_label = []
    for item in influence_temp:
        total = 0
        for x in item:
            total += x
        average = total/len(item)
        influence_label.append(average)

    with open(hashtags_file) as csvfile:
        hashtags_data = list(csv.reader(csvfile))

    with open(mentions_file) as csvfile:
        mentions_data = list(csv.reader(csvfile))

    with open(frequency_words_file) as csvfile:
        freq_words_data = list(csv.reader(csvfile))

    with open(stats_file) as csvfile:
        stats_data = list(csv.reader(csvfile))

    return {
            'data': data,
            'parent_tweet_id': parent_tweet_id,
            'noun': noun,
            'tweet_score': tweet_score, 
            'details': details, 
            'noun_label': noun_label, 
            'influence_label': influence_label,
            'hashtags_data': hashtags_data,
            'mentions_data': mentions_data,
            'freq_words_data': freq_words_data,
            'stats_data': stats_data
    }

###################################################################
# Box and Whisker Plot (Tweet Replies Sentiment)

def box_whisker_sentiment(noun, tweet_score, details):
    """
    Box and whisker plot to showcase sentiment score for each tweet replies to parent tweet.
    """

    box_whisker = go.Figure()
    for xd, yd, cls, item in zip(noun, tweet_score, colors, details):
        box_whisker.add_trace(go.Box(
            y = yd,
            name = xd,
            boxpoints = 'all',
            text = [f"account: {z['account_name']}<br>" + f"tweet: {z['tweet']}<br>" + f"tweet_score: {z['tweet_score']}<br>" + f"sentiment: {z['sentiment']}<br>" + f"influence_score: {z['influence']}<br>" for z in item],
            hoverinfo = 'text',
            jitter = 0.2,
            whiskerwidth = 0.1,
            fillcolor = cls,
            marker_size = 3,
            line_width=2)
        )

    box_whisker.layout.update(
        title = "Tweet's Replies Sentiment Score",
        yaxis = dict(
            autorange = True,
            showgrid = True,
            zeroline = True,
            dtick = 0.1,
            gridcolor = 'rgb(255, 255, 255)',
            gridwidth = 1,
            zerolinecolor = 'rgb(255, 255, 255)',
            zerolinewidth = 1
        ),
        margin = dict(
            l = 20,
            r = 20,
            b = 70,
            t = 100,
        ),
        paper_bgcolor = 'rgb(243, 243, 243)',
        plot_bgcolor = 'rgb(243, 243, 243)',
        showlegend = True,
        legend_title = 'Noun'
    )

    return box_whisker

###################################################################   
# Pie Chart 
     
def piechart_hashtags(hashtags_data, user_name):
    """
    Pie Chart for top 5 hashtags.
    """
    hashtags = []
    hashtags_count = []
    for i in range(1, len(hashtags_data)):
        hashtags.append(hashtags_data[i][0])
        hashtags_count.append(int(hashtags_data[i][1]))

    pie_chart_hashtags = go.Figure(data = [go.Pie(
        labels = hashtags,
        values = hashtags_count,
        textinfo = 'percent',
        insidetextorientation= 'radial',
        pull = [0.15, 0, 0, 0, 0],
        # title = user_name,
        marker_colors = pie_colors_amber
    )])

    pie_chart_hashtags.update_layout(title = user_name)
    return pie_chart_hashtags
 

def piechart_mentions(mentions_data, user_name):
    """
    Pie Chart for top 5 mentions.
    """
    mentions = []
    mentions_count = []
    for i in range(1, len(mentions_data)):
        mentions.append(mentions_data[i][0])
        mentions_count.append(int(mentions_data[i][1]))

    pie_chart_mentions = go.Figure(data = [go.Pie(
        labels = mentions,
        values = mentions_count,
        textinfo = 'percent',
        insidetextorientation= 'radial',
        pull = [0.15, 0, 0, 0, 0],
        title = user_name,
        marker_colors = pie_colors_purple
    )])

    pie_chart_mentions.update_layout(title = user_name)
    return pie_chart_mentions

################################################################### 
# Bar Chart 

def barchart_top_words(freq_words_data, user_name):
    """
    Bar Chart to illustrate the top 10 words that appeared in all replies
    """
    word_label = [item[0] for item in freq_words_data]
    count_label = [item[1] for item in freq_words_data]

    freq_words_barchart = go.Figure(data=[go.Bar(
        x = count_label,
        y = word_label,
        marker_color = colors,
        orientation = 'h'
    )])
    freq_words_barchart.update_layout(title_text = user_name)
    # Top 10 words that Boris Johnson's followers use in replying
    return freq_words_barchart


def barchart_influence(noun_label, influence_label):
    """
    Bar Chart to illustrate the average influence score for each noun and adjective (tweet).
    """
    influence_barchart = go.Figure(
        data=[go.Bar(
            x = noun_label,
            y = influence_label,
            marker_color = colors
    )])
    influence_barchart.update_layout(title_text = "Replies Average Influence Score")
    return influence_barchart

###################################################################
# Table

def table_stats(stats_data_user_1, stats_data_user_2, user_name_1, user_name_2):
    """
    Table to showcase the profile information between two users.
    """

    stats_key = ['Profile Description', 'Tweet Count', 'Likes Count', 'Following Count', 'Followers Count', 'Account Age (Days)', 'Average Tweets Per Day']
    user_1_stats = [stats_data_user_1[i][1] for i in range(3, 10)]
    user_2_stats = [stats_data_user_2[j][1] for j in range(3, 10)]    

    cell_values = []
    cell_values.append([item for item in stats_key])
    cell_values.append([item for item in user_1_stats])
    cell_values.append([item for item in user_2_stats])

    table_fig = go.Figure(data=[go.Table(
        header = dict(values=['', user_name_1, user_name_2],
                      align = 'left'   
                ),
        cells = dict(values= cell_values,
                    align = 'left'
                )
    )])
    
    return table_fig

###################################################################
# Dash 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

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
    app.run_server(debug=True, use_reloader=False)  



    
    
    