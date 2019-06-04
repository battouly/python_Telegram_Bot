import telegram
import json
import logging
from flask import Flask, request

app = Flask(__name__)

HOST = 'https://400ba7a9.ngrok.io'

TOKEN = 'bot token here'
bot = telegram.Bot(token=TOKEN)
botName = 'Fatoumata'

''' mLAB setting '''
import pymongo
from pymongo import MongoClient
mongo = MongoClient('mongodb://Fahtima:Bot123@ds157256.mlab.com:57256/teleg_bot')
db = mongo['teleg_bot']
''' End of mLAB setting '''

def create_profile():
    profile  = {
        "Name": "Leila",
        "Phone": ["982833049043",  "09293048u52843", "qw548293854"],
        "Address": {
            "postbox": 50505,
            "house No": 34,
            "city": "Wilayah Kuala Lumpur",
            "country": "Malaysia"
        }
     }
    pro.insert_one(profile)
    print ("done !!!" )

from modules.telegramBot.main import main

routes = [
    ('/', main)
]

for route in routes:
    app.register_blueprint(route[1], url_prefix=route[0])
