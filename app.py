
from extract_it.pages.extract_opinions_page import Extract_Opinions_Page
from extract_it.pages.extract_memoranda_page import Extract_Memoranda_Page
from extract_it.pages.extract_usc9_page import Extract_USC9_Page
from wittyparrot_sdk.wittyparrot_apis import WittyParrot_Apis
import user_details as yu
from imp import reload

class Import_Web_To_WittyParrot:

    def __init__(self, url=""):
        self.user = WittyParrot_Apis(username=yu.user["user_id"],password=yu.user["password"],env=yu.user["env"])
        self.folders = [i.upper() for i in yu.user['url'].split("/")[2].split(".") if not i in ["www"]]
        self.folders.reverse()
        self.case_details = {}

    def re_do(self):
        reload(yu)
        self.user = WittyParrot_Apis(username=yu.user["user_id"],password=yu.user["password"],env=yu.user["env"])
        self.folders = [i.upper() for i in yu.user['url'].split("/")[2].split(".") if not i in ["www"]]
        self.folders.reverse()
        self.case_details = {}

    def check_models_present(self):
        models = {model["name"]:model["id"] for model in self.user.list_models()}
        if not yu.user["model"] in models:
            return {"status":False, "message":"Model {0} Not exists please create and move forward".format(yu.user["model"])}
        else:
            return {"status":True}

    def extract_web_data(self):
        op_types = Extract_USC9_Page(yu.user["url"]).get_opinion_types()
        for i in op_types:
            if op_types[i].find("https")<0:
                n_url =  "https:"+op_types[i]
            if i == "Published":
                pu = Extract_Opinions_Page(n_url)
                pu.get_number_of_page()
                pu_case_details = pu.get_all_case_details(2)
                self.case_details.update({i:{"case_details":pu_case_details,"headers":pu.get_case_metadata()}})
            elif i == "Unpublished":
                upu = Extract_Memoranda_Page(n_url)
                upu_case_details = upu.get_case_details()
                self.case_details.update({i:{"case_details":upu_case_details,"headers":upu.get_case_metadata()}})
        return self.case_details


    









if __name__ == "__main__":
    cd = Import_Web_To_WittyParrot()
    cd.check_models_present()
    len(cd.extract_web_data())
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





    

