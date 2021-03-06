from flask import Flask, render_template, request, make_response,redirect,url_for,send_file,flash,Markup
import os
import config
from imp import reload
import sys
sys.path.append(os.getcwd().replace("web_app",""))
from app import  Import_Web_To_WittyParrot
import time
import shutil
import threading
from api_requests import apis
import json
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

def fl(ll=None):
    pass

def validate_auth(req):
    if 'Authorization' in req.cookies:
        if req.cookies['Authorization']:
            return True
        else:
            return False
    else:
        return False



@app.route('/')
def index():
    print(Import_Web_To_WittyParrot.req_status)
    if 'Authorization' in request.cookies:
        return redirect(url_for('web_import'))
    return redirect("/login")

@app.route("/<name>")
def non_exist(name):
    return redirect("/login")

@app.route('/login',methods = ['GET'])
def login():
    if 'Authorization' in request.cookies:
        return redirect(url_for('web_import'))
    return render_template("login.html")

@app.route('/login')
def re_login():
    return make_response(render_template('login.html',text="logged out successfully"))


@app.route('/web_import',methods=['GET','POST','PUT'])
def web_import():
    if request.method == 'POST':
        con = apis.login(request.form['email_name'],request.form['password'])
        if con:
            resp = make_response(render_template('web_import.html',status=Import_Web_To_WittyParrot.req_status))
            resp.set_cookie(list(con.keys())[0],list(con.values())[0])
            return resp
        else:
            flash("Invalid Credentials")
            return redirect(url_for('re_login'))
    elif request.method == 'GET':
        status = validate_auth(request)
        if status:
            return render_template('web_import.html',status=Import_Web_To_WittyParrot.req_status)
        else:
            return redirect(url_for('login'))


@app.route('/web_import_status',methods=['GET','POST'])
def web_import_status():
    status = validate_auth(request)
    if status:
        if request.method == "POST":
            try:
                # print("web_import_status")
                # print(request.form)
                folders = [i.strip() for i in request.form['folder'].strip().split(",")]
                workspace = request.form["workspace"]
                facet_name = request.form["facet_name"]
                user_detail.update({"folders":folders})
                user_detail.update({"user_id":request.form['email_name'],"password":request.form['password']})
                user_detail.update({"workspace":workspace,"model":facet_name})
                print(user_detail)
                # print("before")
                cd = Import_Web_To_WittyParrot(obj=fl,user_details=user_detail)
                print("cd.user_status()",cd.user_status())
                if cd.user_status():
                    thread = threading.Thread(target=cd.main, name="web import")
                    thread.start()
                    Import_Web_To_WittyParrot.req_status = True
                    # print("in thread")
                    return render_template('web_import_status.html')
                else:
                    flash("please check the details entered and provide request")
                    return render_template('web_import.html')
            except Exception as e:
                print(e)
                flash(str(e))
                return render_template('web_import.html')
        if request.method == "GET":
            status_p = FRAME_PATH+"/import_status/status.json"
            if os.path.exists(status_p):
                con_sf = open(status_p,"r")
                con = json.loads(con_sf.read())
                con_sf.close()
            else:
                con = {}
            # print(con)
            return render_template('web_import_status.html',messages=con)
    else:
        return redirect(url_for('login'))


@app.route("/messages")
def log_messages():
    status_p = FRAME_PATH+"/import_status/status.json"
    if os.path.exists(status_p):
        con_sf = open(status_p,"r")
        con = json.loads(con_sf.read())
        con_sf.close()
    else:
        con = {}
    return render_template('layout.html',messages=con)

@app.route("/login",methods=['POST'])
def logout():
    if 'Authorization' in request.cookies:
        resp = make_response(render_template('login.html',text="logged out successfully"))
        resp.set_cookie('Authorization','', expires=0)
        resp.set_cookie('sessionID', '', expires=0)
        return resp


if __name__=="__main__":
    pass
