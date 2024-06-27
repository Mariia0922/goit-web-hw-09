import json
import mongoengine as me
from models import Author, Quote


from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://cr1:<cr1>@cluster0.8qrjkg8.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)





def load_authors(filename):
    with open(filename, 'r') as file:
        authors = json.load(file)
        for author in authors:
            Author(**author).save()

def load_quotes(filename):
    with open(filename, 'r') as file:
        quotes = json.load(file)
        for quote in quotes:
            author_name = quote.pop('author')
            author = Author.objects(fullname=author_name).first()
            Quote(author=author, **quote).save()

if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('quotes.json')
