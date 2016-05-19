import os

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
            print(results)
    return results


# Set to File Converter
def set_to_file_converter(links, file_name):
    with open(file_name, 'w') as file:
        for link in sorted(links):
            file.write(link + '\n')
