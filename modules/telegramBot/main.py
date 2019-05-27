import telegram
#import josn
import logging

from flask import request, Blueprint

from modules import (bot)
from modules.message.utils import Utils
from modules.message.handler import handle_callbacks
from modules.Consts.main import Const
#from telegram import ReplyKeyboardMarkup

main = Blueprint('main', __name__)

@main.route('/', methods=['POST'])
def webhook_handler():
    #print('im hereeee')
    try:
        if request.method == "POST":
            # retrieve the message in JSON and transform it to Telegram object
            update = telegram.Update.de_json(request.get_json(force=True),bot)
            if bool(update):
                if update.message:
                    chat_id = update.message.chat.id 
                    #commands for displaying inlinekeyboard
                    print (chat_id)
                    if update.message.entities:
                        for entity in update.message.entities:
                            if entity.type == 'bot_command':
                                c_offset = entity.__dict__.get('offset')
                                c_length = entity.__dict__.get('length')
                                cmnd = update.message.text[c_offset+1: c_offset+ c_length]
                                txt = update.message.text[c_offset+ c_length:]
                                if cmnd == 'task':
                                    _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
                                    bot.sendMessage(chat_id=chat_id, text=txt or ' Do nothing ' ,parse_mode='Markdown', reply_markup=_key)   
                                else:
                                    bot.sendMessage(chat_id=chat_id, text='blah blah')               
                    elif update.message.caption_entities:
                        for entity in update.message.caption_entities:
                            photo = update.message.photo[-1].file_id
                            if entity.type == 'bot_command':
                                print(update.message.caption)
                                c_offset = entity.__dict__.get('offset')
                                c_length = entity.__dict__.get('length')
                                cmnd = update.message.caption[c_offset+1: c_offset+ c_length]
                                txt = update.message.caption[c_offset+ c_length:]
                                if cmnd == 'task':
                                    _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
                                    res = bot.send_photo(chat_id=chat_id, caption=txt or ' Do nothing ' ,
                                    photo=photo, parse_mode='Markdown', reply_markup=_key) 
                                    print(res.message_id)  
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