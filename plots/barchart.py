import plotly.graph_objs as go
from plots.colors import colors


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