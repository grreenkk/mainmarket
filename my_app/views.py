from django.shortcuts import render
from .models import Search
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests


BASE_URL = 'https://www.jumia.com.ng/catalog/?q={}'

# Create your views here.
def index(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('content')
    Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    post_listings = soup.find_all("article", class_="prd _fb col c-prd")

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_="name").text
        post_link = post.find(class_="core").get('href')
        post_price = post.find(class_="prc").text
        post_image = post.find(class_="img").get('data-src')
        post_url = '{}'.format('https://www.jumia.com.ng')+post_link

        final_postings.append((post_title, post_url, post_price, post_image))


    stuffs_for_frontend = {
        'search': search,
        'final_postings' : final_postings,
    }
    print(response)


    print(search)
    print(response)

    return render(request, 'index.html', stuffs_for_frontend)