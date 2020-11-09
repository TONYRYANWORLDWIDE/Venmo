import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import urllib
import json
import base64
import os
import datetime
import json
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import models
import jsonpickle
import datetime
from pathlib import Path
from venmo_api import Client


class getVenmo():
    def __init__(self):
        home = str(Path.home())
        self.credentials_file = os.path.join(home,'Desktop' ,'Venmo' ,'credentials.json')
        self.vusername = ''
        self.vpassword = ''
        self.vdeviceid = ''
        self.accesstoken = ''
        self.server = ''
        self.user = ''
        self.password = ''
        self.database = ''
        self.userid = ''        

    def getCredentials(self):
        self.PLAID_ENV = os.getenv('PLAID_ENV', 'development')
        with open(self.credentials_file) as json_file:
            data = json.load(json_file)
            self.server =   data['codes']['connectionstring']['server']
            self.user =     data['codes']['connectionstring']['user']
            self.password = data['codes']['connectionstring']['password']
            self.database =  data['codes']['connectionstring']['database']
            self.vusername =  data['codes']['Venmo']['vusername']
            self.vpassword =  data['codes']['Venmo']['vpassword']
            self.vdeviceid = data['codes']['Venmo']['vdeviceid']
            self.accesstoken = data['codes']['Venmo']['accesstoken']                        
            self.params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                            "SERVER=" + self.server + ";"
                            "DATABASE=" + self.database + ";"
                            "UID=" + self.user + ";"
                            "PWD=" + self.password)
        return self

class VenmoTransactions():
    vcredentials = getVenmo()
    credentials = vcredentials.getCredentials()
    def getTransactions(self):

        # username = credentials.vusername
        # password = credentials.vpassword
        access_token = self.credentials.accesstoken
        # deviceid = credentials.vdeviceid
        # access_token = Client.get_access_token(username=username,
        #                                password=password)
        venmo = Client(access_token=access_token)
        userid = venmo.user.get_my_profile().id
        usertransactions = venmo.user.get_user_transactions(user_id = userid)
        for i in range(0,len(usertransactions)):
            trans = usertransactions[i].__dict__
            actor = trans['actor'].__dict__
            transfilter = ["id", "payment_id","date_completed", "date_created", "date_updated","amount","status"]
            transfinal = {key: trans[key] for key in transfilter}
            transfinal['transaction_id'] = transfinal['id']
            transfinal['date_completed'] = datetime.datetime.fromtimestamp(int(transfinal['date_completed'])
).strftime('%Y-%m-%d %H:%M:%S')
            transfinal['date_created'] = datetime.datetime.fromtimestamp(int(transfinal['date_created'])
).strftime('%Y-%m-%d %H:%M:%S')
            transfinal['date_updated'] = datetime.datetime.fromtimestamp(int(transfinal['date_updated'])
).strftime('%Y-%m-%d %H:%M:%S')
            del transfinal['id']
            actorfilter = ["id","username", "first_name", "last_name", "display_name"]
            actorfinal = {key: actor[key] for key in actorfilter}
            actorfinal['user_id'] = actorfinal['id']
            del actorfinal['id']
            actorfinal.update(transfinal)
            print(actorfinal)
            fin = models.VenmoTransactions(**actorfinal)
            engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(self.credentials.params))
            DBSession = sessionmaker(bind = engine)    
            session = DBSession()
            session.merge(fin)
            session.commit()
            

def main():
    x = VenmoTransactions()
    x.getTransactions()    

main()
        