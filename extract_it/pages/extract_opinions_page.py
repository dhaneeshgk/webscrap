import requests
from bs4 import BeautifulSoup


class Extract_Opinions_Page:

    def __init__(self,page='https://www.ca9.uscourts.gov/opinions/'):
        self.page = page
        self.page_content = requests.get(self.page).content
        self.soup = BeautifulSoup(self.page_content,'html.parser')
        self.get_table()
        self.case_details = []
        self.get_case_metadata()
        self.opinions = {}

    def change_page(self,page):
        # self.page = page
        self.page_content = requests.get(page).content
        self.soup = BeautifulSoup(self.page_content,'html.parser')
        self.get_table()
        # self.case_details = []
    
    def get_table(self):
        self.cases = [i for i in self.soup.find('table', attrs={'id':'search-data-table'}).findAll('tr')]
        return self.cases

    def get_case_metadata(self):
        self.metadata_he = [str(header.string).replace("\xa0"," ") for header in self.cases[2].select('th a')]
        # self.opinions.update({"headers":self.metadata_he})
        return self.metadata_he

    
    def get_short_list(self):
        self.metadata_h_s = {str(metadata_h.string).replace("\xa0"," "):metadata_h['href'] for metadata_h in self.cases[2].select('th a')}
        return self.metadata_h_s

    def get_case_details(self):
        for case in self.cases[3:]:
            case_detail = {}
            if case.find('tr'):
                for metadata in case.find('tr').findAll("td"):
                    if metadata.find("a"):
                        if 'href' in metadata.find("a").attrs:
                            case_detail.update({"document":metadata.find("a").attrs['href']})
                    case_detail.update({self.metadata_he[case.findAll("td").index(metadata)]:metadata.string})
                self.case_details.append(case_detail)
            else:
                for metadata in case.findAll("td"):
                    if metadata.find("a"):
                        if 'href' in metadata.find("a").attrs:
                            case_detail.update({"document":metadata.find("a").attrs['href']})
                    case_detail.update({self.metadata_he[case.findAll("td").index(metadata)]:metadata.string})
                self.case_details.append(case_detail)
        return self.case_details

    def get_number_of_records(self):
        self.number_of_cases = self.cases[0].select_one('td tr td').string.strip().split()[-1]
        return self.number_of_cases


    def get_number_of_page(self):
        self.number_of_pages = int(self.cases[0].select('td tr td a')[-1].attrs['href'].split("=")[-1])
        return self.number_of_pages

    def get_all_case_details(self,page_number_count=2):
        if not page_number_count: page_number_count = self.number_of_pages
        for page_number in range(1,page_number_count):
            self.change_page(self.page+"/index.php?pagenumber={0}".format(page_number))
            self.get_case_details()
        return self.case_details

if __name__ == "__main__":
    url = 'https://www.ca9.uscourts.gov/opinions/'
    ss = Extract_Opinions_Page(url)
    print(ss.get_number_of_page())
    print(len(ss.get_all_case_details(1)))
