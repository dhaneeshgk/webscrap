import requests
import json

url = "https://wittyapi.wittyparrot.com"
headers = {"Content-Type":"application/json"}


def login(email_=None,password_=None):
    r_url = '/wittyparrot/api/auth/login'
    data = {"userId":email_,"password":password_}
    res = requests.post(url=url+r_url,headers=headers,data=json.dumps(data))
    if res.status_code==200:
        res_j = json.loads(res.content.decode('utf-8'))
        return {'Authorization':res_j["accessToken"]["tokenType"]+" "+res_j["accessToken"]["tokenValue"]}
    else:
        return {}

def validate_auth(access_token=None):
    res = requests.post(url=url+"validate_auth",headers=headers,
    data = json.dumps({"access_token":access_token}))
    con = res.content.decode('utf-8')
    return json.loads(con)

def logout(access_token=None):
    res = requests.post(url=url+"logout",headers=headers,
    data = json.dumps({"access_token":access_token}))
    con = res.content.decode('utf-8')
    return json.loads(con)



if __name__=="__main__":
    # print(login("aab@aa.com","welcome123"))
    pass
