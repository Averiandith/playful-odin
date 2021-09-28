import plotly.graph_objs as go


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