from modules import bot
from modules.Consts.main import Const
from modules.message.utils import Utils
from models.message import MessageModel
from models.task import TaskModel

peopleList = [
    {
        "name": "Nasrin",
        "tid": 499850947
    },
    {
        "name": "Fatima",
        "tid": 462737129
    },
    {
        "name": "KbotMasteresses",
        "tid": -1001484208668
    }    
]
def handle_callbacks(callback):
    #callback = update.callback_query
    if callback.message.photo:
        txt = callback.message.caption
    else:
        txt = callback.message.text
    print(callback.message.message_id)
    #chat_id = callback.from_user.id
    chat_id = callback.message.chat.id
    print('printing user_id')
    print (callback.message.chat.id)
    message_id = callback.message.message_id
    
    selected_btn = callback.data
    print(selected_btn)
    args = str(selected_btn).strip().split('_')
    print(args)
    selected_callback = args[0]
    if selected_callback in ['reassign']:
        msg = MessageModel.get_one(args={'message_id': message_id, 'chatid': chat_id}, filters={'_id': 0})
        print(msg)
        if msg:
            sender_name = callback.from_user.full_name
            t_selected = args[2]
            _task = MessageModel.get_one(args={'id': msg.get('id'), 'chatid': chat_id}, filters={'_id': 0})
            
            #t = '{0} {1} {2} {3} {4} {5} {6} {7}'.format('Task: ', txt, '\n', 'By: ', #sender_name,'\n','To: ', t_selected)
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2])]
            t = 'Task: {task}\nIssuer: {sender} \n Reassigned: {p}(by {u})'.format(task=msg.get('task', ''), sender=_task.get('issuer', sender_name), p=p_lst[0]['name'] if p_lst else 'No Name', u=sender_name)
            _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
            if chat_id<0 or chat_id>0:
                if callback.message.photo:
                    bot.editMessageCaption(chat_id=chat_id, caption=t, message_id = message_id, parse_mode='Markdown', reply_markup=_key)
                else:
                    bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id, parse_mode='Markdown', reply_markup=_key)
    elif selected_callback in ['department']:
        msg = MessageModel.get_one(args={'message_id': message_id, 'chatid': chat_id}, filters={'_id': 0})
        if msg:
            sender_name = callback.from_user.full_name
            t = 'Task: {task}\nIssuer: {sender} \n'.format(task=msg.get('task', ''), sender=sender_name)
            _keyRA=[]
            peopleKey = []
            for people in peopleList:
                    peopleKey.append({'text': u'{name}'.format(name=people.get('name')), 'callback_data': 'people_{department}_{tid}'.format(department=args[1], tid=people.get('tid'))})
            _key2 = Utils.create_inlinekeyboard(buttons=peopleKey, cols=2)  
        
            if callback.message.photo:
                print ('hey')
                #menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, #resize_keyboard=True)
                #message_id = callback.message.message_id
                bot.editMessageCaption(chat_id=chat_id, caption=t, message_id = message_id, parse_mode='Markdown', reply_markup=_key2) 
            else:
                bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id,parse_mode='Markdown', reply_markup=_key2) 
    elif selected_callback in ['people']:
        msg = MessageModel.get_one(args={'message_id': message_id, 'chatid': chat_id}, filters={'_id': 0})
        if msg:
            #_task = MessageModel.get_one(args={'id': msg.get('id'), 'chatid': chat_id}, 
            #filters={'_id': 0})
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2])]
            sender_name = callback.from_user.full_name
            t = 'Task: {task}\nIssuer: {sender} \nAssigned to: {person}'.format(task=msg.get('task', ''), sender=sender_name, person=p_lst[0]['name'] if p_lst else 'No Name')
            people_tid = int(args[2])
            _keyRA = []
            for k2 in Const.approvalInKeyBoard:    
                _keyRA.append({
                    'text': k2.get('text'),
                    'callback_data': k2.get('callback_data').format(dep=' office ', tid=people_tid)
                })
                _key2 = Utils.create_inlinekeyboard(buttons=_keyRA, cols=2)  
            if callback.message.photo:
                #message_id = callback.message.message_id
                res = bot.send_photo(chat_id=people_tid, caption=t, photo=callback.message.photo[-1].file_id, parse_mode='Markdown', reply_markup=_key2) 
                MessageModel.save_one({
                                        'message_id': res.message_id,
                                        'text': t,
                                        'task':msg.get('task', ''),
                                        'chatid':people_tid,
                                        'keyboard':Const.approvalInKeyBoard,
                                        'photo': callback.message.photo[-1].file_id,
                                        'id': msg.get('id')
                                    })
            else:
                res = bot.sendMessage(chat_id=people_tid, text=t, parse_mode='Markdown', reply_markup=_key2) 
                MessageModel.save_one({
                                        'message_id': res.message_id,
                                        'text': t,
                                        'task':msg.get('task', ''),
                                        'chatid':people_tid,
                                        'keyboard':Const.approvalInKeyBoard,
                                        'photo': '',
                                        'id': msg.get('id')
                                    })
        pass
    else:
        pass
