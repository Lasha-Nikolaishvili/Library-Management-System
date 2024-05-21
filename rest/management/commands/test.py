from django.core.management import BaseCommand
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import time
import pprint
import re


def get_book(url):
    product_page = requests.get(url).text
    product_page_soup = BeautifulSoup(product_page, 'html.parser')
    div = product_page_soup.find('div', class_='book-detail')

    title = div.find('h1', class_='book-title').get_text(strip=True)
    authors = [a.get_text(strip=True) for a in div.select('.author a')]
    image = div.find('li', class_='img-item').get('data-src')
    genres = [
        genre for genre in
        re.sub(r'\s+', '', div.select_one('.book-format li:nth-of-type(3) span').get_text())
        .split(',')
        if genre != ''
    ]
    date_published = div.select_one('.book-format li:nth-of-type(2) span').get_text(strip=True)

    return {
        'title': title,
        'authors': authors,
        'image': image,
        'genres': genres,
        'date_published': date_published,
    }


class Command(BaseCommand):
    help = 'This command collects and adds the library data to the database'

    def handle(self, *args, **options):
        url = 'https://bookshop.ge/product/view/-9781338815283'
        pprint.pp(get_book(url))
