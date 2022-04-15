from http.client import HTTPResponse
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from scrappy_webpage.models import Searches
# import scrappy_webpage.twitter_pull as twitter_pull

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cleaned_data = form.cleaned_data
            input
            #call twitter api
            # tweets, interactions = twitter_pull.website_tweet_pull(cleaned_data['first_query'], cleaned_data['second_query'].upper(), cleaned_data['connector'])
            tweets = [3,4]
            #save querry to database
            user_request = Searches(first_query = cleaned_data['first_query'], connector = cleaned_data['connector'], second_query = cleaned_data['second_query'])
            # user_request.save()



            # redirect to a new URL:
            return render(request, 'scrappy_webpage/results.html', {'user_request': user_request,'tweets':tweets})
            #return HttpResponseRedirect('/results/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'scrappy_webpage/index.html', {'form': form,})


def get_results(request):
    return render(request, "scrappy_webpage/results.html")     



# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
# import os
# For dealing with json responses we receive from the API
import json
# For saving the response data in CSV format
# import csv
# For parsing the dates received from twitter in readable formats
# import datetime
# import unicodedata
#To add wait time between requests
# import time
# Test out Tweepy functionality
# import tweepy

token = 'AAAAAAAAAAAAAAAAAAAAAEg4aQEAAAAASy8asmZtrAf3y3aHNLQU2nK3bgY%3D1qoAMuRn0NSsV51MrBJMbSQTIbQiKQQUo6mA1KIXoOpPXI5VsR'

def auth():
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
    if connector != "X":
        if connector == "AND":
            build_query = input1 + " " + input2 + lang_key + rt
        elif connector == "OR":
            build_query = "(" + input1 + " " + connector + " " + input2  + ")" + lang_key + rt
        else:
            raise ValueError
    else:
        build_query = input1 + lang_key + rt
    return build_query

def retrieve_json(input1,input2=None,connector=None,next_token = None):
    #Inputs for the request
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = write_query(input1,input2,connector)
    max_results = 100
    url = create_url(keyword, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
    return json_response

def tweet_looper(tweets):
    all_tweets = []
    # loop through tweets and extract necessary information
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

def website_tweet_pull(input1,input2=None,connector=None):
    json_response = retrieve_json(input1,input2,connector)
    all_tweets = tweet_looper(json_response)
    tweet,interactions = top_five_tweets(all_tweets)
    return tweet,interactions
