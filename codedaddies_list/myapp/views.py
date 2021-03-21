from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = "https://losangeles.craigslist.org/search/?query={}"
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

        soup = BeautifulSoup(data, features='html.parser')



        post_listing = soup.find_all("li", {"class": "result-row"})





        final_posting=[]

        for post in  post_listing:
            post_title=post.find(class_="result-title").text
            post_url=post.find("a").get("href")
            post_image = ''
            if post.find(class_='result-image').get('data-ids'):
                img_list_str = post.find(class_='result-image').get('data-ids')
                img_id = img_list_str.split(',')[0].split(':')[1]
                post_image = 'https://images.craigslist.org/{}_300x300.jpg'.format(img_id)
                
            else:
                post_image="https://www.a777aa77.ru/marussia/2010-marussia-b1-17.jpg"
            if post.find(class_="result-price"):
                post_price=post.find(class_="result-price").text
            
            else:
                post_price="N/A"
        

            final_posting.append((post_title,post_url,post_price,post_image))

        stuff_for_frontend={
            "search":search,
            "final_posting":final_posting,
        }
    return render(request, 'myapp/new_search.html',stuff_for_frontend)
