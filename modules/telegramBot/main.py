import telegram
#import josn
import logging
import time
import datetime
import os
from flask import request, Blueprint

from modules import (bot)
from modules.message.utils import Utils
from modules.message.handler import handle_callbacks
from modules.Consts.main import Const
from models.message import MessageModel
from modules.task.main import Task
#from telegram import ReplyKeyboardMarkup

main = Blueprint('main', __name__)

def generate_id():
    return os.urandom(5).hex()

@main.route('/', methods=['POST'])
def webhook_handler():
    #print('im hereeee')
    timestamp = int(time.time())
    _date = datetime.datetime.now().strftime('%d %B')
    try:
        if request.method == "POST":
            # retrieve the message in JSON and transform it to Telegram object
            update = telegram.Update.de_json(request.get_json(force=True),bot)
            if bool(update):
                if update.message:
                    chat_id = update.message.chat.id 
                    message_id = update.message.message_id
                    #commands for displaying inlinekeyboard
                    print (chat_id,'_hello')
                    _id = generate_id()
                    if update.message.entities:
                        for entity in update.message.entities:
                            if entity.type == 'bot_command':
                                c_offset = entity.__dict__.get('offset')
                                c_length = entity.__dict__.get('length')
                                cmnd = update.message.text[c_offset+1: c_offset+ c_length]
                                task_txt = update.message.text[c_offset+ c_length:]
                                txt = 'Issuer: {}({})\nTitle: {}'.format(update.message.from_user.full_name, _date, task_txt)
                                if cmnd == 'task':
                                    _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
                                    res = bot.sendMessage(chat_id=chat_id, message_id=message_id,text=txt or ' Do nothing ' , parse_mode='Markdown', reply_markup=_key)
                                    print("done 1st step")
                                    
                                    Task.save_task({
                                        'timestamp': int(timestamp),
                                        'task': task_txt,
                                        'issuer_id': chat_id,
                                        'issue': update.message.from_user.full_name,
                                        'level': '',
                                        'status': 'initiate',
                                        'message_id': res.message_id,
                                        'id':_id,
                                        'department': '',
                                        'assignee': '',
                                        'photo': False
                                    })
                                    MessageModel.save_one({
                                        'message_id': res.message_id,
                                        'text': txt,
                                        'task': task_txt,
                                        'chatid':chat_id,
                                        'keyboard':Const.mainInKeyBoard,
                                        'photo':'',
                                        'id':_id
                                    })
                                    bot.delete_message(chat_id=chat_id, message_id=message_id,text=txt)
                                else:
                                    bot.sendMessage(chat_id=chat_id, text='blah blah')  
                                    bot.delete_message(chat_id=chat_id, message_id=message_id,text=txt)             
                    elif update.message.caption_entities:
                        for entity in update.message.caption_entities:
                            photo = update.message.photo[-1].file_id
                            if entity.type == 'bot_command':
                                print ('printing update message')
                                print(update.message.caption)
                                
                                c_offset = entity.__dict__.get('offset')
                                c_length = entity.__dict__.get('length')
                                cmnd = update.message.caption[c_offset+1: c_offset+ c_length]
                                task_txt = update.message.caption[c_offset+ c_length:]
                                txt = 'Issuer: {}({})\nTitle: {}'.format(update.message.from_user.full_name, _date, task_txt)
                                if cmnd == 'task':
                                    _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
                                    res = bot.send_photo(chat_id=chat_id, message_id=message_id, caption=txt or ' Do nothing ' ,
                                    photo=photo, parse_mode='Markdown', reply_markup=_key) 
                                    Task.save_task({
                                        'timestamp': int(timestamp),
                                        'task': task_txt,
                                        'issuer_id': chat_id,
                                        'issue': update.message.from_user.full_name,
                                        'level': '',
                                        'status': 'initiate',
                                        'message_id': res.message_id,
                                        'id':_id,
                                        'department': '',
                                        'assignee': '',
                                        'photo':photo
                                    })
                                    MessageModel.save_one({
                                        'message_id': res.message_id,
                                        'text': txt,
                                        'task':task_txt,
                                        'chatid':chat_id,
                                        'keyboard':Const.mainInKeyBoard,
                                        'photo': photo,
                                        'id':_id
                                    })
                                    bot.delete_message(chat_id=chat_id, message_id=message_id,caption=txt, photo=photo)
                                else:
                                    bot.sendMessage(chat_id=chat_id, text='blah blah')                                  
                    elif update.message.photo:
                        pid = update.message.photo[-1].file_id
                        #check if the photo has caption
                        if update.message.caption:
                            text = update.message.caption + " \n        💙 🌹 💙"
                            bot.send_photo(chat_id=chat_id,caption=text , photo=pid) 
                        #if the photo has no caption send a simple message      
                        else:
                            bot.send_photo(chat_id=chat_id,caption="This is a nice photo!" , photo=pid)

                    else: #update.message.text:
                        pass
                        #text = update.message.text + " 😍"
                        #bot.sendMessage(chat_id=chat_id, text=text)
                    #else:
                        #bot.sendMessage(chat_id=chat_id, text="I can not underestand this !!")
                #CallbackQueryHandler        
                if update.callback_query:
                    handle_callbacks(callback=update.callback_query)
                               
            else:
                print("No update")
    except Exception as e:
        print(str(e))
    return 'ok'