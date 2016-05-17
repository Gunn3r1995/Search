import os

# If directory doesn't exist create new directory
def create_directory(directory):
    if not os.path.exists(directory):
        print('Creating Directory', directory)
        os.makedirs(directory)
create_directory('Shane')


# Create Queue and Crawled files if doesn't Exist
def create_files(project_name, domain_name):
    queue = project_name + '/Queue.txt'
    crawled = project_name + '/Crawled.txt'
    if not os .path.isfile(queue):
        write_file(queue, domain_name)
    if not os .path.isfile(crawled):
        write_file(crawled, '')

# Create and Write to file
def write_file(directory, data):
    file = open(directory, 'w')
    file.write(data)
    file.close()

# Append to a file
def append_file(directory, data):
    with open(directory, 'a') as file:
        file.write(data)
        file.write('\n')

# Delete Content in file
def delete_file(directory):
    with open(directory, 'w'):
        pass






