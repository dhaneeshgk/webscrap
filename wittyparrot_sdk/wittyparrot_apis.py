'''
Created on 01-Sep-2017

@author: dhaneeshgk
'''
from config import *
from wittyparrot_sdk import envs
from imp import reload
import requests
import json
import os
FRAME_PATH = os.getcwd().replace("/web_app","")
import shutil
# print(FRAME_PATH)


class  WittyParrot_Apis:
    
    def __init__(self,details=None,env=None,username='dgk.wittyparrot@outlook.com',password='Welcome123',Authorization=None):
        if not details:
            self.env = env
            self.userId = username
            self.password = password
        else:
            self.env = details['environment']
            self.userId = details['userId']
            self.password = details['password']       
                
        self.Authorization = {'Authorization':None}
        self.enterpriseId = None
        self.login_response = None
        self.uploaded_images = {}
        self.uploaded_attachments = {}
                    
        self.user_path = FRAME_PATH+'/wittyparrot_sdk/data_storage/dbs/{0}'.format(self.userId)
        self.frame_path = FRAME_PATH+'/wittyparrot_sdk/data_storage/'

        dir_f = FRAME_PATH+'/wittyparrot_sdk/data_storage/'
        if os.path.exists(dir_f+"files"):shutil.rmtree(dir_f+"files")
        if os.path.exists(dir_f+"demo_attachments_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        if os.path.exists(dir_f+"demo_folder_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        if os.path.exists(dir_f+"demo_wits_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        
        self.wits = []
        self.workspaces = {}
        
        self.url()
        

        for i in [self.user_path,self.user_path+"/docs",self.user_path+"/images"]:
            if not os.path.exists(i):
                os.makedirs(i)
                
        
        if not Authorization:
            
#             print(self.login())
            if not self.login():
                print("Error with login credentials")
#                 raise "Error with login credentials"
            
            self.enterpriseId = self.login_response['userProfile']['enterpriseId']
        
        else:
            
            if not self.validate_user_auth(Authorization):
                raise "Error Validaing user authentication"
            
            self.enterpriseId = self.login_response['userProfile']['enterpriseId']
        
        

    def url(self):
        
        reload(envs)
        if self.env in envs.envs:
            self.Url = envs.envs[self.env]
        else:
            self.Url = 'https://qawittyapi.wittyparrot.com'
            
    def login(self):
        
        r_url = '/wittyparrot/api/auth/login'
        
        headers = {'Content-Type':'application/json'}
        
        data = {"userId":self.userId,"password":self.password}
        
        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))
        
        if res.status_code==200:
        
            res_j = json.loads(res.content.decode('utf-8'))
            
            self.Authorization.update({'Authorization':res_j["accessToken"]["tokenType"]+" "+res_j["accessToken"]["tokenValue"]})
            
            self.login_response = res_j
            
            return res_j
        
        else:
#             print(res.content)
            return False
        
        
    def create_user(self,Authorization=None):
        
        r_url = '/wittyparrot/api/admin/users'
        
        headers = {'Content-Type':'application/json'}
        
        
        if Authorization:
            headers.update({"Authorization":Authorization})
        else:
            headers.update({"Authorization":self.Authorization['Authorization']})
        
        res = requests.post(url=self.Url+r_url,headers=headers)
        
        if res.status_code==200:
        
            res_j = json.loads(res.content.decode('utf-8'))
            
            self.Authorization.update({'Authorization':Authorization})
            
            self.login_response = res_j
            
            return res_j
        
        else:
            
            return False
            
        
    def validate_user_auth(self,Authorization=None):
        
        r_url = '/wittyparrot/api/auth/user'
        
        headers = {'Content-Type':'application/json'}
        
        if Authorization:
            headers.update({"Authorization":Authorization})
        else:
            headers.update({"Authorization":self.Authorization['Authorization']})
        
        res = requests.get(url=self.Url+r_url,headers=headers)
        
        if res.status_code==200:
        
            res_j = json.loads(res.content.decode('utf-8'))
            
            self.Authorization.update({'Authorization':Authorization})
            
            self.login_response = res_j
            
            return res_j
        
        else:
            
            return False
    
    def upload_image(self,file_path=None,file_type=None):
        
        r_url = '/wittyparrot/api/attachments/inlineImage'
        
        
        
        filename = file_path.split("/")[-1]
        
#         if file_type: f_type=file_type
#         else: f_type = 'image/{0}'.format(filename.split(".")[-1])
        f_type = 'image/*'
        
#         print(filename,f_type)
        
        res = requests.post(url=self.Url+r_url,headers=self.Authorization,
                            files={"file":(filename,open(file_path,"rb"),f_type)})
        
        res_j = json.loads(res.content.decode('utf-8'))
        
#         print(res_j)
        self.uploaded_images.update({res_j['fileId']:res_j})
        
        return res_j
    
    def create_pptx_wit_xml(self,file_path=None,file_type=None,parentId="ef88801c-ce64-4ff2-b5d5-02769726cbeb"):
        
        r_url = '/wittyparrot/api/wits/pptwit/{0}'.format(parentId)
        
        filename = file_path.split("/")[-1]
        
#         if file_type: f_type=file_type
#         else: f_type = 'image/{0}'.format(filename.split(".")[-1])
        if not file_type:
            f_type = 'xml/*'
        else:
            f_type = "xml"
            
        
#         print(filename,f_type)
        
        res = requests.post(url=self.Url+r_url,headers=self.Authorization,
                            files={"file":(filename,open(file_path,"rb"),f_type)})
        
        res_j = json.loads(res.content.decode('utf-8'))
        
        print(res_j)
        
        
    def generate_pptx_doc_xml(self,file_path=None,file_type=None):
        
        r_url = '/wittyparrot/api/attachments/convertxmltoppt'
        
        filename = file_path.split("/")[-1]
        
#         if file_type: f_type=file_type
#         else: f_type = 'image/{0}'.format(filename.split(".")[-1])
        if not file_type:
            f_type = 'xml/*'
        else:
            f_type = "xml"
            
        
#         print(filename,f_type)
        
        res = requests.post(url=self.Url+r_url,headers=self.Authorization,
                            files={"file":(filename,open(file_path,"rb"),f_type)})
        
        con_j = res.content
        print(con_j)
        
        pp = open(file_path.split(".")[0]+".pptx","wb")
        pp.write(con_j)
        pp.close()
        
        
    
    def create_tags(self,tag_names=None):
        
        r_url = '/wittyparrot/api/tags'

        tags = {}
        
        for i in tag_names:
            res = requests.post(url=self.Url+r_url,data=json.dumps({"name":i}))
    
            tags.update({tag_names.index(i):json.loads(res.content)})
            
        return tags
    
    def tag_info(self,tag_names=None):
        
        r_url = '/wittyparrot/api/tags/search'
        
        tags = {}
        
        res = requests.get(self.Url+r_url)
        
        if res.status_code==200:
            for i in tag_names:
                pass
            
        
    
    def download_image(self,file_info=None):
        
        r_url = ''
        
        res = requests.get(url=self.Url+r_url.format())
  
        f = open(self.user_path+'/images/{0}'.format(file_info['fileName']),'wb')
        f.write(res.content)
        f.close()      
        
        return {file_info['fileId']:None,file_info['fileAssociationId']:None,"name":file_info['fileName'],
                'file_path':self.user_path+'/images/{0}'.format(file_info['fileName'])} 
        
        
    def upload_doc(self,file_path=None):
        
        r_url = '/wittyparrot/api/attachments'
        
#         file_path = self.frame_path+"/"
#         
        filename = file_path.split("/")[-1]
        
        res = requests.post(url=self.Url+r_url,headers=self.Authorization,
                            files={"file":(filename,open(file_path,"rb"),'multipart/form-data')})
        
        res_j = json.loads(res.content.decode('utf-8'))
        
#         print(res_j)
        
        self.uploaded_attachments.update({res_j['fileId']:res_j})
        
        return res_j
    
    def download_doc(self,file_info=None):
        
        r_url = '/wittyparrot/api/attachments/associationId/{file_asscoiation_id}'.format(file_asscoiation_id=file_info['fileAssociationId'])

        res = requests.get(url=self.Url+r_url,headers=self.Authorization)     
        
        f = open(self.user_path+'/docs/{0}'.format(file_info['fileName']),'wb')
        f.write(res.content)
        f.close()
        
        return {file_info['fileId']:None,file_info['fileAssociationId']:None,"name":file_info['fileName'],
                'file_path':self.user_path+'/docs/{0}'.format(file_info['fileName'])}
    
    
    def create_wit(self,wit_title="Default Title",content=None,parent_id=None,attach=None,acronyms=None,categories=None,tags=None,all_d=None,res_time=False):
        
        r_url = '/wittyparrot/api/wits'
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})
        
        
        
        if not all_d:
        
            d_m_t = json.loads(open(self.frame_path +'apis_json/create_wit/create_wit.json','rb').read().decode('utf-8'))
              
            d_m_t.update({'name':wit_title})
              
            if content:d_m_t.update({'content':content})
              
            d_m_t.update({'parentId':parent_id})
       
            if attach:
                attachments = []
                d_f_t = json.loads(open(self.frame_path +'apis_json/create_wit/attachmentDetails.json','r').read())
                for i in attach:
                    d_f_t.update(i)
                attachments.append(d_f_t)
                d_m_t.update({'attachmentDetails':attachments})
                      
                  
            if acronyms:
                acronyms = []
                d_a_t = open(self.frame_path +'apis_json/create_wit/acronyms.json','r').read()
                for i in acronyms:
                    d_a_t.update(i)
                acronyms.append(d_a_t)
                d_m_t.update({'acronyms':acronyms})
                
            if tags:
                tags = []
                d_a_t = open(self.frame_path +'apis_json/create_wit/tags.json','r').read()
                for i in tags:
                    d_a_t.update(i)
                acronyms.append(d_a_t)
                d_m_t.update({'acronyms':acronyms})

            if categories:
                d_m_t.update({"categoryValues": []})
                            
            data = d_m_t
            
        else:
            data = all_d
        
        data.update({'enterpriseId':self.enterpriseId})
#         print(json.dumps(data))
        
#         print(data)
        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))
#         print(res.__dict__)
#         print(res.status_code)
        if res.status_code==201:
            if res_time:
                return res.elapsed,json.loads(res.content.decode('utf-8'))
            return json.loads(res.content.decode('utf-8'))
        else:
            print(res.content)
            raise "error while creating wit"
            return False
#             raise False
#         return {'title':wit_title}
    
    
    def list_folders(self,level=0):
        
        r_url = '/wittyparrot/api/folders/workspaceId/{workspaceid}/level/{level}'
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})      
        
        for i in self.login_response["userProfile"]["userWorkspaces"]:
            res= requests.get(url=self.Url+r_url.format(workspaceid=i['id'],level=str(level)),headers=headers)
            
#             print(res.status_code)
            if res.status_code == 200:
                con = json.loads(res.content.decode('utf-8'))
                if not i['name'] in self.workspaces:
                    self.workspaces.update({i['name']:{'id':i['id']}})
                self.workspaces[i['name']].update({level:con})
            else:
                print("Error While getting folders list")
#                 raise "Error While getting folders list"
        return self.workspaces
            
            
    def list_child_folders(self,folder_id=None):
        
        r_url = '/wittyparrot/api/folders/{folder_id}/pathhierarchy'
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})      
        
        res= requests.get(url=self.Url+r_url.format(folder_id=folder_id),headers=headers)
            
        # print()
        if res.status_code == 200:
            con = json.loads(res.content.decode('utf-8'))
            return con
        else:
            print(res.content.decode('utf-8'))
            print("Error While getting folders list")
            return []
#                 raise "Error While getting folders list"      
            
    def create_folder(self,workspaceId=None,name=None,parentId=None):
        
        r_url = '/wittyparrot/api/folders'
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'}) 
          
#         print(os.path.exists(self.frame_path +'api_json/create_folder/create_folder.json'))
#         data = json.loads(open(self.frame_path +'apis_json/create_folder/create_folder.json','r').read())
        data = {"enterpriseId":"{enterpriseId}","workspaceId":"{workspaceId}","name":"{name}","parentId":None}

        data.update({'workspaceId':workspaceId,'name':name})
        
        if parentId: data.update({'parentId':parentId})
        data.update({'enterpriseId':self.enterpriseId})
        
#         print(data)
        
        res = requests.post(url=self.Url+r_url,data=json.dumps(data),headers=headers)
#         print(res.status_code)
        if res.status_code == 201:
            return json.loads(res.content.decode('utf-8'))
        else:
            print(res.content)
            raise "Error While creating folder"
        
        
    def list_wits(self,folder_id=None):
        
        r_url = '/wittyparrot/api/wits/folder/{folder_id}/childids?asc=false'.format(folder_id=folder_id)
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'}) 
        
        res = requests.get(url=self.Url+r_url,headers=headers)
        
#         print(res.status_code)
        if not res.status_code == 200:
            raise "error in list wits"
        else:
            return json.loads(res.content.decode('utf-8'))
        
        
    def list_wits_info(self,folder_id=None):
        
        r_url = '/wittyparrot/api/wits/listbyids'.format(folder_id=folder_id)
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'}) 
        
        data = [folder_id]
        
        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))
        
#         print(res.status_code)
        if not res.status_code == 200:
            print(res.content)
            raise "error in list wits info"
        else:
            return json.loads(res.content.decode('utf-8'))
    
    def wit_info(self,wit_id=None):
        
        r_url = '/wittyparrot/api/wits/{wit_id}'.format(wit_id=wit_id)
        
        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'}) 
        
        res = requests.get(url=self.Url+r_url,headers=headers)
        
#         print(res.status_code)
        if not res.status_code == 200:
#             print(res.content)
            raise "error in wit_info"
        else:
            return json.loads(res.content.decode('utf-8'))     
   
   
    def list_facets(self,Id=None):
        
        if not Id:
            r_url = '/wittyparrot/api/categories/{id}'.format(id=self.enterpriseId)
        else:
            r_url = '/wittyparrot/api/categories/{id}'.format(id=Id)

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})    
        
        res = requests.get(url=self.Url+r_url,headers=headers)
        
#         print(res.status_code)
        if not res.status_code == 200:
#             print(res.content)
            raise "error in list_facets"
        else:
            return json.loads(res.content.decode('utf-8'))  
        
    
    def create_facet(self,name=None,parentId=None,many=None):
        
        r_url = '/wittyparrot/api/categories'
        
        data = {"name":name,"parentId":parentId}
        # data = {"name":name,"groupId":parentId}

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})         

        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))
        
#         print(res.status_code)
        if not res.status_code == 201:
            print(res.content)
            # raise "error in create facet"
        else:
            return json.loads(res.content.decode('utf-8'))          
             
             
    def create_facet_value(self,name=None,parentId=None):
 
        r_url = '/wittyparrot/api/categories/values'
        
        # data = {"name":name,"parentId":parentId}
        data = {"name":name,"groupId":parentId}

        # print(data)

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})         

        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))
        
#         print(res.status_code)
        if not res.status_code == 201:
            print(res.content)
            # raise "error in create facet value"
        else:
            return json.loads(res.content.decode('utf-8'))       

    def get_facet_values(self,Id=None,values="true"):

        r_url = '/wittyparrot/api/categories/{id}?values={values}'.format(id=Id,values=values)

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})         

        res = requests.get(url=self.Url+r_url,headers=headers)
        
        # print(res.status_code)
        if not res.status_code == 200:
            print(res.content)
            raise "error in getting facet values"
        else:
            return json.loads(res.content.decode('utf-8'))   


    def list_models(self,level=1,values="false"):

        r_url = '/wittyparrot/api/categories/hierarchy?level={level}&values={values}'.format(level=str(level),values=values)  

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})         

        res = requests.get(url=self.Url+r_url,headers=headers)
        
#         print(res.status_code)
        if not res.status_code == 200:
#             print(res.content)
            raise "error in getting models list"
        else:
            return json.loads(res.content.decode('utf-8'))         
   
    def create_tag(self,name=None):
        
        r_url = '/wittyparrot/api/tags'

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'}) 
        
        data = {"name":name}        
        
        res = requests.post(url=self.Url+r_url,headers=headers,data=json.dumps(data))   
        
        if res.status_code == 201:
            return json.loads(res.content.decode('utf-8'))
        else:
            raise "Error while creating tag"
        
        
    def rename_tag(self,tag_info=None,new_name=None):
        
        r_url = '/wittyparrot/api/tags'

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})         
        
        data = {"name":new_name,"id":tag_info['id']} 
        res = requests.put(url=self.Url+r_url,headers=headers,data=json.dumps(data))     
        
        if res.status_code == 200:
            return json.loads(res.content.decode('utf-8'))
        else:
            raise "Error while renaming tag"         
        
    def delete_tag(self,tag_infos=None):
        
        r_url = '/wittyparrot/api/tags'

        headers = self.Authorization.copy()
        headers.update({'Content-Type':'application/json'})    
        
        data = [i['id'] for i in tag_infos]
        
        res = requests.delete(url=self.Url+r_url,headers=headers,data=json.dumps(data))
        
        if res.status_code == 200:
            return json.loads(res.content.decode('utf-8'))
        else:
            raise "Error while delete tag"          
        
if __name__ == '__main__':
    wp = WittyParrot_Apis(env='V2',username="testws1@yopmail.com",password="welcome123")
#     wp.create_pptx_wit_xml(file_path="/Users/dhaneeshgk/Downloads/alignment.xlsx", file_type="xlsx")
    wp.generate_pptx_doc_xml(file_path="/Users/dhaneeshgk/Downloads/sample.xml")
    
#     wp = WittyParrot_Apis('V3',username="dhaneesh@wittyparrot.com",password="welcome123")
# #     print(wp.upload_image('/Users/dhaneeshgk/Downloads/TeddyDay.jpg'))
# #     print(wp.upload_doc('/Users/dhaneeshgk/Downloads/DAILY_SMOKE_TEST_SUITE.xlsx'))
# #     print(wp.login_response['userProfile']['enterpriseId'])
#     folders = wp.list_folders()
#     for j in folders.values():
#         folder_ids = [i['id'] for i in j[0]]
#         print(folder_ids)
#         for i in folder_ids:
# #             wit_list_info = wp.list_wits_info(folder_id=i)
# #             print(wit_list_info)
# #             wit_ids = [(i['id'],i['type']) for i in wit_list_info]
#             wits = wp.list_wits(i)
#             wit_infos =[]
#             for wit in wits:
#                 wit_info = wp.wit_info(wit)
#                 wit_infos.append(wit_info)
# #                 print(wit_info)
#                 print(wit_info['name'])
#                 print(wit_info['inlineImageDetails'])
#             print([x for x in wit_infos if x['witType']=='ORDINARY_WIT'])
#     wp.download_doc(file_info=wit_info['attachmentDetails'][0])

#     ds = open('/Users/dhaneeshgk/git/V2_WebApp/miscellaneous/wittyparrot_apis/apis_json/create_folder/create_folder.json','rb').read()
#     print(ds.decode('utf-8'))
#     data = json.loads(str(ds))
    
    