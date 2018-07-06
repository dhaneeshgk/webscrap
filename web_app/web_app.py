from flask import Flask, render_template, request, make_response,redirect,url_for,send_file,flash,Markup
import os
import config
from imp import reload
import sys
sys.path.append(os.getcwd().replace("web_app",""))
from app import  Import_Web_To_WittyParrot
import time

app = Flask(__name__)

app.secret_key = 'random string'

@app.route('/')
def index():
    if 'auto_report_wp' in request.cookies:
        con = {"status":True}
        if con["status"]:
            return redirect(url_for("home"))
    return redirect("/login")

@app.route('/login',methods = ['GET'])
def login():
    return render_template("login.html")


@app.route('/webimport',methods=['GET','POST'])
def web_import():
    if request.method == "POST":
        im = Import_Web_To_WittyParrot(obj=flash)
        flash("Import started")
        # time.sleep(2)
        im.check_models_present()
        im.extract_web_data()
        im.check_facets_presence()
        im.check_facet_values_presence()
        flash("Import in middle")
        # time.sleep(2)
        im.check_folder_presense()
        im.check_wits_presence()
        flash("Import Completed")
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
