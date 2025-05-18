import requests
from bs4 import BeautifulSoup
import json

def scrape_books(url="http://books.toscrape.com"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('.price_color').text
        books.append({'title': title, 'price': price})
    return books

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_from_file(filename='books.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def search_book(data, query):
    return [book for book in data if query.lower() in book['title'].lower()]

