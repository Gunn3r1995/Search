import os
import sqlite3

# http://www.tutorialspoint.com/python/python_files_io.htm
# Opening and closeing files etc learned from this website


# If directory doesn't exist create new directory
def create_directory(directory):
    if not os.path.exists(directory):
        print('Creating Directory', directory)
        os.makedirs(directory)


# Create Queue and Crawled files if doesn't Exist
def create(project_name, base_url):
    queue = project_name + '/Queue.txt'
    crawled = project_name + '/Crawled.txt'
    if not os .path.isfile(queue):
        write(queue, base_url)
    if not os .path.isfile(crawled):
        write(crawled, '')


# Create and Write to file
def write(directory, data):
    file = open(directory, 'w')
    file.write(data)
    file.close()

    '''
    try:
        # Connect to the Database
        connect = sqlite3.connect('Queue_Database.db')
        cursor = connect.cursor()
        # Create A table with the rows, Primary Key, Url, word and WordCounts
        cursor.execute(''''''CREATE TABLE IF NOT EXISTS QUEUED_URLs
                          (Id INTEGER PRIMARY KEY, Url TEXT);'''''')
        # set all words equal to Url, word, WordCount, from the WORDs Table
        all_words = cursor.execute('SELECT Url FROM QUEUED_URLs')
        # if the word is not in all words continue
        # Insert the current url, search_term and the amount of times the word was found
        cursor.execute(''''''INSERT INTO QUEUED_URLs VALUES (NULL, ?);''''''
                       , (url))
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
            connect.close()'''


# Append to a file
def append(directory, data):
    with open(directory, 'a') as file:
        file.write(data)
        file.write('\n')

# http://stackoverflow.com/questions/874017/python-load-words-from-file-into-a-set
# Set to file and vis verse helped from this website

# File to Set Converter
def file_to_set_converter(file_name):
    results = set()
    with open(file_name, 'rt') as file:
        for line in file:
            results.add(line.replace('\n', ''))
    return results


# Set to File Converter
def set_to_file_converter(links, file_name):
    with open(file_name, 'w') as file:
        for link in sorted(links):
            file.write(link + '\n')
        file.close()