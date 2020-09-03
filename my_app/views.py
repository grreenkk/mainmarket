from django.shortcuts import render
from .models import Search
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests

# Link of scrapped site
BASE_URL = 'https://www.jumia.com.ng/catalog/?q={}'

# Create your views here.


def index(request):
    return render(request, 'base.html')


def new_search(request):
    # This gets the objects inputed into the search bar
    search = request.POST.get('content')
    # This creates a database for all searches
    Search.objects.create(search=search)
    # This is the url that will be passed to response
    final_url = BASE_URL.format(quote_plus(search))
    # This gets the information embedded in the url
    response = requests.get(final_url)
    # contains site content in text form
    data = response.text
    # Used to scrape the website by passing, by taking two attributes which contains text gotten by response
    soup = BeautifulSoup(data, 'html.parser')
    # This is the element that contains all the need information to be scraped
    post_listings = soup.find_all("article", class_="prd _fb col c-prd")

    # Array that contains scrapped information to be rendered in html
    final_postings = []

    # For loop to get used to get info added to final_postings
    for post in post_listings:
        post_title = post.find(class_="name").text
        post_link = post.find(class_="core").get('href')
        # If statement in case price value is not available
        if post.find(class_="prc"):
            post_price = post.find(class_="prc")
        else:
            post_price = 'N/A'
        post_image = post.find(class_="img").get('data-src')
        post_url = '{}'.format('https://www.jumia.com.ng')+post_link

        final_postings.append((post_title, post_url, post_price, post_image))

    # Includes all rendered data
    stuffs_for_frontend = {
        'search': search,
        'final_postings' : final_postings,
    }

    return render(request, 'index.html', stuffs_for_frontend)