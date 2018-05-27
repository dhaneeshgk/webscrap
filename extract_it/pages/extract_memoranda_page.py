import requests
from bs4 import BeautifulSoup


class Extract_Memoranda_Page:

    def __init__(self,page='https://www.ca9.uscourts.gov/memoranda/'):
        self.page = page
        self.page_content = requests.get(self.page).content
        self.soup = BeautifulSoup(self.page_content,'html.parser')
        self.case_details = []
        self.get_case_metadata()
        self.memorandas = {}

    def get_case_metadata(self):
        self.metadata_he =[i.string for i in self.soup.find('tr',attrs={"id":"c_row_"}).select('th a b')]
        self.memorandas.update({"headers":self.metadata_he})
        return self.metadata_he

    def get_case_details(self):
        self.case_details = [] 
        for case in self.soup.select('table tbody')[0].findAll('tr')[0:1]:
            case_detail = {}
            for detail in case.findAll('td'):
                if detail.find('a'):
                    case_detail.update({'document':detail.find('a').attrs['href']})
                case_detail.update({self.metadata_he[case.findAll("td").index(detail)]:detail.string})
            self.case_details.append(case_detail)
        return self.case_details

    def get_number_of_records(self):
        self.number_of_cases = self.soup.findAll('td', attrs = {"align":"left", "class":"dg_nowrap"})[0].string.strip().split(" ")[-1]
        return self.number_of_cases






if __name__ == "__main__":
    url = 'https://www.ca9.uscourts.gov/memoranda/'
    ss = Extract_Memoranda_Page(url)
    print(ss.get_number_of_records())
    # print(ss.get_case_details())
    
