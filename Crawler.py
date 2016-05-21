import requests
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from Get_Links import GetLinks
from Create import *
import string
import sqlite3
from tkinter import *

class Crawler:
    # initialising Class Variables
    folder_name = ''
    url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    search_file = ''
    indexer_result_file = ''
    queue = set()
    crawled = set()
    url_set = set()
    console_list = ['Welcome to my simple Search Engine \n']

    def __init__(self, folder_name, url, domain_name):
        # Setting Class variables to current values
        Crawler.folder_name = folder_name
        Crawler.url = url
        # Creating Directory's and files
        Crawler.domain_name = domain_name
        Crawler.queue_file = folder_name + '/Queue.txt'
        Crawler.crawled_file = folder_name + '/Crawled.txt'

        self.create()
        # Starting First Crawl
        self.crawl(url)



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
        url = set()

        with open(Crawler.crawled_file, 'rt') as file:
            for line in file:
                url.add(line.replace('\n', ''))

                Crawler.indexer(url)

    @staticmethod
    def indexer(url):
            current_url = url.pop()
            url_source_code = requests.get(current_url)
            # text equals the main text of the source code i.e no headers etc.
            text = url_source_code.text
            # change to beautiful soup format
            soup = BeautifulSoup(text, 'html.parser')

            print('Current URL', current_url)
            url_dict = {}

            # Read In Stop Word List
            with open('stop-word-list.txt', 'rt') as file:
                stop_list = file.read()
                file.close()
            # Get the html text of the soup file
            html = soup.get_text()
            try:
                # splits the html into individual words and loops through for every word
                for word in html.split():
                    # Strings most unwanted characters
                    word.strip(string.punctuation + string.digits + string.whitespace)
                    # check whether the work is not in stop list or already found
                    if word not in stop_list and word not in url_dict:
                        # Make search term equal the value of word
                        search_term = word
                        search_term.strip(string.punctuation + string.digits + string.whitespace)

                        # Get the results from the soup file
                        results = soup.find_all(string=re.compile('.*{0}.*'.format(search_term)), recursive=True)
                        print('Found the word "{0}" {1} times'.format(search_term, len(results)))
                        # if the length of the results is equal to or greater than 1
                        if len(results) >= 1:
                            # Add to the dictionary the already found words
                            url_dict.update({search_term: len(results)})
                            try:
                                # Connect to the Database
                                connect = sqlite3.connect('Indexed_Database.db')
                                cursor = connect.cursor()
                                # Create A table with the rows, Primary Key, Url, word and WordCounts
                                cursor.execute('''CREATE TABLE IF NOT EXISTS WORDs
                                                  (Id INTEGER PRIMARY KEY, Url TEXT, word TEXT, WordCount INT);''')
                                # set all words equal to Url, word, WordCount, from the WORDs Table
                                all_words = cursor.execute('SELECT Url, word, WordCount FROM WORDs')
                                # if the word is not in all words continue
                                if word not in all_words:
                                    # Insert the current url, search_term and the amount of times the word was found
                                    cursor.execute('''INSERT INTO WORDs VALUES (NULL, ?, ?, ?);'''
                                                   , (current_url, search_term, len(results)))
                                    # select all rows from the table but only show 1 (the last result)
                                    cursor.execute('SELECT * FROM WORDs ORDER BY Id DESC LIMIT 1')
                                    print(cursor.fetchall())
                                    # Commit the changes to the table
                                    connect.commit()
                            # Except clause to keep the programme running if there is an error
                            except sqlite3.Error as e:

                                if connect:
                                    connect.rollback()

                                print('Error %s:' % e.args[0])
                                sys.exit(1)

                            finally:
                                # Close the connect with the database
                                if connect:
                                    connect.close()
            except:
                print('Error')
                pass

    @staticmethod
    def database_output(search_term):

        try:
            connect = sqlite3.connect('Indexed_Database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT Url, word, WordCount FROM WORDs WHERE word=? ORDER BY WordCount DESC;',
                           (search_term,))

            output = cursor.fetchall()

            print('Search Term', search_term)
            print('About Number of Results', str(len(output)), '\n')

            if len(output) >= 1:
                for lines in output:
                    print(lines)
                    print('-----------------------------------\n')
            else:
                print('Your search -', search_term, '- did not match any documents.')

        except sqlite3.Error as e:

            if connect:
                connect.rollback()

                print('Error %s:' % e.args[0])
                sys.exit(1)

        finally:

            if connect:
                connect.close()

    @staticmethod
    def init_gui():

        def start_crawl(folder_name, url, domain_name):
            search_engine.update()
            Crawler(folder_name, url, domain_name)

            import main
            main.create_threads()
            main.crawl(folder_name)

            Crawler.read_file()

            search_engine.update()

        def search():
            print('Implement Search')

        search_engine = Tk()
        search_engine.title('Search Engine')
        search_engine.geometry('640x480')

        app = Frame(search_engine)
        app.grid()

        label = Label(app, text='Enter Unique Folder Name')
        label.pack()
        label.grid()

        folder_name = Entry(app)
        folder_name.pack()
        folder_name.grid()

        label = Label(app, text='Enter Url')
        label.pack()
        label.grid()

        url = Entry(app)
        url.insert(END, 'http://shanesmithcv.com/')
        url.pack()
        url.grid()

        crawl_button = Button(app, text='Start Crawl', command=lambda: start_crawl(folder_name.get(), url.get(), url.get()))
        crawl_button.pack()
        crawl_button.grid()

        label = Label(app, text='Enter a Word to Search')
        label.pack()
        label.grid()

        search_term = Entry(app)
        search_term.insert(END, 'Shane')
        search_term.pack()
        search_term.grid()

        search_button = Button(app, text='Search', command=lambda: search())
        search_button.pack()
        search_button.grid()

        search_engine.mainloop()

Crawler.init_gui()
