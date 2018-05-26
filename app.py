import requests
from bs4 import BeautifulSoup

con = requests.get('https://www.ca9.uscourts.gov/opinions/').content
# print(con)

soup  = BeautifulSoup(con,'html.parser')
soup.select_one()
for i in soup.find_all('a'):
    print(i.string)

