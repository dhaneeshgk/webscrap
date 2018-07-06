from selenium import webdriver
from article_metadata import url_mo
from author_metadata import url_am
from issue_metadata import url_oa
import os
import json

def import_urls(name_g=None):
    if name_g == "ArticleMetadata":
        return json.loads(open(os.getcwd()+"/article_metadata.json","r").read())
    elif name_g == "AuthorMetadata":
        return json.loads(open(os.getcwd()+"/author_metadata.json","r").read())
    elif name_g == "IssueMetadata":
        return json.loads(open(os.getcwd()+"/issue_metadata.json","r").read())




if __name__ == "__main__":
    chrome_path = "/Users/dhaneesh.gk/Projects/own/web_import/extract_it/drivers/chromedriver"
    ch = webdriver.Chrome(executable_path=chrome_path)
    print("\n")
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print('''                   Welcome To POC of Web Import                    ''')
    print("\n\n")
    # input("Press enter to start\n\n")
    input("To start with Article Metadata Import Press enter\n")
    url_mo.ArticleMetadata(import_urls("ArticleMetadata"),driver=ch) 
    print("Completed with Article Metadata Import\n")
    # input("Press enter to start next web import\n\n")
    input("To start with Author Metadata Import Press enter\n")
    url_am.AuthorMetadata(import_urls("AuthorMetadata"),driver=ch)
    print("Completed with Author Metadata Import Press enter\n")
    # input("Press enter to start next web import\n\n")
    input("To start with Issues Metadata Import with details available related to article Press enter")
    url_oa.IssueMetadata(import_urls("IssueMetadata"))
    print("Completed with Issues Metadata Import\n")
    ch.quit()
