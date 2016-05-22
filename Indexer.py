import re
import sys
import string
import sqlite3


class Indexer:

    @staticmethod
    def indexer(current_url, soup):
            print('Current URL', current_url)
            url_dict = {}

            # Get the html text of the soup file
            html = soup.get_text()

            # splits the html into individual words and loops through for every word
            for word in html.split():
                # Strings most unwanted characters
                word.strip(string.punctuation + string.digits + string.whitespace)
                # check whether the work is not in stop list or already found
                from Crawler import Crawler
                if word not in Crawler.stop_list and word not in url_dict:
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
                        #try:
                        # Connect to the Database
                        connect = sqlite3.connect('Indexed_Database.db')
                        cursor = connect.cursor()
                        # Create A table with the rows, Primary Key, Url, word and WordCounts
                        cursor.execute('''CREATE TABLE IF NOT EXISTS WORDs
                                          (Id INTEGER PRIMARY KEY, Url TEXT, word TEXT, WordCount INT);''')
                        # set all words equal to Url, word, WordCount, from the WORDs Table
                        all_words = cursor.execute('SELECT Url, word, WordCount FROM WORDs')
                        # if the word is not in all words continue
                        # Insert the current url, search_term and the amount of times the word was found
                        cursor.execute('''INSERT OR IGNORE INTO WORDs VALUES (NULL, ?, ?, ?);'''
                                       , (current_url, search_term.lower(), len(results)))
                        # select all rows from the table but only show 1 (the last result)
                        cursor.execute('SELECT * FROM WORDs ORDER BY Id DESC LIMIT 1')
                        print(cursor.fetchall())
                        # Commit the changes to the table
                        connect.commit()

    @staticmethod
    def database_output(search_term):

        try:
            connect = sqlite3.connect('Indexed_Database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT Url, word, WordCount FROM WORDs WHERE word=? ORDER BY WordCount DESC;',
                           (search_term,))

            output = cursor.fetchall()

            print('Search Term', search_term)
            print('About', str(len(output)), 'Number of Results\n')

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