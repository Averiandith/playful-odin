import plotly.graph_objs as go
from plots.colors import colors


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