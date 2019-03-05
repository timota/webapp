# flask app
from flask import Flask

# need to parse the request data
from flask import request

# connect Python Flask with MongoDB
from pymongo import MongoClient

from bson.json_util import dumps

# import json module to load the request.data
import json

# date module
import datetime

# read config file
try:
    with open('app.conf') as json_data_file:
        data = json.load(json_data_file)
except:
    print('Cannot read config file')

# MongoDB connector
client = MongoClient(data['server'], int(data['port']))
db = client.ContactDB

# start Flask
app = Flask(__name__)

# add routers
# POST - add data to db
@app.route("/add", methods = ['POST'])
def add():
    try:
        # get our data from request and decode it
        data = json.loads(request.data.decode('utf-8'))
        
        # parse response
        event = data['event']

        # if value exists - add it to database with timestamp
        if event:
            status = db.Contacts.insert_one({
                "event" : event,
                "date" : datetime.datetime.utcnow() 
            })
        # if data has been added - return success, overwise - error
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

# GET - lets get our data from DB
@app.route("/get_all_events", methods = ['GET'])
def get_all_events():
    try:
        contacts = db.Contacts.find()
        return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})

