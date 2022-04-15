from http.client import HTTPResponse
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from scrappy_webpage.models import Searches
import twitter_pull

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cleaned_data = form.cleaned_data
            #call twitter api
            tweets, interactions = twitter_pull.website_tweet_pull(cleaned_data['first_query'], cleaned_data['second_query'].upper(), cleaned_data['connector'])
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
