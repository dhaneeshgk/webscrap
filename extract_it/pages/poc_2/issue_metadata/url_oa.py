import requests
from bs4 import BeautifulSoup
# import config_oa
import os

class IssueMetadata:

    def __init__(self, pages=None):
        if not pages:pages = config_oa.pages
        cwd = os.getcwd().split("extract_it")[0]+"extracted_data/"
        self.store_extract = cwd+"Info_P/IssueMetadata/"
        print("\nYou can find the extracted contents at below location\n{0}\n\n".format(self.store_extract))
        if not os.path.exists(self.store_extract):
            os.mkdir(self.store_extract)
        self.data = {}
        self.to_csv = {}
        for i in pages:
            self.page = pages[i]
            page_content = requests.get(self.page).content
            self.soup = BeautifulSoup(page_content, 'html.parser')
            if i == "wiley": self.data.update({i:self.wiley(self.page,"wiley")})
            if i =="jstage": self.data.update({i:self.jstage(self.page,"jstage")})

    def save_as_csv(self,objects,page,related=None):
        store_path = ""
        tsv = False
        if related == "wiley":
            con = "article\tAuthors\tOA\tPublished History\tAbstract\tFull text\tPDF\tReferences\n"
            for i in objects:
                con = con + i["article"]+"\t"
                authors = ""
                for j in i["Authors"]:
                    authors  = authors + " ".join(list(j.values())) + ","
                con = con + authors[:-1]+"\t"
                con = con + i["OA"] +"\t"
                con = con + list(i["Published History"].keys())[0]+list(i["Published History"].values())[0]+ "\t"
                con = con + i['MoreInfo']['Abstract'] +"\t"+i['MoreInfo']['Full text'] +"\t"+i['MoreInfo']['PDF'] +"\t"+i['MoreInfo']['References'] +"\n"

            if not os.path.exists(self.store_extract+related):os.mkdir(self.store_extract+related)
            # print(page)
            store_path = self.store_extract+related+"/"+page.split("//")[1].split("/")[0].replace(".","_")

            tsv = True        

        if related == "jstage":
            con = ""
            con = "title\tAuthors\tOA\tabstract\tPDF\tMore Info\n"
            for i in objects:
                con = con + i["title"]+"\t"
                authors = ""
                for j in i["authors"]:
                    authors  = authors + " ".join(list(j.values())) + ","
                con = con + authors[:-1]+"\t"
                con = con + i["OA"] +"\t"
                con = con + i["abstract"] +"\t"
                con = con + i["PDF"] + "\t"
                con = con + " ".join(i["MoreInfo"]) +"\n"

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
    
        print("\nFor link  :: "+page+"\n")

    def wiley(self, page, related):
        lists = self.soup.findAll('div',attrs={"class":"issue-item"})
        data = []
        for i in lists:
            data_extracted = {"OA":"N"}
            data_extracted.update({"article":i.find("h2").text.strip().replace("    ","").replace("\n","")})
            data_extracted.update({"Authors":[{"First Name":j.text.split(" ")[0],"Last Name":j.text.split(" ")[1]} for j in i.find("ul",attrs={"class":"loa-authors-trunc"}).findAll("span")]})
            data_extracted.update({"Published History":{i.find("li", attrs={"class", "ePubDate"}).findAll("span")[0].text:i.find("li", attrs={"class", "ePubDate"}).findAll("span")[1].text}})
            data_extracted.update({"MoreInfo":{j.attrs["title"]:"https://onlinelibrary.wiley.com"+j.attrs["href"] for j in i.find("div", attrs={"class", "content-item-format-links"}).findAll("a") if "title" in j.attrs and "href" in j.attrs}})
            data.append(data_extracted)
        self.save_as_csv(data, page, related)
        return data

    def jstage(self, page, related):
        lists = self.soup.find('ul',attrs={"class":"search-resultslisting"}).findAll("li")
        data = []
        for i in lists:
            # print(i)
            data_extracted = {}
            if i.find("div",attrs={"class","searchlist-title"}).find("a"):
                title = {"title":i.find("div",attrs={"class","searchlist-title"}).find("a").attrs["title"]} 
            # print("title", title)
            data_extracted.update(title)
            authors = [{"First Name":j.split(" ")[0], "Last Name":j.split(" ")[1]}for j in i.find("div",attrs={"class","searchlist-authortags customTooltip"}).text.split(",")]
            data_extracted.update({"authors":authors})
            # print("authors",authors)
            if i.find("div", attrs={"class","inner-content abstract"}):abstract = {"abstract":i.find("div", attrs={"class","inner-content abstract"}).text.strip().split("\n")[0]}
            data_extracted.update(abstract)
            # print("abstract", abstract)
            tags = {j.attrs["title"]:j.text for j in i.find("div", attrs={"class","global-tags"}).findAll("span")}
            if "FREE ACCESS" in tags:
                tags = {"OA":"Y"}
            data_extracted.update(tags)
            # print("tags", tags)
            pdf_link = {"PDF":a.attrs["href"] for a in i.findAll("a") if a.text.find("Download PDF")>=0}
            data_extracted.update(pdf_link)
            # print("pdf_link",pdf_link)
            if i.find("div",attrs={"class","searchlist-additional-info"}):
                more_info = [j.strip()  for j in i.find("div",attrs={"class","searchlist-additional-info"}).text.strip().split("\n")]
                data_extracted.update({"MoreInfo":more_info})
                # print("more_info",more_info)
            data.append(data_extracted)
            # break
        self.save_as_csv(data, page, related)
        return data

    def get_data(self):
        return self.data

if __name__ == "__main__":
    dd = IssueMetadata()
    # data = dd.get_data()

    # print(data)
    # for i in data:
    #     for j in data[i]:
    #         for q in j:
    #             print(q, j[q])
    #             print("\n")
    #     print("Done\n\n\n")