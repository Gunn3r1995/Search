import re
import urllib.request
from bs4 import BeautifulSoup
from Indexer import Indexer


class Crawler:
    # initialising Class Variables
    stop_list = set()
    queue = set()
    crawled = set()

    @staticmethod
    def crawl(current_url):
        print('Total in Queue', len(Crawler.queue), '| Total Crawled', len(Crawler.crawled))
        try:
            with urllib.request.urlopen(current_url) as response:
                html = response.read()

            soup = BeautifulSoup(html, "html.parser")
            print(" crawling", current_url)
            for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
                href = link.get('href')
                if href not in Crawler.queue and href not in Crawler.crawled:
                    Crawler.queue.add(href)
            Crawler.crawled.add(current_url)
            Crawler.queue.discard(current_url)
            Indexer.indexer(current_url, soup)
            Crawler.save_crawl_lists()
        except:
            print("ERROR", current_url)
            Crawler.queue.discard(current_url)
            Crawler.save_crawl_lists()
            pass

    @staticmethod
    def save_crawl_lists():
        with open('Search/Queue.txt', 'w') as file:
            for link in Crawler.queue:
                file.write(link + '\n')
            file.close()

        with open('Search/Crawled.txt', 'w') as file:
            for link in Crawler.crawled:
                file.write(link + '\n')
            file.close()

    @staticmethod
    def read_file(directory):
        if directory == 'Search/Queue.txt':
            with open('Search/Queue.txt', 'rt') as file:
                    for line in file:
                        Crawler.queue.add(line.replace('\n', ''))
                    file.close()

        if directory == 'Search/Crawled.txt':
            with open('Search/Crawled.txt', 'rt') as file:
                for line in file:
                    Crawler.crawled.add(line.replace('\n', ''))
                file.close()

        if directory == 'Search/stop_word_list.txt':
            with open('Search/stop_word_list.txt', 'rt') as file:
                for line in file:
                    Crawler.stop_list.add(line.replace('\n', ''))
                file.close()
