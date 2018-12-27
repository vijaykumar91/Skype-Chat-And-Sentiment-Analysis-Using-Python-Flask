from flask import Flask,request, render_template, redirect, url_for,make_response,send_from_directory,send_file
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Response
from flask import jsonify
import urllib.request
import hashlib
import sys
from flask_cors import CORS, cross_origin
from urllib.request import Request, urlopen
from sqlalchemy import func, create_engine
from bs4 import BeautifulSoup
import json
from collections import Counter
import requests, bs4, csv
#-----------  mongo file ----module-----
from pymongo import MongoClient
from bson import ObjectId
import smtplib
from smtplib import SMTPException
import random
from jose import jwt
import datetime

from api import *
#-------------- mongo file -----module end--

#-------CSV xlsx Reder-----------------
import csv
import pandas as pd
import time

import mysql.connector
#--------CSV xlsx Reder--------------

#---------- Skype Validation Start-------#
from skpy import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import glob
import errno
import os
import sys
from collections import Counter
#-----------Skype Validation End------#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

path = 'C:/data_analytics/files/june/*.txt'
f = open('positive.txt')
positive = [line.rstrip() for line in f.readlines()]
f2 = open('negetive.txt')
negetive = [line.rstrip() for line in f2.readlines()]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#---- Postgres Connector Start-------------------#
#engine = create_engine("postgresql://postgres:@localhost/analytics", isolation_level="AUTOCOMMIT")
#---- Postgres Connector end-------------------#

#---- Mongo Connector Start-------------------#
DbUri="mongodb://analytics:analytics#1@ds139534.mlab.com:39534/lws_sentiment"
client = MongoClient(DbUri)
mydb = client
#---- MOngo Connector Start-------------------#

#---- Mysql Connector Start-------------------#
# python app.pydfvdgdfg
#---- Mysql Connector Start-------------------#
'''
db=SQLAlchemy(app)

sk=''
class Signup(db.Model):
    __tablename__='signup'
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('username',db.String)
    email=db.Column('email',db.String)
    password=db.Column('password',db.String)
    active = db.Column('active', db.Integer)
    mobile = db.Column('mobile', db.String)
    skype_id = db.Column('skype_id', db.String)
    address_1 = db.Column('address_1', db.String)
    address_2 = db.Column('address_2', db.String)
    city = db.Column('city', db.String)
    state = db.Column('state', db.String)
    zip = db.Column('zip', db.String)
    gender = db.Column('gender', db.String)
    dob = db.Column('dob', db.String)
    merital_status = db.Column('merital_status', db.String)
    company_name = db.Column('company_name', db.String)
    company_address = db.Column('company_address', db.String)


    def __init__(self,name,email,password):
        self.name = name
        self.id = id
        self.email = email
        self.password = password
        self.mobile = mobile
        self.skype_id = skype_id
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.zip = zip
        self.gender = gender
        self.dob = dob
        self.merital_status = merital_status
'''
#************ Signup start*******
@app.route("/signup", methods=['POST','GET'])
def signup_form():

    error = ""
    alert = ""
    userRequired = {
        'type': 'validation',
        'message': '',
        'status': 0
    }
    userData = {
        'name': '',
        'email':'' ,
        'phone': '',
        'password': ''
    }
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        name = jsonData['username']
        email =jsonData['email']
        phone = jsonData['mobile']
        password = jsonData['password']
        userData = {
            'username':name,
            'email': email,
            'mobile':phone,
            'password': hashlib.sha224(password.encode('utf-8')).hexdigest(),
            'role':'user'
        }


        if name == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Name is required',
                'status': 0
            }

        if email == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Email is required',
                'status': 0
            }

        if phone == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Phone is required',
                'status': 0
            }

        if password == "":
            userRequired = {
                'type': 'validation',
                'message': 'password is required',
                'status': 0
            }

        if name !="" and email !="" and password !="" and phone !="":
            record_id2 = mydb.users.find_one({"email": email});
            if(record_id2):
                return jsonify({'type': 'signup','message': 'Email-Id already Exists','status': 0})
                sys.exit()
            else:
                record_id = mydb.users.insert(userData)
                if(record_id):
                    id='';
                    id=record_id
                    userSignupSuccess = {
                        'type': 'sinup',
                        'message': 'user signup successfully',
                        'username': name,
                        'email': email,
                        'mobile': phone,
                        'id':str(id),
                        'status':1
                    }
                    return jsonify(userSignupSuccess)
                    sys.exit()
                else:
                    userRequired = {
                        'type': 'signup',
                        'message': 'Signup Fail! something went wrong',
                        'status': 0
                    }
                    return jsonify(userRequired)
                    sys.exit()
        else:

            return jsonify(userRequired)
            sys.exit()
    return jsonify(status)

#************ Signup End*******


#************ Login start*******
@app.route("/login", methods=['POST','GET'])
def login_form():
    auth = request.authorization
    error = ""
    alert = ""
    userRequired = {
        'type': 'validation',
        'message': '',
        'status': 0
    }
    userData = {
        'name': '',
        'email':'' ,
        'phone': '',
        'password': ''
    }
    status = {
        'name': 'Request are invalid!',
        'status': 0,
    }
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        email =jsonData['email']
        password = jsonData['password']
        password = hashlib.sha224(password.encode('utf-8')).hexdigest()


        if email == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Email is required',
                'status': 0
            }
        if password == "":
            userRequired = {
                'type': 'validation',
                'message': 'password is required',
                'status': 0
            }
        if email !="" and password !="":
            #record_id = mydb.users.insert(userData)
            record_id = mydb.users.find_one({"email":email, "password":password});
            if(record_id):
                token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=6000),
                                    'iat': datetime.datetime.utcnow(), 'sub': str(record_id)
                                    }, app.config['SECRET_KEY'], algorithm='HS256')
                for key, val in record_id.items():
                    if '_id' in key:
                        user_id = val
                    if 'email' in key:
                        email = val
                    if 'mobile' in key:
                        mobile = val
                    if 'role' in key:
                        role = val
                update=mydb.users.update_one({
                    '_id': ObjectId(user_id)
                }, {
                    '$set': {
                        'token': token
                    }
                }, True)
                if(update):
                    return jsonify({'message': 'user login successfully', 'status': 1,'user_id':str(user_id), 'email':email,"mobile":mobile,'role':role,'token':token})
                    sys.exit()
                #if auth and auth.password == 'secret':
                #return make_response('Could not verify! secret is wrong', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
                #sys.exit()
            else:
                userRequired = {
                    'type': 'login',
                    'message': 'Login Fail! Email or Password is wrong',
                    'status': 0
                }
                return jsonify(userRequired)
                sys.exit()
        else:

            return jsonify(userRequired)
            sys.exit()
    return jsonify(status)

#************ Login End*******


#************ ForgotPassword start*******
@app.route("/forgotPass", methods=['POST','GET'])
def forgotPass_form():
    error = ""
    alert = ""
    userRequired = {
        'type': 'validation',
        'message': '',
        'status': 0
    }
    userData = {
        'name': '',
        'email':'' ,
        'phone': '',
        'password': ''
    }
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        email =jsonData['email']

        if email == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Email is required',
                'status': 0
            }
        if  email !="":
            #record_id = mydb.users.insert(userData)
            #get
            record_id = mydb.users.find_one({"email":email});
            password=''.join(random.choice('0123456789ABCDEF') for i in range(6))
            'E2C6B2E19E4A7777'
            password=password+'T#$@'
            user_id=''
            if(record_id):
                sender = 'data-delivery@loginworks.com'
                receivers = [email]
                message = """From: From Person <data-delivery@loginworks.com>
                To: To Person <"""+email+""">
                Subject: Forgot Password

                your new password is:"""+password+""" 
                """
                try:
                    #smtpObj = smtplib.SMTP('localhost')
                    smtpObj = smtplib.SMTP('host.apponlease.com', 587)
                    smtpObj.sendmail(sender, receivers, message)
                    print("Successfully sent email")
                    for key, val in record_id.items():
                        if '_id' in key:
                            user_id=val  # now you got only date column values

                    query = mydb.users.update_one({
                        '_id': user_id
                    }, {
                        '$set': {
                            'password': hashlib.sha224(password.encode('utf-8')).hexdigest()
                        }
                    }, upsert=False)
                except SMTPException:
                    print("Error: unable to send email")

                userSignupSuccess = {
                    'type': 'forgot_password',
                    'message': 'password  send on register email',
                    'status':1
                }
                return jsonify(userSignupSuccess)
                sys.exit()
            else:
                userRequired = {
                    'type': 'forgot_password',
                    'message': 'Email-id not register with Us.',
                    'status': 0
                }
                return jsonify(userRequired)
                sys.exit()
        else:

            return jsonify(userRequired)
            sys.exit()
    return jsonify(status)
#************ Forgot Password*******
'''
@app.route("/search_cat", methods=['POST','GET'])
def search_cat_form():
    searchValidation = {
        'message': 'pleas Enter Something.',
        'status': True,
        'status_code': 1,
    }

    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        searchData = jsonData['search']

        result = engine.execute("SELECT * FROM getsearchproduct(%s); ",(searchData))

        new_data1=[]
        for line in result:
            new_data = {}
            new_data['id'] = line.id
            new_data['description'] = line.description
            new_data['price'] = line.price
            new_data['brand'] = line.brand
            new_data['review'] = line.review
            new_data['pageimage'] = line.pageimage
            new_data['linkID'] = line.linkID
            new_data['imagelink'] = line.imagelink
            new_data1.append(new_data)

        searchValidation = {
            'message': 'pleas Enter Something.',
            'status': True,
            'products':new_data1
        }
        return jsonify(searchValidation)
        sys.exit
'''
@app.route("/search", methods=['POST','GET'])
def search_form():
    searchValidation = {
        'message': 'pleas Enter Something.',
        'status': True,
        'status_code': 1,
    }
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        searchData = jsonData['search']
        if searchData == "":
                return jsonify(searchValidation)
        else:
            req = Request('https://www.guru.com/jobs/1462449/chat/25697',
                          headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            print(soup)
            titles = soup.findAll('h3', attrs={'class': 'r'})
            print(titles)
            sys.exit();
        #return response.read()

@app.route("/unprotected", methods=['POST','GET'])
def unprotected():
    #print(readwords())
    sys.exit()
    # if request.method == 'POST':
    #     jsonData = request.get_json(force=True)
    #     token = jsonData['token']
    #     rs=verify_token(token)

@app.route("/protected", methods=['POST', 'GET'])

def protected():
    message = client.messages \
        .create(
        body="Join Earth's mightest heroes. Like Kevin Bacon.",
        from_='+15017122661',
        to='7838043535'
    )

    print(message.sid)
    sys.exit()
    return jsonify({'message': 'This is the only available  for people with valid token!'})

def verify_token(token):
        try:
             jwt.decode(token, 'thisissecret', algorithms=['HS256'])
             return  True
        except jwt.ExpiredSignatureError:
             return False

#************ Logout start*******
@app.route("/logout", methods=['POST','GET'])
def logout_form():
    error = ""
    alert = ""
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        id =jsonData['id']
        if id == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Id is required',
                'status': 0
            }
        if  id !="":
            query = mydb.users.update_one({
                '_id': ObjectId(id)
            }, {
                '$set': {
                    'token': ""
                }
            },True)
            return jsonify({"message":"user logout successfully!","status":"1"})
            sys.exit()
        else:
            return jsonify(userRequired)
        sys.exit()
    return jsonify(status)
#************ Logout End*******


#************  Add manager *********
@app.route("/add_manager", methods=['POST'])
def add_manager_form():
    error = ""
    alert = ""

    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        name =jsonData['name']
        id=jsonData['id']
        token = request.headers['Authorization']
        token = token.split()[1]
        phone = jsonData['phone']
        email = jsonData['email'].strip()
        type = jsonData['role_type']
        data={
            "name":name,
            "phone":phone,
            "email":email,
            "role_type":type
        }

        if name == "" :
            return jsonify({"type": "validation!", "message":"name are required.","status": "0"})
            sys.exit()
        if email == "" :
            return jsonify({"type": "validation!", "message":"email are required.","status": "0"})
            sys.exit()

        if  name !="":
            checkSecuirity=verify_token(token)
            record_id = mydb.users.find_one({"_id": ObjectId(id)});

            for key, val in record_id.items():
                if 'token' in key:
                    token = val  # now you got only date column values
            if(checkSecuirity ==True and token !=''):
                try:
                     emailExist = mydb.manager.find({"email":email}).count();
                     if(emailExist > 0):
                         return jsonify({'type': 'signup', 'message': 'Email-Id already Exists', 'status': 0})
                         sys.exit()
                     else:
                        try:
                            record_id = mydb.manager.insert(data)
                            if (record_id):
                                id = '';
                                id = record_id
                                return jsonify({'type': 'add_manager','message': 'Manager Added Successfully','name': name,'phone':phone,'id': str(id),'status': 1})
                                sys.exit()
                            else:
                                return jsonify({"message": "add manager fail!", "status": "0"})
                                sys.exit()
                        except:
                            return jsonify({"message": "Add Manager Fail something went wrong!","exception_level": 2,"status":0,"code":500})
                            sys.exit()
                except:
                    return jsonify(
                        {"message": "Add Manager Fail something went wrong!", "exception_level": 1, "status": 0,
                         "code": 500})
                    sys.exit()
            else:
                return jsonify({"message": "token are invalid!", "status": "0"})
                sys.exit()
        else:
            return jsonify(userRequired)
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Add Manger End*******

#************Add Project  Start*********
@app.route("/add_project", methods=['POST','GET'])
def add_project_form():
    error = ""
    alert = ""
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        name =jsonData['project_name']
        start_date = jsonData['start_date']
        end_date = jsonData['end_date']
        milestones= jsonData['milestones']
        role_type = jsonData['role_type']
        user_name = jsonData['user_name']
        rating=jsonData['rating']
        token = request.headers['Authorization']
        token = token.split()[1]
        id=jsonData['id']
        projectData={
            "name":name,
            "start_date":start_date,
            "end_date":end_date,
            "rating":rating,
            "role_type":role_type,
            "user_name":user_name,
            "milestones":json.dumps(milestones),
        }
        if name == "" :
            return jsonify({"type": "validation!", "message":"project name are required.","status": "0"})
            sys.exit()
        if start_date == "" :
            return jsonify({"type": "validation!", "message":"start date required.","status": "0"})
            sys.exit()
        if  name !="" and start_date!="":
            checkSecuirity=verify_token(token)
            record_id = mydb.users.find_one({"_id": ObjectId(id)});

            for key, val in record_id.items():
                if '_id' in key:
                    record_id = val  # now you got only date column values

            if(checkSecuirity ==True and token !=''):
                try:
                        record_id = mydb.project.insert(projectData)
                        if (record_id):
                            id = '';
                            id = record_id
                            return jsonify({'type': 'add_project','message': 'Project Added Successfully','name': name,'start_date':start_date,'id': str(id),'status': 1,"code":200})
                            sys.exit()
                        else:
                            return jsonify({"message": "add project fail!", "status": "0","code":403})
                            sys.exit()

                except:
                    return jsonify({"message": "something went wrong!","status":0,"code":500})
                    sys.exit()
            else:
                return jsonify({"message": "token are invalid!", "status": "0","code":401})
                sys.exit()
        else:
            return jsonify(userRequired)
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Add Project End*******



#************ Validate Admin *******
@app.route("/isadmin", methods=['POST','GET'])
def isadmin_form():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        id =jsonData['id']
        token = jsonData['token']
        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()
        if id !="":
            checkSecuirity = verify_token(token)
            record_id2 = mydb.users.find_one({"_id": ObjectId(id)});

            for key, val in record_id2.items():
                if 'token' in key:
                    token1 = val  # now you got only date column values

            if (checkSecuirity == True and token1 != ''):
                    try:
                        record_id = mydb.users.find_one({"_id": ObjectId(id)});
                        if(record_id):
                            for key, val in record_id.items():
                                if 'role' in key:
                                    role = val
                            if(role=='admin'):
                                return jsonify({"message": "role verify successfully!", "status": "1",'code':200})
                                sys.exit()
                            else:
                                return jsonify({"message": "role is not valid!", "status": "0"})
                                sys.exit()
                        else:
                            return jsonify({"message": "id is are required!", "status": "0"})
                            sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0, "code": 500})
                        sys.exit()
            else:
                return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Validate Admin End*******


#************ renew token *******
@app.route("/renew_token", methods=['POST','GET'])
def renew_token_form():
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        id =jsonData['id']
        token = jsonData['token']
        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()
        if id !="":
            try:
                checkSecuirity = verify_token(token)
                record_id2 = mydb.users.find_one({"_id": ObjectId(id)});
                for key, val in record_id2.items():
                    if 'token' in key:
                        token1 = val  # now you got only date column values
                    if 'role' in key:
                        role = val  # now you got only date column values
                if (checkSecuirity == True and token1 != ''):
                    try:
                        token2 = jwt.encode(
                            {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=6000),
                             'iat': datetime.datetime.utcnow(), 'sub': str(id)
                             }, app.config['SECRET_KEY'], algorithm='HS256')

                        update = mydb.users.update_one({
                            '_id': ObjectId(id)
                        }, {
                            '$set': {
                                'token': token2
                            }
                        }, True)
                        if (update):
                            return jsonify(
                                {'message': 'token renew successfully', 'status': 1, 'user_id': str(id), 'role': role,
                                 'token': token})
                            sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0, "code": 500})
                        sys.exit()
                else:
                    return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                    sys.exit()
            except:
                return jsonify({"message": "something went wrong!", "status": 0, "code": 500})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ renew token End*******


#************ get project list *******
@app.route("/project_list", methods=['GET'])
def project_list_token_form():
    if request.method == 'GET':
        id = request.args.get('id')
        token = request.headers['Authorization']
        token=token.split()[1]

        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()
        if id !="":
            try:
                checkSecuirity = verify_token(token)
                record_id2 = mydb.users.find_one({"_id": ObjectId(id)});
                for key, val in record_id2.items():
                    if 'token' in key:
                        token1 = val  # now you got only date column values
                    if 'role' in key:
                        role = val  # now you got only date column values

                if (checkSecuirity == True and token1 != ''):
                    try:
                        all_project = mydb.project.find();
                        projects=[]
                        for projectDtl in all_project:
                            projects.append({'id':str(projectDtl['_id']),'name':projectDtl['name'],'start_date':projectDtl['start_date'],'end_date':projectDtl['end_date'],'rating':projectDtl['rating'],'user_name':projectDtl['user_name'],'role_type':projectDtl['role_type'],'milestones':projectDtl['milestones']})

                        return jsonify({"project_lists":projects, "status": 1, "code": 200})
                        sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0,"exception_level": 2, "code": 500})
                        sys.exit()
                else:
                    return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                    sys.exit()

            except:
                return jsonify({"message": "something went wrong!", "status": 0, "exception_level": 1,"code": 500})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 401})
#************ get project list End*******

#************ get manager list *************
@app.route("/manager_list", methods=['GET'])
def manager_list_token_form():
    if request.method == 'GET':
        id = request.args.get('id')
        token = request.headers['Authorization']
        token=token.split()[1]

        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()
        if id !="":
            try:
                checkSecuirity = verify_token(token)
                record_id2 = mydb.users.find_one({"_id": ObjectId(id)});
                for key, val in record_id2.items():
                    if 'token' in key:
                        token1 = val  # now you got only date column values
                    if 'role' in key:
                        role = val  # now you got only date column values

                if (checkSecuirity == True and token1 != ''):
                    try:
                        all_project = mydb.manager.find();
                        projects=[]
                        for projectDtl in all_project:
                            projects.append({'manager_id':str(projectDtl['_id']),'name':projectDtl['name'],'phone':projectDtl['phone'],'email':projectDtl['email'],'role_type':projectDtl['role_type']})

                        return jsonify({"manager_lists":projects, "status": 1, "code": 200})
                        sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0,"exception_level": 2, "code": 500})
                        sys.exit()
                else:
                    return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                    sys.exit()

            except:
                return jsonify({"message": "something went wrong!", "status": 0, "exception_level": 1,"code": 500})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ get project list End*******

#************ UPDATE Product *************
@app.route("/update_project", methods=['PUT'])
def update_project_form():
    if request.method == 'PUT':
        jsonData = request.get_json(force=True)
        id = jsonData['id']
        token = request.headers['Authorization']
        token = token.split()[1]

        project_id = jsonData['project_id']
        project_name = jsonData['project_name']
        start_date = jsonData['start_date']
        end_date = jsonData['end_date']
        rating = jsonData['rating']
        role_type = jsonData['role_type']
        user_name = jsonData['user_name']
        milestones = jsonData['milestones']

        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()
        if id !="":
            try:
                checkSecuirity = verify_token(token)
                record_id2 = mydb.users.find_one({"_id": ObjectId(id)});
                for key, val in record_id2.items():
                    if 'token' in key:
                        token1 = val  # now you got only date column values
                    if 'role' in key:
                        role = val  # now you got only date column values

                if (checkSecuirity == True and token1 != ''):
                    try:
                        query = mydb.project.update_one({
                            '_id': ObjectId(project_id)
                        }, {
                            '$set': {'name': project_name,'start_date': start_date,'end_date': end_date,'rating':rating,'role_type':role_type,'user_name':user_name,'milestones':json.dumps(milestones)}
                        })

                        return jsonify({"message": 'project updated successfully!', "status": 1, "code": 200})
                        sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0,"exception_level": 2, "code": 500})
                        sys.exit()
                else:
                    return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                    sys.exit()

            except:
                return jsonify({"message": "something went wrong!", "status": 0, "exception_level": 1,"code": 500})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ update project End*******



#************ UPDATE User *************
@app.route("/update_manager", methods=['PUT'])
def update_manager_form():
    if request.method == 'PUT':
        jsonData = request.get_json(force=True)
        id = jsonData['id']
        token = request.headers['Authorization']
        token = token.split()[1]

        manager_id = jsonData['manager_id']
        phone = jsonData['phone']
        name = jsonData['name']
        project = jsonData['project']
        email = jsonData['email']
        role_type = jsonData['role_type']


        if id == "" :
            return jsonify({'message': 'user  id required', 'status': 0})
            sys.exit()

        if id !="":
            try:
                checkSecuirity = verify_token(token)
                record_id2 = mydb.users.find_one({"_id": ObjectId(id)});
                for key, val in record_id2.items():
                    if 'token' in key:
                        token1 = val  # now you got only date column values
                    if 'role' in key:
                        role = val  # now you got only date column values

                if (checkSecuirity == True and token1 != ''):
                    try:
                        checkDuplicateEmail = mydb.manager.find({"$and": [{"email": email}, {"_id": {"$ne": ObjectId(manager_id)}}]}).count();
                        if(checkDuplicateEmail >=1):
                            return jsonify({"message": 'Email ID already Exist in Database!', "status": 0, "code": 200})
                            sys.exit()
                        else:
                            try:
                                query = mydb.manager.update_one({
                                    '_id': ObjectId(manager_id)
                                }, {
                                    '$set': {'phone': phone, 'name': name, 'project': project, 'email': email,
                                             'role_type': role_type}
                                })
                                return jsonify({"message": 'manager updated successfully!', "status": 1, "code": 200})
                                sys.exit()
                            except:
                                return jsonify({"message": "something went wrong!", "status": 0, "exception_level": 3,
                                                "code": 500})
                                sys.exit()
                    except:
                        return jsonify({"message": "something went wrong!", "status": 0,"exception_level": 2, "code": 500})
                        sys.exit()
                else:
                    return jsonify({"message": "token or id are not valid!", "status": 0, "code": 401})
                    sys.exit()

            except:
                return jsonify({"message": "something went wrong!", "status": 0, "exception_level": 1,"code": 500})
                sys.exit()
        else:
            return jsonify({"message": "fields are missing!", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ update project End*******


#************ Update Password Start*********
@app.route("/password_update", methods=['PUT'])
def password_update_form():
    error = ""
    alert = ""

    if request.method == 'PUT':
        jsonData = request.get_json(force=True)
        token = request.headers['Authorization']

        token = token.split()[1]

        email = jsonData['email'].strip()
        password = jsonData['password']

        if  email !="":
            emailExist = mydb.users.find({"email": email}).count();
            if (emailExist > 0):
                try:
                    query = mydb.users.update_one({
                        'email': email
                    }, {
                        '$set': {
                            'password': hashlib.sha224(password.encode('utf-8')).hexdigest()
                        }
                    }, upsert=False)

                    jsonify({'type': 'forgotpass', 'message': 'password updated successfully', 'status': 1,"code": 200})
                    sys.exit()
                except:
                    return jsonify(
                        {"message": "update password Fail something went wrong!", "exception_level": 1, "status": 0,
                         "code": 500})
                    sys.exit()

            else:
                return jsonify({'type': 'forgotpass', 'message': 'Email-Id not register in database', 'status': 0})
                sys.exit()
        else:
            return jsonify(userRequired)
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Update Password End*******



#************ Skype Login*********
@app.route("/skype_login", methods=['POST'])
def skype_login_form():
    error = ""
    alert = ""
    contacts = []
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        username =jsonData['username']
        password = jsonData['password']
        if username == "" :
            return jsonify({'message': 'username is  required', 'status': 0})
            sys.exit()

        if password == "" :
            return jsonify({'message': 'password is  required', 'status': 0})
            sys.exit()
        if username !="" and password !="":
            try:
                sk = Skype(username,password)
                source_contacts = sk.contacts

                for contact in source_contacts:

                    contacts.append({'id':str(contact.id),'name':str(contact.name),'birthday':str(contact.birthday),'phone':str(contact.phones),'dob':str(contact.birthday),'image':str(contact.avatar)})
                # for contact in contacts:
                #     #print(contact)
                #     print('hi....')
                return jsonify({"message": 'Skype Login successfully!', "status": 1,"contact_list":contacts, "code": 200})
                sys.exit()
            except Exception as exc:
                return jsonify({"message":"Your account or password is incorrect. If you don't remember your password, reset it now", "status": "0", "code": 401})
                sys.exit()
        else:
            return jsonify({"message": "username and password are required", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Skype Login End*******



#************ Skype Chat Detail Start*********
@app.route("/skype_chat", methods=['POST'])
def skype_chat_form():
    error = ""
    alert = ""
    contacts = []

    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        contact_user_id =jsonData['contact_user_id']
        username = jsonData['username']
        password = jsonData['password']
        if contact_user_id == "" :
            return jsonify({'message': 'contact user id required', 'status': 0})
            sys.exit()

        if contact_user_id !="":
            try:
                sk = Skype(username, password)

                source_contacts = sk.contacts
                contacts.append(str(contact_user_id))

                for contact in contacts:
                    try:
                        chat = sk.contacts[contact].chat

                        if chat:
                            if (chat.getMsgs() != ""):
                                message = ""
                                for mes in chat.getMsgs():
                                    message=get_message(mes)
                                sk = Skype(connect=False)
                                if(message):
                                    message=message
                                    return jsonify({"message": "Chat Analysis Successfull", "status": "1", "report": message,
                                         "code": 200})
                                else:
                                    message=[]
                                    return jsonify({"message": "No recent chat awailable", "status": "0","report":message, "code": 401})
                                sys.exit()
                    except Exception as exc:
                        return jsonify({"message": "Contact list error", "status": "0", "error_lavel": 2, "code": 500})
                        sys.exit()
            except Exception as exc:
                return jsonify({"message":"Something wrong please try again", "status": "0","error_lavel":1, "code": 500})
                sys.exit()
        else:
            return jsonify({"message": "username and password are required", "status": "0", "code": 405})
            sys.exit()
    return jsonify({"message": "request are not valid!", "status": "0", "code": 405})

#************ Skype Chat Detail End*********#

#--------------Sentiment start------------------#
date_chat=[]
analyzer = SentimentIntensityAnalyzer()
def get_message(msg):
        #print(str(msg.time).split(" ")[0])
        #dates=str(msg.time).split(" ")[0]
        # if dates in k:
        #     date_chat.append(dates)
        #return date_chat
        vs = analyzer.polarity_scores(str(msg.content))
        positive_negetive_data=positive_negetive_count(str(msg.content))
        neg = str(vs).split(",")[0]
        compund = str(vs).split(",")[3]
        neg = neg.replace("{", "")
        neg = neg.replace("'", '')
        compund = compund.replace("}", "")
        compund = compund.replace("'", '')
        neu = str(vs).split(",")[1]
        neu = neu.replace("'", '')
        pos = str(vs).split(",")[2]
        pos = pos.replace("'", '')

        neg = neg.split(":")[1].strip(" ")
        neu = neu.split(":")[1].strip(" ")
        pos = pos.split(":")[1].strip(" ")
        compund = compund.split(":")[1].strip(" ")
        # print(neg)
        # print(neu)
        # print(pos)
        # print(compund)

        date_chat.append({'date':msg.time,'chats':msg.content,"neg":neg,"neu":neu,"pos":pos,"compound":compund,'positive_negative_data':positive_negetive_data})

        return date_chat
#--------------Sentiment end------------------#

#--------------Positive Negetive Count------------------#
def positive_negetive_count(paragraph):

    f = open('positive.txt')
    positive = [line.rstrip() for line in f.readlines()]
    f2 = open('negetive.txt')
    negative = [line.rstrip() for line in f2.readlines()]
    polarity = ''
    textSet = ''
    count = Counter(paragraph.split())
    pos = 0
    neg = 0
    positive_negetive_arr=[]
    for key, val in count.items():
        key = key.rstrip('.,?!\n')  # removing possible punctuation signs
        if key in positive:
            pos += val
        if key in negative:
            neg += val

    sentiment = int(pos) - int(neg)
    positive = str(pos)
    negetive = str(neg)
    sentiment = str(sentiment)

    if sentiment == '0' :
        sentiment=0
    elif sentiment > '0' or sentiment <= '+3' :
        sentiment = 3
    elif sentiment >'-1' or sentiment <= '-3':
        sentiment = -3
    elif  sentiment >='-5':
        sentiment = -5
    elif sentiment >='+5':
        sentiment = '+5'
    else:
        sentiment = sentiment

    positive_negetive_arr.append({'positive':positive,'negative':negetive,'sentiment':sentiment})
    return positive_negetive_arr

#--------------Positive Negetive Count End------------------#

#--------------Glassdoor Review Data------------------#
@app.route("/srape_data", methods=['POST'])
def srape_data_form():
    error = ""

    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        website_type=jsonData['website_type']
        if(website_type=='glassdoor'):
            glassdoor_data()
        elif(website_type=='facebook'):
            facebook_data()
        elif (website_type == 'trustpilot'):
            trustpilot_data()
        elif (website_type == 'indeed'):
            indeed_data()

    else:
        return jsonify({"message": "request are not valid!", "status": "0", "code": 405})
#************ Skype Login End*******
def get_content(x):
    ratingArr = []
    prosArr = []
    date_timeArr = []
    ratingArr = []
    consArr = []
    ratingArr = []
    titleArr = []
    allArr = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    page = requests.get('https://www.glassdoor.co.in/Reviews/Loginworks-Reviews-E913549_P' + str(x) + '.htm',
                        headers=headers)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    results_table = soup.find(id='EmployerReviews')
    #pros = results_table.find_all(class_="pros")

    pros = results_table.find_all(class_="pros")
    prosArr.append(pros)

    date_time = results_table.find_all(class_="date subtle small")
    date_timeArr.append(date_time)


    rating = results_table.find_all(class_="value-title")
    ratingArr.append(rating)

    title = results_table.find_all(class_="reviewLink")
    titleArr.append(title)

    adviceMgmt = results_table.find_all(class_="adviceMgmt")
    cons = results_table.find_all(class_="cons")
    consArr.append(cons)
    info = results_table.find_all('description ')

    #return prosArr.date_timeArr.ratingArr.titleArr.consArr
    return prosArr,date_timeArr,ratingArr,titleArr,consArr
#--------------Glassdoor Review Data End------------------#
#=====================Glassdoor Review Start=====================#
def glassdoor_data():
        header = [' Review_ID', 'Review_date', 'Review_title', 'Google_rating', 'Review_details_prequestsros',
                  'Review_details_cons']
        prosArr = []
        date_timeArr = []
        ratingArr = []
        consArr = []
        ratingArr = []
        pros = []
        resultArr=[]
        titleArr = []

        count = 1
        while count < 6:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            page = requests.get('https://www.glassdoor.co.in/Reviews/Loginworks-Reviews-E913549_P' + str(count) + '.htm',
                                headers=headers)

            soup = bs4.BeautifulSoup(page.content, 'html.parser')
            results_table = soup.find(id='EmployerReviews')
            # pros = results_table.find_all(class_="pros")

            pros = results_table.find_all(class_="pros")
            prosArr.append(pros)

            date_time = results_table.find_all(class_="date subtle small")
            date_timeArr.append(date_time)

            rating = results_table.find_all(class_="value-title")
            ratingArr.append(rating)

            title = results_table.find_all(class_="reviewLink")
            titleArr.append(title)

            adviceMgmt = results_table.find_all(class_="adviceMgmt")
            cons = results_table.find_all(class_="cons")
            consArr.append(cons)
            info = results_table.find_all('description ')
            count += 1

        with open('C:/data_analytics/files/reviews.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(i for i in header)
            for j in range(5):
                for i in range(len(prosArr[j])):
                    #print(prosArr[j][i].get_text())
                    filewriter.writerow(
                        [i, date_timeArr[j][i].get_text(), titleArr[j][i].get_text(), ratingArr[j][i]['title'], prosArr[j][i].get_text(),
                         consArr[j][i].get_text()])
            # return send_file('C:/Users/abc/Downloads/barcode',
            #                  mimetype='text/csv',
            #                  attachment_filename='downloadFile.csv',
            #                  as_attachment=True)

#=====================Glassdoor Review End=======================#

#=====================Facebook Review Start=====================#
def facebook_data():
        header = [' Review_ID', 'Review_date', 'Review_title', 'Google_rating', 'Review_details_prequestsros',
                  'Review_details_cons']
        prosArr = []
        date_timeArr = []
        ratingArr = []
        consArr = []
        ratingArr = []
        pros = []
        resultArr=[]
        titleArr = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        page = requests.get('https://www.facebook.com/pg/lognow/reviews/',
                            headers=headers)

        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        print(soup)
        sys.exit()

        results_table = soup.find(id='EmployerReviews')
        # pros = results_table.find_all(class_="pros")

        pros = results_table.find_all(class_="pros")
        prosArr.append(pros)

        date_time = results_table.find_all(class_="date subtle small")
        date_timeArr.append(date_time)

        rating = results_table.find_all(class_="value-title")
        ratingArr.append(rating)

        title = results_table.find_all(class_="reviewLink")
        titleArr.append(title)

        adviceMgmt = results_table.find_all(class_="adviceMgmt")
        cons = results_table.find_all(class_="cons")
        consArr.append(cons)
        info = results_table.find_all('description ')
#=====================Glassdoor Review End=======================#

#=====================Facebook Review Start=====================#
def trustpilot_data():
        header = [' Review_ID', 'Review_date', 'Review_title', 'Rating', 'Review_details',
                  'Review_details_cons']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        page = requests.get('https://www.trustpilot.com/review/www.loginworks.com?languages=all',
                            headers=headers)

        soup = bs4.BeautifulSoup(page.content, 'html.parser')


        results_table = soup.find(class_='reviews-container')
        title = results_table.find_all(class_="review-info__body__title")
        date_time = results_table.find_all(class_="header__verified__date")

        rating = results_table.find_all(class_="star-rating")
        review_description = results_table.find_all(class_="review-info__body__text")

        with open('C:/data_analytics/files/trustpilot.csv', 'w',encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(i for i in header)
            for i in range(len(title)):

                filewriter.writerow(
                    [i, date_time[i].get_text(), title[i].get_text(), rating[i]['class'], review_description[i].get_text()])
            #sys.exit()
#=====================Glassdoor Review End=======================#

#=====================Facebook Review Start=====================#
def indeed_data():
        header = [' Review_ID', 'Review_date', 'Review_title', 'Rating', 'Review_details',
                  'Review_details_cons']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        page = requests.get('https://www.indeed.co.in/cmp/Loginworks-Software/reviews',
                            headers=headers)

        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        results_table = soup.find(id='cmp-content')
        title = results_table.find_all(class_="cmp-review-title")
        date_time = results_table.find_all(class_="cmp-review-date-created")

        rating = results_table.find_all('meta',itemprop="ratingValue")
        review_description = results_table.find_all(class_="cmp-review-text")

        pros = results_table.find_all(class_="cmp-review-pro-text")

        with open('C:/data_analytics/files/indeed.csv', 'w',encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(i for i in header)
            for i in range(len(title)):
                filewriter.writerow(
                    [i, date_time[i].get_text(), title[i].get_text(), rating[i]['content'], review_description[i].get_text()])
            #sys.exit()
#=====================Glassdoor Review End=======================#


#**************************************
if __name__=="__main__":
    app.run()

