import requests
from bs4 import BeautifulSoup

class Extract_USC9_Page:

    def __init__(self, page="https://www.ca9.uscourts.gov/"):
        self.page = page
        page_content = requests.get("https://www.ca9.uscourts.gov/").content
        self.soup = BeautifulSoup(page_content, 'html.parser')

    def get_opinion_types(self):
        self.pages = {i.string:i.attrs['href'] for i in self.soup.select('div.bd ul li a') if str(i.string).find('ublished')>0}
        return self.pages