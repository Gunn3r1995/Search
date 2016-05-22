import os
from Crawler import Crawler


class Create:

    @staticmethod
    def create_file():
        if not os.path.exists('Search/Queue.txt'):
            file = open('Search/Queue.txt', 'w')
            file.write('http://shanesmithcv.com')
            file.close()

            Crawler.read_file('Search/Queue.txt')
        else:
            Crawler.read_file('Search/Queue.txt')

        if not os .path.isfile('Search/Crawled.txt'):
            file = open('Search/Crawled.txt', 'w')
            file.write('')
            file.close()

            Crawler.read_file('Search/Crawled.txt')
        else:
            Crawler.read_file('Search/Crawled.txt')

        Crawler.read_file('Search/stop_word_list.txt')