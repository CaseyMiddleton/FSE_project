from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    #template = loader.get_template('scrappy_webpage/index.html')
    #return HttpResponse(template.render(request))
    return render(request, 'scrappy_webpage/index.html') 
