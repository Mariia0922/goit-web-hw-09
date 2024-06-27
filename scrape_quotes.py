import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_quotes():
    quotes = []
    authors = []
    authors_set = set()
    
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        soup = get_soup(url)
        
        quote_divs = soup.find_all("div", class_="quote")
        if not quote_divs:
            break
        
        for quote_div in quote_divs:
            quote_text = quote_div.find("span", class_="text").get_text()
            author_name = quote_div.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
            
            quotes.append({
                "author": author_name,
                "quote": quote_text,
                "tags": tags
            })
            
            if author_name not in authors_set:
                author_url = BASE_URL + quote_div.find("a")["href"]
                author_soup = get_soup(author_url)
                
                born_date = author_soup.find("span", class_="author-born-date").get_text()
                born_location = author_soup.find("span", class_="author-born-location").get_text()
                description = author_soup.find("div", class_="author-description").get_text().strip()
                
                authors.append({
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                })
                authors_set.add(author_name)
        
        page += 1
    
    return quotes, authors

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    quotes, authors = scrape_quotes()
    save_json(quotes, "quotes.json")
    save_json(authors, "authors.json")
