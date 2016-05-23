import string
import sqlite3


class Indexer:

    @staticmethod
    def indexer(current_url, soup):
            print('Current URL', current_url)
            url_dict = {}
            # Get the html text of the soup file
            html = soup.get_text()

            for character in string.punctuation:
                html = html.replace(character, " ")
            html.encode('utf8')

            # Connect to the Database
            connect = sqlite3.connect('Indexed_Database.db')
            cursor = connect.cursor()

            # splits the html into individual words and loops through for every word
            for word in html.split():
                # check whether the work is not in stop list or already found
                from Crawler import Crawler
                if word not in Crawler.stop_list and word not in url_dict:
                    # Make search term equal the value of word
                    search_term = word

                    results = html.count(search_term)
                    print('Found word: ', search_term, results, ' Times')
                    html.replace(search_term, " ")

                    # if the length of the results is equal to or greater than 1
                    if search_term not in Crawler.stop_list:
                        if results >= 2 and result <= 35:
                            # Add to the dictionary the already found words
                            url_dict.update({search_term: results})

                            # Create A table with the rows, Primary Key, Url, word and WordCounts
                            cursor.execute('''CREATE TABLE IF NOT EXISTS WORDs
                                              (Id INTEGER PRIMARY KEY, Url TEXT, word TEXT, WordCount INT);''')
                            # if the word is not in all words continue
                            # Insert the current url, search_term and the amount of times the word was found
                            cursor.execute('''INSERT OR IGNORE INTO WORDs VALUES (NULL, ?, ?, ?);'''
                                           , (current_url, search_term.lower(), results))
                            # select all rows from the table but only show 1 (the last result)
                            cursor.execute('SELECT * FROM WORDs ORDER BY Id DESC LIMIT 1')
                            print(cursor.fetchall())
                            # Commit the changes to the table
                            connect.commit()
            connect.close()
