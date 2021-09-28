import csv


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
