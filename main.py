from tkinter import *
from Indexer import Indexer
from Create import *


def init_gui():
    set_url = set()

    def crawl(max_pages):
        queue = str(Crawler.queue.pop())
        console.delete('1.0', END)
        console.insert(END, 'Currently Crawling' + str(queue) + '\n')
        search_engine.update()

        count = int(max_pages)
        while len(Crawler.queue) > 0 and count > 0:
            Crawler.crawl(queue)
            count -= 1

        print('Crawl Finished Can Now Search')
        console.delete('1.0', END)
        console.insert(END, 'Crawl Finished Can Now Search\n')
        console.insert(END, str(len(Crawler.crawled)) + " Url's have been Crawled and Indexed \n")
        console.insert(END, str(len(Crawler.queue)) + " Total Number of Url's In Queue\n")
        search_engine.update()

    def search(search_term):
        search = search_term.lower()
        print("SEARCH", search_term)
        Indexer.database_output(search)

    search_engine = Tk()
    search_engine.title('Search Engine')
    search_engine.geometry('640x480')

    app = Frame(search_engine)
    app.grid()

    folder_name = 'Search_Results'

    label = Label(app, text='Enter Url')
    label.pack()
    label.grid()

    url = Entry(app)
    url.insert(END, '10')
    url.pack()
    url.grid()

    crawl_button = Button(app, text='Start Crawl', command=lambda: crawl(url.get()))
    crawl_button.pack()
    crawl_button.grid()

    label = Label(app, text='Enter a Word to Search')
    label.pack()
    label.grid()

    search_term = Entry(app)
    search_term.insert(END, 'Shane')
    search_term.pack()
    search_term.grid()

    search_button = Button(app, text='Search', command=lambda: search(search_term.get()))
    search_button.pack()
    search_button.grid()

    console = Text(app)
    console.pack()
    console.grid()
    console.insert(END, str(len(Crawler.crawled)) + " Url's have been Crawled and Indexed \n")
    console.insert(END, str(len(Crawler.queue)) + " Total Number of Url's In Queue\n")

    search_engine.mainloop()

Create.create_file()
init_gui()
Crawler.save_crawl_lists()
sys.exit(1)