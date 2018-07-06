from flask import Flask, render_template, request, make_response,redirect,url_for,send_file,flash,Markup
import os
import config
from imp import reload
import sys
sys.path.append(os.getcwd().replace("web_app",""))
from app import  Import_Web_To_WittyParrot
import time
import shutil
FRAME_PATH = os.getcwd()

user_detail = {
        "user_id":"demo@lscms.wp",
        "password":"Welcome123",
        "env":"V3",
        "model":"",
        "workspace":"",
        "folders":["Courts","Court Opinions","Federal","United States Court of Appeals","United States Court of Appeals for 9th Circuit"],
        "url":"https://www.ca9.uscourts.gov/"
}

app = Flask(__name__)

app.secret_key = 'random string'

@app.route('/')
def index():
    return redirect("/login")

@app.route('/login',methods = ['GET'])
def login():
    return render_template("login.html")

@app.route('/login')
def re_login():
    return render_template("login.html",text="Invalid Credentials")


@app.route('/webimport',methods=['GET','POST','PUT'])
def web_import():
    if request.method == "POST":
        print(request.form)
        # url = request.form["url"]
        # identifiers = request.form["identifiers"]
        flash("Import started")
        workspace = request.form["workspace"]
        facet_name = request.form["facet_name"]
        user_detail.update({"workspace":workspace,"model":facet_name})
        # print(url,identifiers,workspace,facet_name)
        im = Import_Web_To_WittyParrot(obj=flash,user_details=user_detail)
        # time.sleep(2)
        im.check_models_present()
        im.extract_web_data()
        im.check_facets_presence()
        im.check_facet_values_presence()
        # flash("Import in middle")
        # time.sleep(2)
        im.check_folder_presense()
        im.check_wits_presence() 
        # flash("Import Completed")
        # if os.path.exists(user_f): os.unlink(user_f)
        dir_f = FRAME_PATH+'/wittyparrot_sdk/data_storage/'
        if os.path.exists(dir_f+"files"):shutil.rmtree(dir_f+"files")
        if os.path.exists(dir_f+"demo_attachments_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        if os.path.exists(dir_f+"demo_folder_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        if os.path.exists(dir_f+"demo_wits_status.json"):os.unlink(dir_f+"demo_attachments_status.json")
        return render_template('web_import.html')
    else:
        return render_template('web_import.html')


@app.route('/web_import_status',methods=['GET','POST'])
def web_import_status():
    im = Import_Web_To_WittyParrot(obj=flash)
    im.check_models_present()
    im.extract_web_data()
    im.check_facets_presence()
    im.check_facet_values_presence()
    im.check_folder_presense()
    im.check_wits_presence()
    return render_template('web_import_status.html')

@app.route("/login",methods=['POST'])
def logout():
    if 'auto_report_wp' in request.cookies:
        con = {"status":True}
        if con["status"]:
            return render_template('login.html',text=con["remarks"])
        else:
            return render_template('login.html',text=con["remarks"])


if __name__=="__main__":
    pass
