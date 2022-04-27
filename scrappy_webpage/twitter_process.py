# For sending GET requests from the API
import requests
# For dealing with json responses we receive from the API
import json
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import unicodedata
#To add wait time between requests
import time

def tweet_looper(tweets):
    all_tweets = []
    # loop through tweets and extract necessary information
    try:
        for tweet in tweets['data']:
            # 1. Author ID
            author_id = tweet['author_id']
            # 2. Time created
            created_at = tweet['created_at']
            # 3. Language
            lang = tweet['lang']
            # 4. Tweet metrics
            retweet_count = tweet['public_metrics']['retweet_count']
            reply_count = tweet['public_metrics']['reply_count']
            like_count = tweet['public_metrics']['like_count']
            quote_count = tweet['public_metrics']['quote_count']
            tot_count = retweet_count + reply_count + like_count + quote_count
            # 5. source
            source = tweet['source']
            # 6. Tweet text
            text = tweet['text']

            tweet_data = [author_id, created_at, lang, tot_count, text]
            all_tweets.append(tweet_data)

        return all_tweets
    except:
        # if no tweets exist for keywords, return message
        return [[1, 1, 1, 1, "Sorry, no tweets exist with your search terms! Please try again."]]

def get_min_index(lst):
    minimum = min(lst)
    min_idx = lst.index(minimum)
    return min_idx

def top_five_tweets(all_tweets):
    max_interactions = [0, 0, 0, 0, 0]
    displayed_tweets = ["", "", "", "", ""]
    for data in all_tweets:
        interactions = data[3]
        if interactions > min(max_interactions):
            idx = get_min_index(max_interactions)
            max_interactions[idx] = interactions
            displayed_tweets[idx] = data[4]
    return(displayed_tweets,max_interactions)

def website_tweet_process(json_response):
    all_tweets = json_response #tweet_looper(json_response)
    tweet,interactions = top_five_tweets(all_tweets)
    return tweet,interactions
