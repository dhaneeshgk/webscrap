
import requests
from bs4 import BeautifulSoup


def app():
    pass







# url3 = 'https://www.ca9.uscourts.gov/memoranda/'

# con = requests.get(url3).content

# soup  = BeautifulSoup(con,'html.parser')
# metadata_he = [i.string for i in soup.find('tr',attrs={"id":"c_row_"}).select('th a b')]

# number_of_records = soup.findAll('td', attrs = {"align":"left", "class":"dg_nowrap"})[0].string.strip().split(" ")[-1]

# case_details=[]
# for case in soup.select('table tbody')[0].findAll('tr')[0:1]:
#     case_detail = {}
#     for detail in case.findAll('td'):
#         if detail.find('a'):
#             case_detail.update({'document':detail.find('a').attrs['href']})
#         case_detail.update({metadata_he[case.findAll("td").index(detail)]:detail.string})
#     case_details.append(case_detail)







# url2 = 'https://www.ca9.uscourts.gov/opinions/'

# con = requests.get(url2).content

# soup  = BeautifulSoup(con,'html.parser')

# cases = [i for i in soup.find('table', attrs={'id':'search-data-table'}).findAll('tr')]

# pages = {page.string:page.attrs['href'] for page in cases[1].select('td a') if 'href' in page.attrs}

# metadata_he = [str(header.string).replace("\xa0"," ") for header in cases[2].select('th a')]

# metadata_h_s = {str(metadata_h.string).replace("\xa0"," "):metadata_h['href'] for metadata_h in cases[2].select('th a')}

# case_details = []
# for case in cases[3:]:
#     case_detail = {}
#     if case.find('tr'):
#         for metadata in case.find('tr').findAll("td"):
#             if metadata.find("a"):
#                 if 'href' in metadata.find("a").attrs:
#                     case_detail.update({"document":metadata.find("a").attrs['href']})
#             case_detail.update({metadata_he[case.findAll("td").index(metadata)]:metadata.string})
#         case_details.append(case_detail)
#     else:
#         for metadata in case.findAll("td"):
#             if metadata.find("a"):
#                 if 'href' in metadata.find("a").attrs:
#                     case_detail.update({"document":metadata.find("a").attrs['href']})
#             case_detail.update({metadata_he[case.findAll("td").index(metadata)]:metadata.string})
#         case_details.append(case_detail)


# print(pages)
# print(metadata_h_s)
# print(metadata_he)
# print(case_details)





    

