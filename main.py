import sqlite3
from tkinter import *
from Crawler import Crawler


def init_gui():
    def crawl(max_page):
        text.delete('1.0', END)
        text.insert(END, 'Currently Crawling Please Wait\n')
        search_engine.update()

        count = int(max_page)
        while len(Crawler.queue) > 0 and count > 0:
            queue = str(Crawler.queue.pop())
            Crawler.crawl(queue)
            count -= 1
            text.insert(END, 'Currently Crawling: ' + queue + '\n')
            search_engine.update()

        print('Crawl Finished Can Now Search')
        text.delete('1.0', END)
        text.insert(END, 'Crawl Finished Can Now Search\n')
        text.insert(END, str(len(Crawler.crawled)) + " Url's have been Crawled and Indexed \n")
        text.insert(END, str(len(Crawler.queue)) + " Total Number of Url's In Queue\n")
        search_engine.update()

        Crawler.save_lists()

    def search(search):
        global connect
        search_term = search.lower()
        try:
            connect = sqlite3.connect('Indexed_Database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT Url, word, WordCount FROM WORDs WHERE word=? ORDER BY WordCount DESC;',
                           (search_term,))

            output = cursor.fetchall()

            text.delete('1.0', END)
            text.insert(END, 'Search Term - ' + search_term + '\n')
            text.insert(END, 'About ' + str(len(output)) + ' Number of Results Found\n\n\n')
            search_engine.update()

            print('Search Term', search_term)
            print('About', str(len(output)), 'Number of Results\n')
            if len(output) >= 1:
                for lines in output:
                    text.insert(END, str(lines) + '\n\n')
                    text.insert(END, '-------------------------------------------\n')
                    search_engine.update()

                    print(lines)
                    print('-----------------------------------\n')
            else:
                text.insert(END, 'Your search - ' + search_term + ' - did not match any documents.\n')
                search_engine.update()
                print('Your search - ' + str(search_term) + ' - did not match any documents.\n')

        except sqlite3.Error as e:

            if connect:
                connect.rollback()

                print('Error %s:' % e.args[0])
                sys.exit(1)

        finally:

            if connect:
                connect.close()

    search_engine = Tk()
    search_engine.title('Search Engine')
    search_engine.geometry('600x600')

    window = Frame(search_engine)
    window.grid()

    label = Label(window, text="Enter Maximum Number of Url's to Crawl")
    label.pack()

    max_pages = Entry(window)
    max_pages.insert(END, '10')
    max_pages.pack()

    crawl_button = Button(window, text='Start Crawl', command=lambda: crawl(max_pages.get()))
    crawl_button.pack()

    label = Label(window, text='Enter a Word to Search')
    label.pack()

    search_input = Entry(window)
    search_input.insert(END, 'Shane')
    search_input.pack()

    search_button = Button(window, text='Search', command=lambda: search(search_input.get()))
    search_button.pack()

    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(window, wrap=WORD, yscrollcommand=scrollbar.set)
    text.pack()

    scrollbar.config(command=text.yview)

    text.insert(END, str(len(Crawler.crawled)) + " Url's have been Crawled and Indexed \n")
    text.insert(END, str(len(Crawler.queue)) + " Total Number of Url's In Queue\n")

    search_engine.mainloop()

Crawler.create_file()
init_gui()

Crawler.save_lists()
sys.exit()
