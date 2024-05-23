from django.core.management import BaseCommand
from library.models import Author, Book, Genre

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from datetime import datetime
from random import randint
import requests
import time
import re


def get_book(url, session, book_listing):
    product_page = session.get(url).text
    product_page_soup = BeautifulSoup(product_page, 'html.parser')
    div = product_page_soup.find('div', class_='book-detail')

    title = div.find('h1', class_='book-title').get_text(strip=True)
    authors = [a.get_text(strip=True) for a in div.select('.author a')]
    image = div.find('li', class_='img-item').get('data-src')
    genres = [
        genre.strip() for genre in
        re.sub(r'\s+', ' ', div.select_one('.book-format li:nth-of-type(3) span').get_text())
        .split(',')
        if genre.strip() != ''
    ]
    date_published = div.select_one('.book-format li:nth-of-type(2) span').get_text(strip=True)

    book_listing.append({
        'title': title,
        'authors': authors,
        'image': image,
        'genres': genres,
        'date_published': date_published,
    })


def get_book_listing_urls(url, num_page, session, product_urls):
    url = f'{url}?page={num_page}'
    listing_page = session.get(url).text
    listing_page_soup = BeautifulSoup(listing_page, 'html.parser')
    for a in listing_page_soup.select('.product-card .product-header a'):
        link = a.get('href')
        if link is not None:
            product_urls.append(link)


def get_book_listing(url, session, num_pages):
    product_urls = []

    with ThreadPoolExecutor(max_workers=num_pages) as executor:
        executor.map(lambda num_page: get_book_listing_urls(url, num_page, session, product_urls), range(num_pages))

    book_listing = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda product_url: get_book(product_url, session, book_listing), product_urls)

    return book_listing


def get_data(urls, num_pages=44):
    with requests.Session() as session:
        data = []
        for i in range(len(urls)):
            if i == len(urls) - 1:
                data.extend(get_book_listing(urls[i], session, num_pages // len(urls) + num_pages % len(urls)))
                break

            data.extend(get_book_listing(urls[i], session, num_pages // len(urls)))
        return data


def populate_db(data):
    for item in data:
        authors = []
        for author_name in item.get('authors'):
            author, created = Author.objects.get_or_create(full_name=author_name)
            authors.append(author)

        genres = []
        for genre_name in item.get('genres'):
            genre, created = Genre.objects.get_or_create(genre=genre_name)
            genres.append(genre)

        book, created = Book.objects.get_or_create(
            title=item.get('title'),
            image=item.get('image'),
            date_published=datetime.strptime(item.get('date_published'), '%Y-%m-%d'),
            stock=randint(0, 100)
        )

        book.authors.set(authors)
        book.genres.set(genres)
        book.save()


class Command(BaseCommand):
    help = 'This command collects and adds the library data to the database'

    def handle(self, *args, **options):
        urls = ['https://bookshop.ge/category/view/fiction', 'https://bookshop.ge/category/view/non-fiction']
        start_time = time.perf_counter()
        self.stdout.write(self.style.SUCCESS('Started collecting book data, this may take approximately 5 minutes...'))
        book_data = get_data(urls, 43)
        end_time = time.perf_counter()
        self.stdout.write(self.style.SUCCESS(f'Finished collecting book data in {end_time - start_time} seconds.'))
        self.stdout.write(self.style.SUCCESS(f'Collected {len(book_data)} books.'))
        start_time = time.perf_counter()
        self.stdout.write(self.style.SUCCESS('Started populating the database...'))
        populate_db(book_data)
        end_time = time.perf_counter()
        self.stdout.write(self.style.SUCCESS(f'Finished populating the database in {end_time - start_time} seconds.'))
