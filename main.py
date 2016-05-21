import threading
from queue import Queue

from Get_Links import GetLinks
from Crawler import Crawler
from Create import *

queue = Queue()

# Using this url to figure out some of the basic concepts of multi threading
# https://docs.python.org/3/library/threading.html


# Create worker threads (will die when main exits)
def create_threads():
    i = 0
    number_of_threads = 8
    while i < number_of_threads:
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        i += 1


# Do the next job in the queue
def run():
    while True:
        queue_url = queue.get()
        Crawler.crawl(queue_url)
        queue.task_done()


# Each queued link is a new job
def converter_queue(folder_name):
    queue_file = folder_name + '/Queue.txt'
    for queue_url in file_to_set_converter(queue_file):
        queue.put(queue_url)
        queue.join()
        crawl(folder_name)


# Check if there are items in the queue, if so crawl them
def crawl(folder_name):
    queue_file = folder_name + '/Queue.txt'
    # Call file_to_set_converter from Create Class to turn the file to a set
    queued_set = file_to_set_converter(queue_file)
    # If there is 1 or more urls in the set then create job
    if len(queued_set) >= 1:
        urls = str(len(queued_set))
        print(urls, ' links in the queue')
        converter_queue(folder_name)
