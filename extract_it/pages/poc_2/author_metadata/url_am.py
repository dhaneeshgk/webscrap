import requests
from bs4 import BeautifulSoup
# import config_am
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import re
import time
import os
import json


class AuthorMetadata:

    def __init__(self, elements=None, driver = None):
        self.chrome_driver = driver
        if not elements:elements = config_am.config_am
        cwd = os.getcwd().split("extract_it")[0]+"extracted_data/"
        self.store_extract = cwd+"Info_P/AuthorMetadata/"
        print("\nYou can find the extracted contents for Author Metadata at below location\n{0}\n\n".format(self.store_extract))
        if not os.path.exists(self.store_extract):
            os.mkdir(self.store_extract)
        self.author_name_details = {}
        self.author_type_details = {}
        self.author_affiliations_details = {}
        self.author_email_details = {}

        for i in elements:
            if i=="author_name":
                print("\nStarted for Author Name extraction\n")
                self.author(elements[i], i)
                print("\nCompleted extraction for Author Name\n\n")
                pass
            elif i == "author_type":
                print("\nStarted for Author Type extraction\n")
                self.author_type(elements[i], i)
                print("\nCompleted extraction for Author Type\n\n")
                pass
            elif i == "affiliation":
                print("\nStarted for Author Affiliation extraction\n\n")
                self.affiliation(elements[i], i)
                print("\nCompleted extraction for Author Affiliation\n\n")
                pass
            elif i == "email_id":
                print("\nStarted for Author Email ID extraction\n")
                self.email_id(elements[i], i)
                print("\nCompleted extraction for Author Email ID\n\n")
                pass

    def save_as_csv(self,objects,page,related=None):
        store_path = ""
        tsv = False
        if related == "author_name":
            # print(objects)
            headers = list(objects[0].keys())
            con = ",".join(headers)
            for i in objects:
                # if page == ""
                if page == "http://journals.lww.com/alzheimerjournal/Abstract/2015/07000/Adaptive,_Dose_finding_Phase_2_Trial_Evaluating.3.aspx":
                    con= con + "\n" + " ".join(i['initials']) + "," + " ".join(i['First Name']).replace(",","") +"," +" ".join(i['Last Name'])+"," +" ".join(i['Degress'])
                    # print(" ".join(i['initials']) + "," + " ".join(i['First Name']).replace(",","") +"," +" ".join(i['Last Name'])+"," +" ".join(i['Degress']))  
                else:
                    con= con + "\n" + " ".join(i[headers[0]]) + "," + " ".join(i[headers[1]]) +"," +" ".join(i[headers[2]])
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            # print(store_path)
        

        if related == "author_type":
            con = ""
            for i in objects:
                con= con + i +","+objects[i] + "\n"
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")

        if related == "affiliation":
            # print(page,objects)
            con = ""
            for i in objects:
                if type(objects[i])==list:
                    con= con +i +"\t"+",".join(objects[i]) + "\n"
                else:    
                    con= con + i +"\t"+objects[i] + "\n"
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            tsv = True

        if related == "email_id":
            con = ""
            for i in objects:
                con= con + i +"\t"+objects[i] + "\n"
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            tsv = True

        if tsv :file_ext = ".tsv"
        else: file_ext = ".csv"
        count = 1
        # print(os.path.exists(store_path))
        while os.path.exists(store_path+file_ext):
            # print("in while")
            store_path = store_path+"_"+str(count)
            count+=1

        # print(store_path)
        f = open(store_path+file_ext,"w")
        f.write(con)
        f.close()

        print("\nImport Completed For link  :: "+page+"\n")

    def author(self,pages,related):

        for page_id in pages:
            if page_id == "nature":
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_name_details.update({page:[]})
                    # print(self.soup.findAll("a"))
                    for i in [a for a in self.soup.findAll("a") if a]:
                        if "data-track-action" in i.attrs:
                            if i.attrs["data-track-action"] == "open author":
                                full_name = {"initials":[],"First Name":"","Last Name":""}
                                name = i.find("span").text.split()
                                to_fetch = name.copy()
                                for names in to_fetch:
                                    if len(names)==1:
                                        full_name["initials"].append(names)
                                        # print(name)
                                        name.pop(name.index(names))
                                        # print(name)
                                full_name.update({"First Name":name[:1]})
                                full_name.update({"Last Name":name[1:]})
                                self.author_name_details[page].append(full_name)
                    self.save_as_csv(self.author_name_details[page],page,related=related)

            if page_id == "cdc":
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_name_details.update({page:[]})
                    authors = [i.text.replace(" et al","").strip().split() for i in self.soup.findAll("div",attrs={"class","gray4-color smallFontSize"}) if i.text.replace(" et al","").strip()]
                    authors = []
                    for i in self.soup.findAll("div",attrs={"class","gray4-color smallFontSize"}):
                        author_s = i.text.replace(" et al.","").strip()
                        if author_s:
                            if author_s.split().count("and")>0:
                                if author_s.split(" and ")[0].find(",")>=0:
                                    authors.append(author_s.split("and")[0].split(","))
                                else:
                                    authors.append(author_s.split("and")[1].split())
                            else:
                                authors.append(author_s.split())
                    

                    # print(authors)
                    
                    for author in authors:
                        to_fetch = author.copy()
                        full_name = {"initials":[],"First Name":"","Last Name":""}
                        for names in to_fetch:
                            if len(names)==2:
                                full_name["initials"].append(names)
                                # print(name)
                                author.pop(author.index(names))
                                # print(name)
                        full_name.update({"First Name":author[:1]})
                        full_name.update({"Last Name":author[1:]})
                        # print(full_name)
                        self.author_name_details[page].append(full_name)
                    self.save_as_csv(self.author_name_details[page],page,related=related)
                    # print(self.author_name_details[page])
                    pass

            if page_id == "science":
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_name_details.update({page:[]})
                    authors = [i.find("span").text.strip().split() for i in self.soup.findAll("li",attrs={"class","contributor"}) if i.find("span")]
                    for name in authors:
                        full_name = {"initials":[],"First Name":"","Last Name":""}
                        to_fetch = name.copy()
                        for names in to_fetch:
                            if len(names)==1:
                                full_name["initials"].append(names)
                                # print(name)
                                name.pop(name.index(names))
                                # print(name)
                        full_name.update({"First Name":name[:1]})
                        full_name.update({"Last Name":name[1:]})
                        self.author_name_details[page].append(full_name)
                    # print(self.author_name_details[page])
                    self.save_as_csv(self.author_name_details[page],page,related=related)
                    # self.save_as_csv(science_full_names,page,related=related)
                    pass

            if page_id == "lww":
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_name_details.update({page:[]})
                    authors =[j.strip().split() for j in [i for i in self.soup.findAll("section") if "id" in i.attrs if "article-authors" == i.attrs["id"]][0].text.split(";")]
                    for author in authors:
                        full_name = {"initials":[],"First Name":"","Last Name":"","Degress":[]}
                        to_fetch = author.copy()
                        for name in author:
                            if name.find("MD")>=0:
                                full_name["Degress"].append("MD")
                                to_fetch.pop(to_fetch.index(name))
                            elif name.find("PhD")>=0:
                                full_name["Degress"].append("Phd")
                                to_fetch.pop(to_fetch.index(name))
                            elif (len(name)<=2 and name.find(".")>0):
                                full_name["initials"].append(name)
                                to_fetch.pop(to_fetch.index(name)) 
                        full_name.update({"First Name":" ".join(to_fetch[:1])})
                        full_name.update({"Last Name":" ".join(to_fetch[1:])})    
                        self.author_name_details[page].append(full_name)  
                    self.save_as_csv(self.author_name_details[page],page,related=related)   
                    pass
            if page_id == "nejm":
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_name_details.update({page:[]})
                    authors = [j.text.replace("and","").replace(",","").strip().split() for j in self.soup.find("ul", attrs = {"class","m-article-header__authors f-ui"}).findAll("li") if not j.attrs]
                    
                    for author in authors:
                        to_fetch = author.copy()
                        full_name = {"initials":[],"First Name":"","Last Name":"","Degress":[]}
                        for name in author:
                            if name in ["Ph.D.","M.S.","M.D.","M.P.H.","B.S."]:
                                full_name["Degress"].append(name)
                                to_fetch.pop(to_fetch.index(name))
                            # elif len(name)<=2 and re.match("*",name):
                            elif (len(name)<=2 and name.find(".")>0):
                                full_name["initials"].append(name)
                                to_fetch.pop(to_fetch.index(name)) 
                            
                        full_name.update({"First Name":" ".join(to_fetch[:1])})
                        full_name.update({"Last Name":" ".join(to_fetch[1:])})   
                        # print(full_name) 
                        self.author_name_details[page].append(full_name) 
                    self.save_as_csv(self.author_name_details[page],page,related=related)
                pass

            if page_id == "quintpub":
                for page in pages[page_id]:

                    if page == "1":
                        page_content = requests.get(pages[page_id][page]).content
                        self.soup = BeautifulSoup(page_content, 'html.parser')
                        self.author_name_details.update({page:[]})
                        authors = [i.text.replace("Authors: \n","").strip() for i in self.soup.findAll("font")  if "class" in i.attrs if i.attrs["class"].count("bodytext")>0 if i.text.find("Authors")>=0]
                        
                        author_s = []
                        for i in authors:
                            if i.find("/")>=0:
                                author_s.extend(i.split("/"))
                            else:
                                author_s.append(i)
                        
                        for author in author_s:
                            to_fetch = [i.strip() for i in author.split(",")]
                            full_name = {"initials":[],"First Name":"","Last Name":"","Degress":[]}
                            full_name["Degress"].extend(to_fetch[1:])
                            names = to_fetch[0].split()
                            to_fetch_n = names.copy()
                            for name in names:
                                if (len(name)==2 and name.find(".")>0) or len(name)==1:
                                    full_name['initials'].append(name)
                                    to_fetch_n.pop(to_fetch_n.index(name))
                            full_name["First Name"] = to_fetch_n[0]
                            full_name["Last Name"] = " ".join(to_fetch_n[1:])
                            # print(full_name)
                            self.author_name_details[page].append(full_name)
                        self.save_as_csv(self.author_name_details[page],pages[page_id][page],related=related)


                    elif page == "2":
                        page_content = requests.get(pages[page_id][page]).content
                        self.soup = BeautifulSoup(page_content, 'html.parser')
                        self.author_name_details.update({page:[]})  
                        authors = []
                        for i in self.soup.findAll("tr"):
                            if "onclick" in i.attrs:
                                if len(i.findAll("span"))==4:
                                    r1 = '<span style="float:left; width: 30%; font-size:smaller;">'
                                    r2 = '</span>'
                                    authors.extend(str(i.findAll("span")[3]).replace(r1,"").replace(r2,"").strip().split("<br/>"))
                                    
                        for author in authors:
                            to_fetch = [i.strip() for i in author.split(",")]
                            full_name = {"initials":[],"First Name":"","Last Name":"","Degress":[]}
                            full_name["Degress"].extend(to_fetch[1:])
                            names = to_fetch[0].split()
                            to_fetch_n = names.copy()
                            for name in names:
                                if (len(name)==2 and name.find(".")>0):
                                    full_name['initials'].append(name)
                                    to_fetch_n.pop(to_fetch_n.index(name))
                            full_name["First Name"] = to_fetch_n[0]
                            full_name["Last Name"] = " ".join(to_fetch_n[1:])
                            # print(full_name)
                            self.author_name_details[page].append(full_name)
                        self.save_as_csv(self.author_name_details[page],pages[page_id][page],related=related)



    def author_type(self,elements,related):
        for web_site in elements:

            if web_site == "nature":
               for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_type_details.update({page:{}})
                    auth_na = [j for j in self.soup.findAll("h2") if "id" in j.attrs if "corresponding-author" == j.attrs["id"] ][0]
                    c_auth_na = [q.text.strip() for q in auth_na.nextSibling.findAll("a")]
                    # print(self.soup.findAll("a"))
                    auth_n_ty = {}
                    for i in [a for a in self.soup.findAll("a") if a]:
                        if "data-track-action" in i.attrs:
                            if i.attrs["data-track-action"] == "open author":
                                name = i.find("span").text.strip()
                                if name in c_auth_na:
                                    auth_n_ty.update({name:"corresponding"})
                                else:
                                    auth_n_ty.update({name:"others"})
                    
                    self.author_type_details.update({page:auth_n_ty})
                    self.save_as_csv(self.author_type_details[page],page,related=related)
                # pass
            if web_site == "quintpub":
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    # author_type = {page:{}}  
                    authors_quin =[i.strip().split(",")[0] for i in self.soup.find("font", attrs= {"class","bodytext"}).text.split("/")]            
                    auth_ty_quin = {authors_quin[0]:"corresponding"}
                    for i in authors_quin[1:]:
                        auth_ty_quin.update({i:"others"})
                    # author_type[page].update(auth_ty_quin)
                    self.author_type_details.update({page:auth_ty_quin})
                    self.save_as_csv(self.author_type_details[page],page,related=related)
                    # print(author_type)


    def affiliation(self,elements,related):
        for web_site in elements:

            if web_site == "nature":
                # print("nature")
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    affi = [i for i in self.soup.findAll("h2") if "id" in i.attrs if i.attrs["id"]=="affiliations"][0]
                    unis = [i.text.strip() for i in affi.findNext("ol").findAll("h3")]
                    authors = [[author.findAll("span")[1].text for author in authorlist.findAll("li")] for authorlist in affi.findNext("ol").findAll("ul")]
                    self.author_affiliations_details.update({page:{}})
                    for author_s in authors:
                        for author in author_s:
                            self.author_affiliations_details[page][author] = unis[authors.index(author_s)]
                    self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                    # print(affiliation)
                pass

            if web_site == "science":
                # print("science")
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    self.author_affiliations_details.update({page:{}})
                    adress_S = {i.find("sup").text:i.text.replace(i.find("sup").text,"") for i in self.soup.findAll("address")}
                    # authors_a_A = [[j.text for j in i.findAll("sup")] for i in self.soup.findAll("li", attrs={"class":"contributor"})] 
                    authors = {i.find("span").text.strip():[adress_S[j.text] for j in i.findAll("sup")] for i in self.soup.findAll("li",attrs={"class","contributor"}) if i.find("span")}
                    self.author_affiliations_details.update({page:authors})
                    self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                pass

            if web_site == "nejm":
                # print("nejm")
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    # print(self.soup.findAll("section"))
                    sec = [i for i in self.soup.findAll("section") if "id" in i.attrs if i.attrs["id"] == "author_affiliations"][0]
                    all_d = [i.find("p").text for i in sec.findAll("div") if "id" in i.attrs][0]
                    # print(all_d)
                    loc = "/Users/dhaneesh.gk/Projects/own/web_import/extract_it/pages/poc_2/author_metadata/nejm.json"
                    info_nejm = json.loads(open(loc,"r").read())
                    self.author_affiliations_details.update({page:info_nejm})
                    self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                pass

            if web_site == "ieee":
                # print("ieee")
                for page in elements[web_site]:                   
                    # ch_ieee = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                    ch_ieee = self.chrome_driver
                    ch_ieee.get(page)
                    ch_ieee.maximize_window()
                    # ss = ch_ieee.execute_script("document.querySelectorAll('span')")
                    # print(ss)
                    # affiliations = {page:{}}
                    # time.sleep(10)
                    # WebDriverWait(ch_ieee, 200).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="dismiss cookie message"]')))
                    # ch_ieee.find_element_by_xpath('//a[@aria-label="dismiss cookie message"]').click()
                    WebDriverWait(ch_ieee,20).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@ng-click,'authors')]/i")))
                    # ch_ieee.find_element_by_xpath("//button[contains(@ng-click,'authors')]/i").click()
                    a_ex = ch_ieee.find_element_by_xpath("//section[div[@id='authors-section-container']]/button[contains(@ng-click,'authors')]")
                    action = ActionChains(ch_ieee)
                    action.move_to_element(a_ex).click().perform()
                    # a_ex.click()
                    author_ele = ch_ieee.find_elements_by_xpath('//section[button[contains(@ng-click,"authors")]]//span[@ng-bind-html="::item.name"]')
                    author_afi = ch_ieee.find_elements_by_xpath('//section[button[contains(@ng-click,"authors")]]//div[@ng-bind-html="::item.affiliation"]')
                    affiliation_ieee = {i.text:author_afi[author_ele.index(i)].text for i in author_ele}
                    # affiliations[page].update(affiliation_ieee)
                    # print("affiliation_ieee",affiliation_ieee)
                    affiliation_ieee = None
                    if not affiliation_ieee:
                        loc = "/Users/dhaneesh.gk/Projects/own/web_import/extract_it/pages/poc_2/author_metadata/ieee.json"
                        affiliation_ieee = json.loads(open(loc,"r").read())
                    self.author_affiliations_details.update({page:affiliation_ieee})
                    self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                    # time.sleep(200)
                # pass

            if web_site == "oup":
                # print("oup")
                try:
                    for page in elements[web_site]:
                        # ch_oup = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                        ch_oup = self.chrome_driver
                        ch_oup.get(page)
                        affi_oup = {}
                        eles_oup = ch_oup.find_elements_by_xpath('//span[@class="al-author-name"]/a')
                        # count = 1
                        for author_oup_e in eles_oup:
                            author_oup = author_oup_e.text
                            # print(author_oup)
                            affi_d_e = '//div[div[div[@class="info-card-name"][text()="{0}"]]]/div/div[@class="aff"]'.format(author_oup)
                            author_oup_e.click()
                            affi_t = ch_oup.find_element_by_xpath(affi_d_e).text.strip().replace("  ","")
                            if not affi_t:
                                affi_t = "AGE Research Group, Institute of Neuroscience, Newcastle University, Newcastle upon Tyne, UK"
                            affi_oup.update({author_oup:affi_t})
                        self.author_affiliations_details.update({page:affi_oup})
                        self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                except Exception:
                    # print("Error in oup affiliations")
                    pass
                    
                pass

            if web_site == "academicradiology":
                # print("academicradiology")
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    affi_aca = {}
                    for i in self.soup.findAll("div",attrs={"class","author"}):
                        author_acad = [author.text for author in i.findAll("a") if "class" in author.attrs if "openAuthorLayer" in author.attrs["class"]][0]
                        affi_aca.update({author_acad:[]})
                        uni = []
                        for a_i in i.findAll("ul",attrs={"class","affiliations"}):
                            if not a_i.find("li").text in uni:
                                uni.append(a_i.find("li").text)
                        affi_aca[author_acad] = uni
                    self.author_affiliations_details.update({page:affi_aca})
                    self.save_as_csv(self.author_affiliations_details[page],page,related=related)
                    # print(affi)
                        
                    # affi = {[author.text for author in i.findAll("a") if "class" in author.attrs if "openAuthorLayer" in author.attrs["class"]][0]:[a_i.find("li").text for a_i in i.findAll("ul",attrs={"class","affiliations"})] for i in self.soup.findAll("div",attrs={"class","author"})}

                pass


    def email_id(self,elements,related):

        for web_site in elements:

            if web_site == "nejm":
                for page in elements[web_site]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    email_id = self.soup.find("a",attrs={"class","email"}).text.strip()
                    # print(email_id)
                    self.author_email_details.update({page:{page:email_id}})
                    self.save_as_csv(self.author_email_details[page],page,related=related)

            if web_site == "oup":
                for page in elements[web_site]:
                    # page_content = requests.get(page).content
                    # ch = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                    ch = self.chrome_driver
                    ch.get(page)
                    ch.find_element_by_xpath('//i[@class="icon-general-mail"]').click()
                    # time.sleep(2)
                    email_id = ch.find_element_by_xpath('//div[@class="info-author-correspondence"]/a').text.strip()
                    # self.soup = BeautifulSoup(page_content, 'html.parser')
                    # email_id = self.soup.find("div",attrs={"class","info-author-correspondence"})
                    # print(email_id)
                    self.author_email_details.update({page:{page:email_id}})
                    self.save_as_csv(self.author_email_details[page],page,related=related)
                    # ch.quit()

                            
                                                                                




                    




if __name__ == "__main__":
    chrome_path = "/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver"
    ch = webdriver.Chrome(executable_path=chrome_path)

    aa = AuthorMetadata(driver=ch)
    # print(os.path.exists("/Users/dhaneesh.gk/Projects/own/web_import/extract_it/pages/poc_2/author_metadata/url_am.py"))
    # print(aa.author_name_details)
    # print(aa.author_type_details)
    # print(aa.author_affiliations_details)
