from http.client import HTTPResponse
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from scrappy_webpage.models import Searches
import twitter_pull as twitter_pull
import twitter_process as twitter_process

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_health_check(request):
    health_check = {'health':'This application is healthy'}
    return Response(health_check)

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cleaned_data = form.cleaned_data

            #save querry to database
            user_request = Searches(first_query = cleaned_data['first_query'], connector = cleaned_data['connector'], second_query = cleaned_data['second_query'])#, raw_data = '', cleaned_data = '')
            user_request.save()

            #call twitter api for json response
            recent_db_entry = Searches.objects.latest("id") # call most recent entry
            json_as_list = twitter_pull.retrieve_tweets(recent_db_entry.first_query, recent_db_entry.second_query.upper(), recent_db_entry.connector)
            recent_db_entry.raw_data = json_as_list # tag as completing raw data pull
            recent_db_entry.save()

            # clean twitter data
            tweets, interactions = twitter_process.website_tweet_process(recent_db_entry.raw_data)
            recent_db_entry.cleaned_data = tweets
            recent_db_entry.save()

            # redirect to a new URL:
            #return render(request, 'scrappy_webpage/results.html', {'user_request': user_request,'tweets':tweets})
            return render(request, 'scrappy_webpage/results.html', {'user_request': user_request,'tweet1':tweets[0],'tweet2':tweets[1],'tweet3':tweets[2],'tweet4':tweets[3],'tweet5':tweets[4]})
            #return HttpResponseRedirect('/results/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'scrappy_webpage/index.html', {'form': form,})


def integration_test(request):
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':

    db_entry = 'Database Integration Success'

    user_request = Searches(first_query = db_entry, connector = db_entry, second_query = db_entry, raw_data = db_entry, cleaned_data = db_entry)
    user_request.save()

    recent_db_entry = Searches.objects.latest("id") # call most recent entry


    if (recent_db_entry.first_query == db_entry) &\
       (recent_db_entry.connector == db_entry) &\
       (recent_db_entry.second_query == db_entry) &\
       (recent_db_entry.raw_data == db_entry) &\
       (recent_db_entry.cleaned_data == db_entry):
        return render(request, 'scrappy_webpage/integration_test.html', {'int_test_results': recent_db_entry.first_query})

    return render(request, 'scrappy_webpage/integration_test.html', {'int_test_results': 'Integration Test Failed'})


def get_results(request):
    return render(request, "scrappy_webpage/results.html")
