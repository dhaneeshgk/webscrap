import requests
from bs4 import BeautifulSoup
import config_mo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import os
import time

class ArticleMetadata:

    def __init__(self, elements=None):
        if not elements:elements = config_mo.elements
        cwd = os.getcwd().split("extract_it")[0]+"extracted_data/"
        self.store_extract = cwd+"Info_P/ArticleMetadata/"
        if not os.path.exists(self.store_extract):
            os.mkdir(self.store_extract)
        self.art_titels = {}
        self.art_abstracts = {}
        self.art_subtitle = {}
        self.oa_art_details = {}
        for i in elements:
            # print(i)
            if i=="title":
                # self.article_title(elements[i], i)
                pass
            elif i == "sub_title":
                # self.article_sub_title(elements[i], i)
                pass
            elif i == "abstract":
                self.abstract_text(elements[i], i)
                pass
            elif i == "OA_Art":
                # self.oa_art(elements[i], i)
                pass

    def save_as_csv(self,objects,page,related=None,page_id=None):
        store_path = ""
        tsv = False
        html = False
        if related == "title":
            con = "title"
            for i in objects:
                con= con + "\n" + i
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            # print(store_path)
        

        if related == "sub_title":
            con = "sub_title"
            for i in objects:
                con= con + "\n" + i
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            # print(store_path)

        if related == "abstract":
            con = objects
            html = True
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")


        if related == "OA_Art":
            # print(objects)
            if page_id == "jes":
                con = "title\tOA\tArticle Type\n"
            else:
                con = "title\tOA\n"
            for i in objects:
                if len(objects[i].values())>1:
                    con= con + i +"\t"+objects[i]["OA"]+"\t"+objects[i]["Article Type"]+"\n"
                else:
                    con= con + i +"\t"+objects[i]["OA"]+"\n"
            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")
            tsv = True
        print("\n\n")
        if tsv :file_ext = ".tsv"
        elif html: file_ext = ".html"
        else: file_ext = ".csv"
        count = 1
        # print(os.path.exists(store_path))
        while os.path.exists(store_path+file_ext):
            print("in while")
            store_path = store_path+"_"+str(count)
            count+=1

        print(store_path)
        f = open(store_path+file_ext,"w")
        f.write(con)
        f.close()        

    def article_title(self,pages, related):

        for page_id in pages:

            if page_id == "jes":
                pass
                print("in jes")
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                lists = [i for i in self.soup.find("form", attrs={"action":"/gca"}).findAll("div") if i.attrs["class"].count("toc-level")>0]
                titles_jes = []
                for i in lists:
                    data_extracted = {}

                    lists2 = [j for j in i.findAll("div") if j.attrs["class"].count("toc-level")>0]
                    
                    if lists2:
                        if i.find("h2"): data_extracted.update({i.find("h2").text:{}})
                        # count_q = 0
                        for q in lists2:
                            if q.find("h3"):
                                data_extracted[i.find("h2").text].update({q.find("h3").text:[]})
                                for l in q.findAll("h4",attrs={"class","cit-title-group"}):
                                    data_extracted[i.find("h2").text][q.find("h3").text].append(l.text.strip().replace("\n",""))
                                titles_jes.append(l.text.strip().replace("\n",""))
                    else:
                        print("in h2 jes")
                        if i.find("h2"): 
                            data_extracted.update({i.find("h2").text:[]})
                            for l in i.findAll("h4",attrs={"class","cit-title-group"}):
                                data_extracted[i.find("h2").text].append(l.text.strip().replace("\n",""))
                                titles_jes.append(l.text.strip().replace("\n",""))
                    # data.update(data_extracted)
                # print(data)
                self.save_as_csv(titles_jes, pages[page_id],related)
                # print(titles_jes)
                print("end of jes")

            elif page_id=="iopscience":
                pass
                print("in iopscience")
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                lists_article_title = [i.text.strip() for i in self.soup.findAll("a",attrs={"class","art-list-item-title"})]
                # lists_authors = [i.text.strip() for i in self.soup.findAll("p",attrs={"class","small art-list-item-meta"})] 
                # abstract_text = [i.find("p").text for i in self.soup.findAll("div",attrs={"class","article-text wd-jnl-art-abstract cf"})]
                # pdfs_link = [i.findAll("a")[2].attrs["href"] for i in self.soup.findAll("div",attrs={"class","art-list-item-tools small"}) if i.findAll("a",attrs={"class","mr-2 nowrap"}) ]
                # oa_or_not = []
                # for i in self.soup.findAll("div",attrs={"class","eyebrow"}):
                #     if i.findAll("a",attrs={"class","mr-2 nowrap"}):
                #         oa_or_not.append({"OA":True})
                #     else:
                #         oa_or_not.append({"OA":False})
                # print(oa_or_not)
                # print(lists_article_title)
                self.save_as_csv(lists_article_title, pages[page_id],related)
                print("end of iopscience")

            elif page_id=="scrip":
                driver_scrip = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                driver_scrip.get(pages[page_id])
                time.sleep(10)
                driver_scrip.refresh()
                article_titles_scrip =[i.text.strip() for i in driver_scrip.find_elements_by_xpath("//ul[div[contains(@id,'JournalInfor_Repeater_Papers')]]/p/a[@name]")]
                # print(article_titles_scrip)
                self.save_as_csv(article_titles_scrip, pages[page_id],related)
            
            elif page_id=="sciencedirect":
                pass
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                article_titels = []
                for i in self.soup.findAll("h3", attrs={"class","text-m u-display-inline"}):
                    for j in i.findAll("span"):
                        if j.attrs:
                            if article_titels.count(j.text)==0:
                                article_titels.append(j.text)
                # print(article_titels)
                self.save_as_csv(article_titels, pages[page_id],related)
                            
            elif page_id=="jsac":
                pass
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                articles = []
                article_titels = []
                for i in self.soup.findAll("div",attrs={"class","article"}):
                    data_extracted = {}
                    title = i.find("div",attrs={"class","title"}).text
                    authors = i.find("div",attrs={"class","author"}).text
                    journal = i.find("div",attrs={"class","journal"}).text
                    links = {j.text:"http://www.jsac.or.jp"+j.attrs["href"] for j in i.findAll("a") if "href" in j.attrs}
                    image = "http://www.jsac.or.jp"+i.find("img").attrs["src"]
                    data_extracted.update({"title":title,"authors":authors,"journal":journal,"links":links,"image":image})
                    article_titels.append(title)
                    articles.append(data_extracted)
                # print(article_titels)
                self.save_as_csv(article_titels, pages[page_id],related)
            

    def article_sub_title(self,pages, related):

        for page_id in pages:

            if page_id == "kunststoffe":
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                # title = self.soup.find("h1").text
                sub_title = self.soup.findAll("h2")[0].text
                # pdf_link = "https://www.kunststoffe.de/"+self.soup.find("h5").find("a").attrs["href"]
                # article_info = self.soup.find("p",attrs={"class","article-intro"}).text
                # author = self.soup.find("p",attrs={"class","author"}).text

                self.art_subtitle.update({pages[page_id]:sub_title})
                self.save_as_csv([sub_title], pages[page_id],related)
                # print(title)
                # print(sub_title)
                # print(pdf_link)
                # print(article_info)
                # print(author)

    def abstract_text(self,pages, related):

        for page_id in pages:

            if page_id == "ems-ph":
                page_content = requests.get(pages[page_id]).content
                self.soup = BeautifulSoup(page_content, 'html.parser')
                abstract_text = self.soup.findAll("span")[1].text
                self.art_abstracts.update({pages[page_id]:{"abstract":abstract_text}})
                self.save_as_csv(abstract_text, pages[page_id],related)
                pass

            if page_id == "springeropen":
                # abstracts = {}
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')
                    content="<html><body>{0}</body></html>"
                    content = content.format(self.soup.find("section",attrs={"class","Abstract Section1 RenderAsSection1"}))
                    # print(content,"\n\n")
                    self.save_as_csv(content, page,related)
                    self.art_abstracts.update({page:{"abstract":content}})
                    # abstracts.update({page:{"abstract":content}})
                pass

            if page_id == "jes":
                # abstracts = {}
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')   
                    content="<html><body>{0}</body></html>"
                    data_extracted = self.soup.find("div",attrs={"class","section abstract"})
                    src_s = [i.attrs['src'] for i in data_extracted.findAll("img")]
                    for img_s in src_s:
                        img = "/".join(page.split("/")[:-1])+"/"+img_s
                        content = content.format(data_extracted).replace(img_s, img )
                    # print(content,"\n\n")
                    self.save_as_csv(content, page,related)
                    self.art_abstracts.update({page:{"abstract":content}})
                    # abstracts.update({page:{"abstract":content}})       
                pass
            if page_id == "springer":
                # abstracts = {}
                for page in pages[page_id]:
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')   
                    content="<html><body>{0}</body></html>"
                    data_extracted = self.soup.find("section",attrs={"class","Abstract"})
                    content = content.format(data_extracted)
                    # print(content,"\n\n")
                    self.save_as_csv(content, page,related)
                    self.art_abstracts.update({page:{"abstract":content}})
                    # abstracts.update({page:{"abstract":content}})       
                    pass
            
            if page_id == "sciencedirect":
                for page in pages[page_id]:
                    print(page)
                    page_content = requests.get(page).content
                    self.soup = BeautifulSoup(page_content, 'html.parser')   
                    content="<html><body>{0}</body></html>"
                    data_extracted = self.soup.find("div",attrs={"class","Abstracts"})
                    content = content.format(data_extracted)
                    # print(content,"\n\n")
                    self.save_as_csv(content, page,related)
                    self.art_abstracts.update({page:{"abstract":content}})
                    # abstracts.update({page:{"abstract":content}})  
                pass

            if page_id == "aerospaceamerica":
                for page in pages[page_id]:
                    # print(page)
                    page_content = requests.get(page).content
                    # ch = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                    # ch.get(page)
                    # page_content = ch.page_source
                    print(page_content)
                    self.soup = BeautifulSoup(page_content, 'html.parser')   
                    content="<html><body>{0}</body></html>"
                    data_extracted = self.soup.find("section")
                    # print(data_extracted)
                    content = content.format(data_extracted)
                    # print(content,"\n\n")
                    self.save_as_csv(content, page,related)
                    self.art_abstracts.update({page:{"abstract":content}})
                    # abstracts.update({page:{"abstract":content}}) 
                pass

                     
    def oa_art(self,pages, related):

        for page_id in pages:

            if page_id == "wiley":
                for page in pages[page_id]:
                    ch_wiley_oa = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                    ch_wiley_oa.get(page)
                    art_wiley_tit = ch_wiley_oa.find_elements_by_xpath('//div[@class="issue-item"]/a/h2')
                    oa_art_wiley = {}
                    for i in art_wiley_tit:
                        if i.text:
                            ele_dom_wiley = '//div[@class="issue-item"][a[h2[contains(text(),"{0}")]]]/div/ul/li[6]'.format(" ".join(i.text.split()[:2]))
                            if ch_wiley_oa.find_element(By.XPATH,ele_dom_wiley).text == "Request permissions":
                                oa_art_wiley.update({i.text:{"OA":"N"}})
                            else:
                                oa_art_wiley.update({i.text:{"OA":"Y"}})
                    self.save_as_csv(oa_art_wiley,page,related)
                    # print(oa_art_wiley)
                pass

            elif page_id == "jes":
                oa_art_jes = {}
                ch_jes_oa = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                for page in pages[page_id]:
                    ch_jes_oa.get(page)
                    page_d = {}
                    art_jes_cat = ch_jes_oa.find_elements(By.XPATH,'//h2/span')
                    for j in art_jes_cat:
                        art_jes_tit = ch_jes_oa.find_elements_by_xpath('//div[h2[span[text()="{0}"]]]/ul/li/div/h4'.format(j.text))
                        for i in art_jes_tit:
                            if i.text:
                                ele_dom_jes = '//div[h2[span[text()="{0}"]]]/ul/li[div[h4[contains(text(),"{1}")]]]//span[@class="cit-flags"]/span'.format(j.text," ".join(i.text.split()[:2]))
                                if ch_jes_oa.find_elements(By.XPATH,ele_dom_jes):
                                    page_d.update({i.text:{"OA":"Y","Article Type":j.text}})
                                else:
                                    page_d.update({i.text:{"OA":"N","Article Type":j.text}})
                    self.save_as_csv(page_d, page,related)
                    oa_art_jes.update({page:page_d})
                    # print(oa_art_jes)

                pass

            elif page_id == "sciencedirect":

                for page in pages[page_id]:
                    ch_sun_oa = webdriver.Chrome(executable_path="/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver")
                    ch_sun_oa.get(page)
                    art_sun_tit = ch_sun_oa.find_elements_by_xpath('//span[@class="js-article-title"]')
                    oa_art_sun = {}
                    for i in art_sun_tit:
                        if i.text:
                            ele_dom = '//dl[dt[h3[a[span[span[@class="js-article-title"][contains(text(),"{0}")]]]]]]/dd//span[@class="anchor-text"]'.format(" ".join(i.text.split()[:1]))
                            if ch_sun_oa.find_element(By.XPATH,ele_dom).text == "Download PDF":
                                oa_art_sun.update({i.text:{"OA":"Y"}})
                            else:
                                oa_art_sun.update({i.text:{"OA":"N"}})
                    self.save_as_csv(oa_art_sun, page,related)
                    # print(oa_art_sun)
                pass

        
        
                


if __name__ == "__main__":
    ArticleMetadata()
    # get_data()
