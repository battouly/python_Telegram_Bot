import telegram
import json, os
import logging
from flask import Flask, request

app = Flask(__name__)

#HOST = 'https://dry-lowlands-71228.herokuapp.com/'
HOST = 'https://04f2e852.ngrok.io'

TOKEN = 'bot token here!'
bot = telegram.Bot(token=TOKEN)
botName = 'Fatoumata'

''' mLAB setting '''
import pymongo
from pymongo import MongoClient
mongo = MongoClient('mongodb://Fahtima:Bot123@ds157256.mlab.com:57256/dbname')
db = mongo['dbname']
''' End of mLAB setting '''

from modules.telegramBot.main import main

routes = [
    ('/', main)
]

for route in routes:
    app.register_blueprint(route[1], url_prefix=route[0])
