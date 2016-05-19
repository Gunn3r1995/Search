import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from Get_Links import GetLinks
from Create import *
import re


class Crawler:
    # initialising Class Variables
    folder_name = ''
    url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    url_dict = {}
    word_dict = {}

    def __init__(self, folder_name, url, domain_name):
        # Setting Class variables to current values
        Crawler.folder_name = folder_name
        Crawler.url = url
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.folder_name + '/Queue.txt'
        Crawler.crawled_file = Crawler.folder_name + '/Crawled.txt'
        # Creating Directory's and files
        self.create()
        # Starting First Crawl
        self.crawl(Crawler.url)

    @staticmethod
    def create():
        # Runs methods in Create class
        # Creates a directory if not already created
        create_directory(Crawler.folder_name)
        create(Crawler.folder_name, Crawler.url)
        Crawler.queue = file_to_set_converter(Crawler.queue_file)
        Crawler.crawled = file_to_set_converter(Crawler.crawled_file)

    @staticmethod
    def crawl(url):
        if url not in Crawler.crawled:
            length_queue = str(len(Crawler.queue))
            length_crawled = str(len(Crawler.crawled))
            print('Total Waiting', length_queue, '| Total Crawled', length_crawled)

            Crawler.urls_to_queue(Crawler.get_links(url))

            Crawler.queue.remove(url)
            Crawler.crawled.add(url)

            # Update the txt Files
            set_to_file_converter(Crawler.queue, Crawler.queue_file)
            set_to_file_converter(Crawler.crawled, Crawler.crawled_file)

    # Convert the human readable links from Get Links to computer Readable links for crawler
    @staticmethod
    def get_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            get_links = GetLinks(Crawler.url, page_url)
            get_links.feed(html_string)
        except:
            print('Error: Cannot Crawl Page, url', page_url, 'may not exists')
            return set()
        return get_links.return_links()

    # Check if haven't Crawled and if is within the domain name
    @staticmethod
    def urls_to_queue(urls):
        for url in urls:
            if url in Crawler.queue:
                continue
            if url in Crawler.crawled:
                continue
            if Crawler.domain_name not in url:
                if 'http' in str(url):
                    print('Url Found but not within website Domain', url)
                    Crawler.crawled.add(url)
                continue
            Crawler.queue.add(url)

    @staticmethod
    def read_file():
        search_term = input("Please Enter Word: ")
        url = set()
        print(search_term)
        with open(Crawler.crawled_file, 'rt') as file:
            for line in file:
                url.add(line.replace('\n', ''))
                Crawler.indexer(search_term, url)

    @staticmethod
    def indexer(search_term, url):
        print('Search term', search_term)

        current_url = url.pop()

        print("Current URL", current_url)

        url_source_code = requests.get(current_url)
        # text equals the main text of the source code i.e no headers etc.
        text = url_source_code.text
        # change to beautiful soup format
        soup = BeautifulSoup(text, "html.parser")

        results = soup.find_all(string=re.compile('.*{0}.*'.format(search_term)), recursive=True)
        if len(results) > 0:
            print('Results', len(results))
            Crawler.url_dict.update({search_term : len(results)})
            Crawler.word_dict.update({current_url : Crawler.url_dict})

            print(Crawler.word_dict)
