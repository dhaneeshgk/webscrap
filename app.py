
from config import *
from extract_it.pages.extract_opinions_page import Extract_Opinions_Page
from extract_it.pages.extract_memoranda_page import Extract_Memoranda_Page
from extract_it.pages.extract_usc9_page import Extract_USC9_Page
from wittyparrot_sdk.wittyparrot_apis import WittyParrot_Apis
import user_details as yu
from imp import reload
import json
import os
import requests
import time


class Import_Web_To_WittyParrot:

    def __init__(self, url=""):
        self.user = WittyParrot_Apis(username=yu.user["user_id"],password=yu.user["password"],env=yu.user["env"])
        self.folders = [i.upper() for i in yu.user['url'].split("/")[2].split(".") if not i in ["www"]]
        self.folders.reverse()
        self.case_details = {}
        self.model = {}
        self.folder_s_p = FRAME_PATH+"/wittyparrot_sdk/data_storage/"+yu.user["user_id"].split("@")[0]+"_folder_status.json"
        self.wits_s_p = FRAME_PATH+"/wittyparrot_sdk/data_storage/"+yu.user["user_id"].split("@")[0]+"_wits_status.json"
        self.attachments_s_p = FRAME_PATH+"/wittyparrot_sdk/data_storage/"+yu.user["user_id"].split("@")[0]+"_attachments_status.json"
        self.attach_f_p = FRAME_PATH+"/wittyparrot_sdk/data_storage/files/"

    def re_do(self):
        reload(yu)
        self.user = WittyParrot_Apis(username=yu.user["user_id"],password=yu.user["password"],env=yu.user["env"])
        self.folders = [i.upper() for i in yu.user['url'].split("/")[2].split(".") if not i in ["www"]]
        self.folders.reverse()
        self.case_details = {}

    def check_models_present(self):
        print("started for models presence check")
        models = {model["name"]:model["id"] for model in self.user.list_models()}
        if not yu.user["model"] in models:
            print("error for models presence check")
            return {"status":False, "message":"Model {0} Not exists please create and move forward".format(yu.user["model"])}
        else:
            self.model.update({"name":yu.user["model"],"id":models[yu.user["model"]]})
            print("completed for models presence check")
            return {"status":True}

    def extract_web_data(self):
        print("started for extract_web_data of main")
        op_types = Extract_USC9_Page(yu.user["url"]).get_opinion_types()
        print("completed for extract_web_data main")
        for i in op_types:
            print("started for extract_web_data of '{0}'".format(i))
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
            print("completed for extract_web_data of '{0}'".format(i))
        return self.case_details

    def check_facets_presence(self):
        print("started check for facets presence")
        # print(self.case_details["Published"]["case_details"][0].keys())
        # print(self.case_details["Unpublished"]["case_details"][0].keys())
        # self.model.update({"childs":{"Case Origin":{},"Case Type":{},"Authoring Judge":{},"Case Panel":{}}})
        self.model.update({"childs":{"Case Origin":{},"Case Type":{}}})
        for i in self.model["childs"]:
            # print(i)
            c_l = self.user.get_facet_values(Id=self.model["id"])
            if "subGroups" in c_l:
                ml_c = {j["name"]:j for j in c_l["subGroups"]}
                if not i in ml_c:
                    details = self.user.create_facet(name=i,parentId=self.model["id"])
                    self.model["childs"][i].update({"name":i,"id":details["id"],"details":details,"childs":{}})
                else:
                    self.model["childs"][i].update({"name":i,"id":ml_c[i]["id"],"details":ml_c[i],"childs":{}})
            else:
                details = self.user.create_facet(name=i,parentId=self.model["id"])
                self.model["childs"][i].update({"name":i,"id":details["id"],"details":details,"childs":{}})  
        print("completed check for facets presence")
        return self.model


    def check_facet_values_presence(self):
        print("started check for facet_values_presence")
        case_details = []
        for i in self.case_details:
            case_details.extend(self.case_details[i]["case_details"])
        for i in case_details:
            for j in i:
                if j in self.model["childs"]:
                    if i[j]:
                        if i[j].strip():
                            facet_vals = self.user.get_facet_values(Id=self.model["childs"][j]["id"])
                            # print("facet_vals",facet_vals)
                            if facet_vals["hasChildren"]:
                                facet_l_val = {tag_d["name"]:{"id":tag_d["id"],"details":tag_d} for tag_d in facet_vals['tags']}
                                # print(facet_l_val.keys())
                                if not i[j] in facet_l_val:
                                    val = self.user.create_facet_value(name=i[j], parentId=self.model["childs"][j]["id"])
                                    self.model["childs"][j]["childs"].update({i[j]:{"id":val["id"],"details":val}})
                                else:
                                    self.model["childs"][j]["childs"].update({i[j]:facet_l_val[i[j]]})
                            else:
                                val = self.user.create_facet_value(name=i[j], parentId=self.model["childs"][j]["id"])
                                self.model["childs"][j]["childs"].update({i[j]:{"id":val["id"],"details":val}})  
        print("completed check for facet_values_presence")
        return self.model                               

    def check_folder_presense(self):
        print("started check for folder_presense")
        workspaces = {i["name"]:i["id"] for i in self.user.login_response["userProfile"]["userWorkspaces"]}
        f_st = self.status(folders=True,read=True)
        if not yu.user["folders"][0] in f_st:
            r_f = self.user.create_folder(workspaceId=workspaces[yu.user['workspace']],name=yu.user["folders"][0])
            self.folder_c = {r_f['name']:r_f["id"]}
            self.status(folders=self.folder_c)
        else:
            self.folder_c = {yu.user["folders"][0]:f_st[yu.user["folders"][0]]}

        count = 1
        for i in yu.user["folders"][1:]:
            if not i in f_st:
                f_l = self.user.create_folder(workspaceId=workspaces[yu.user['workspace']],name=i,parentId=self.folder_c[yu.user["folders"][count-1]])
                count = count+1
                self.folder_c.update({f_l["name"]:f_l["id"]})
                self.status(folders=self.folder_c)
            else:
                self.folder_c.update({i:f_st[i]})
        for i in self.case_details:
            if not i in f_st:
                j_l = self.user.create_folder(workspaceId=workspaces[yu.user['workspace']],name=i,parentId=self.folder_c[yu.user["folders"][-1]])
                self.folder_c.update({j_l["name"]:j_l["id"]})
                self.status(folders=self.folder_c)
            else:
                self.folder_c.update({i:f_st[i]})            
        print("completed check for folder_presense")

    def check_wits_presence(self):

        for i in self.case_details:
            print('Started creation of wit for "{0}"'.format(i))
            w_c_s = self.status(wits=True,read=True)
            for j in self.case_details[i]["case_details"]:

                if not "NO OPINIONS FILED TODAY" == j['Case Title']:
                    if not j['Case No.']+"--"+j['Case Title'] in w_c_s:
                        print('Started creation of wit for case "{0}"'.format(j['Case No.']+"--"+j['Case Title']))
                        content = ""
                        c_j = json.loads(open(FRAME_PATH+"/wittyparrot_sdk/apis_json/create_wit.json","r").read())
                        # print(c_j)

                        c_j["parentId"] = self.status(folders=True,read=True)[i]

                        c_j['name'] = j['Case No.']+"--"+j['Case Title']

                        for p in j:
                            if not p in ["document"]:
                                content = content +"<div>"+ p +" : "+str(j[p])+"</div>"
                        content = content.strip()+"<div>Details are in the attachment with Case No.</div>"
                        c_j['content'] = content
                        c_j['desc'] = content

                        if j["document"].find("http")<0:
                            f_url = "http:"+j["document"]
                        else:
                            f_url = j["document"]
                        at_res = requests.get(f_url)
                        con = at_res.content
                        f = open(self.attach_f_p+j["Case No."]+".pdf","wb")
                        f.write(con)
                        f.close()
                        at_st = self.status(attachments=True,read=True)
                        if not j["Case No."] in at_st:
                            attach_l = self.user.upload_doc(self.attach_f_p+j["Case No."]+".pdf")
                            self.status(attachments={j["Case No."]:attach_l})
                            c_j['attachmentDetails'].append({"fileId":attach_l["fileId"],
                            "fileName":attach_l["fileName"], "extention":".pdf","attachmentType": "LOCAL",
                            "seqNumber": 0})
                        else:
                            c_j['attachmentDetails'].append(at_st[j["Case No."]])
                            c_j['attachmentDetails'].append({"fileId":at_st[j["Case No."]]["fileId"],
                            "fileName":at_st[j["Case No."]], "extention":".pdf","attachmentType": "LOCAL",
                            "seqNumber": 0})
                        
                        for x in self.model['childs'].keys():
                            if x in j:
                                # print(self.model['childs'][i], j[i])
                                # if j[x] and self.model['childs'][x]["childs"] and self.model['childs'][x]["childs"][j[x]]:
                                c_j['categoryValues'].append(self.model['childs'][x]["childs"][j[x]]["details"])
                        # print(c_j)
                        w_c = self.user.create_wit(all_d=c_j)
                        self.status(wits={w_c["name"]:w_c["id"]})
                        print('Completed creation of wit for case "{0}"'.format(j['Case No.']+"--"+j['Case Title']))
                        time.sleep(5)
            print('Completed creation of wit for "{0}"'.format(i))

    def status(self,folders=None,wits=None,attachments=None,read=False):

        if folders:

            if os.path.exists(self.folder_s_p):
                f_s = json.loads(open(self.folder_s_p,"r").read())
            else:
                f_s = {}
            if read:
                if not f_s:
                    f_s_f = open(self.folder_s_p,"w")
                    f_s_f.write(json.dumps(f_s))
                    f_s_f.close()
                return f_s
            f_s.update(folders)
            f_s_f = open(self.folder_s_p,"w")
            f_s_f.write(json.dumps(f_s))
            f_s_f.close()
        elif wits:
            if os.path.exists(self.wits_s_p):
                f_s = json.loads(open(self.wits_s_p,"r").read())
            else:
                f_s = {}
            if read:
                if not f_s:
                    f_s_f = open(self.wits_s_p,"w")
                    f_s_f.write(json.dumps(f_s))
                    f_s_f.close()
                return f_s
            f_s.update(wits)
            f_s_f = open(self.wits_s_p,"w")
            f_s_f.write(json.dumps(f_s))
            f_s_f.close()
        elif attachments:
            if os.path.exists(self.attachments_s_p):
                f_s = json.loads(open(self.attachments_s_p,"r").read())
            else:
                f_s = {}
            if read:
                if not f_s:
                    f_s_f = open(self.attachments_s_p,"w")
                    f_s_f.write(json.dumps(f_s))
                    f_s_f.close()
                return f_s
            f_s.update(attachments)
            f_s_f = open(self.attachments_s_p,"w")
            f_s_f.write(json.dumps(f_s))
            f_s_f.close()

            
            






if __name__ == "__main__":
    cd = Import_Web_To_WittyParrot()
    cd.check_models_present()
    cd.extract_web_data()
    cd.check_facets_presence()
    cd.check_facet_values_presence()
    cd.check_folder_presense()
    cd.check_wits_presence()
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





    

