from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib import parse


class GetLinks(HTMLParser):

    # Main Initialise Method
    def __init__(self, base_url, current_url):
        super().__init__()
        self.base_url = base_url
        self.current_url = current_url
        self.links = set()

    # Get domain name
    @staticmethod
    def get_domain_name(url):
        try:
            return urlparse(url).netloc
        except:
            return ''

    # Get Links in all start tags using built in function handle_starttag(self, tag, attrs)
    def handle_starttag(self, tag, attrs):
        try:
            # only get tags with a
            if tag == 'a':
                for (attribute, value) in attrs:
                    # only get attributes with href
                    if attribute == 'href':
                        # get and add the url to the links set
                        url = parse.urljoin(self.base_url, value)
                        self.links.add(url)
        except:
            print("Error Url may not exist")

    # Return Links
    def return_links(self):
        return self.links

    # Default error class
    def error(self, message):
        pass
