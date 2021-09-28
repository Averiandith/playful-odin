import plotly.graph_objs as go
from plots.colors import pie_colors_amber, pie_colors_purple


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
