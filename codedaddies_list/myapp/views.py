from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL="https://losangeles.craigslist.org/search/?query={}"
# Create your views here.


def index(request):
    return render(request, 'base.html')


def newsearch(request):
    if request.POST.get('search'):
        search = request.POST['search']
        # Entry into Database
        models.Search.objects.check(search=search)
        final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
        response = requests.get(final_url)
        data = response.text
        print(data)
        soup = BeautifulSoup(data, features='html.parser')

    stuff_for_frontend={
        "search":search,
    }
    return render(request, 'myapp/new_search.html',stuff_for_frontend)
