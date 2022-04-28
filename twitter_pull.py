# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import unicodedata
#To add wait time between requests
import time
# For accessing API Key in Heroku environmental variables
from boto.s3.connection import S3Connection

def auth():
    token = 'AAAAAAAAAAAAAAAAAAAAAEg4aQEAAAAASy8asmZtrAf3y3aHNLQU2nK3bgY%3D1qoAMuRn0NSsV51MrBJMbSQTIbQiKQQUo6mA1KIXoOpPXI5VsR'
    return token

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results = 50):
    search_url = "https://api.twitter.com/2/tweets/search/recent" # could change to /all for academic account
    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    #'start_time': start_date, # use default parameter - 7 days ago
                    #'end_time': end_date,     # use default parameter - ~30 seconds ago
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def write_query(input1, input2 = None, connector = None):
    lang_key = " lang:en"               # only english results
    rt = " -is:retweet"                 # do not include retweets
    #if connector != "X":
    if connector != "":
        if connector == "AND":
            build_query = input1 + " " + input2 + lang_key + rt
        elif connector == "OR":
            build_query = "(" + input1 + " " + connector + " " + input2  + ")" + lang_key + rt
        else:
            # if user inputs first word and connector but no second word, default to first word
            build_query = input1 + lang_key + rt
    else:
        build_query = input1 + lang_key + rt
    return build_query

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

def retrieve_tweets(input1,input2=None,connector=None,next_token = None):
    # Handle cases of improper inputs:
    if (connector == "" and input2 != "") or (connector != "" and input2 == ""):
        return [[1, 1, 1, 1, "Please enter a valid search with either one search term, or two search terms with a connector."]]
    #Inputs for the request
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = write_query(input1,input2,connector)
    max_results = 100
    url = create_url(keyword, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
    tweets = tweet_looper(json_response)
    return tweets
