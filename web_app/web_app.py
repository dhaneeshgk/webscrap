from flask import Flask, render_template, request, make_response,redirect,url_for,send_file,flash,Markup
import os
import config
from imp import reload
import sys
sys.path.append(os.getcwd().replace("web_app",""))
from app import  Import_Web_To_WittyParrot
import time

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
    if 'auto_report_wp' in request.cookies:
        con = {"status":True}
        if con["status"]:
            return redirect(url_for("login"))
    return redirect("/login")

@app.route('/login',methods = ['GET'])
def login():
    return render_template("login.html")


@app.route('/webimport',methods=['GET','POST'])
def web_import():
    if request.method == "POST":
        # print(request.form)
        # url = request.form["url"]
        # identifiers = request.form["identifiers"]
        workspace = request.form["workspace"]
        facet_name = request.form["facet_name"]
        user_detail.update({"workspace":workspace,"model":facet_name})
        # print(url,identifiers,workspace,facet_name)
        im = Import_Web_To_WittyParrot(obj=flash,user_details=user_detail)
        # flash("Import started")
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
