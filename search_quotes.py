import mongoengine as me
from models import Author, Quote

me.connect('authors_and_quotes_db', host='YOUR_ATLAS_CONNECTION_STRING')

def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.quote)
    else:
        print(f'No quotes found for author: {name}')

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(quote.quote)

def search_by_tags(tags):
    tag_list = tags.split(',')
    quotes = Quote.objects(tags__in=tag_list)
    for quote in quotes:
        print(quote.quote)

def main():
    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            name = command.split("name:")[1].strip()
            search_by_author(name)
        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            search_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip()
            search_by_tags(tags)
        elif command == "exit":
            break
        else:
            print("Invalid command. Try again.")

if __name__ == '__main__':
    main()
