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

def website_tweet_process(all_tweets):
    tweet,interactions = top_five_tweets(all_tweets)
    return tweet,interactions
