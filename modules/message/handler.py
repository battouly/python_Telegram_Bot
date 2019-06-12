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
    chat_id = callback.message.chat.id
    print (callback.message.chat.id)
    message_id = callback.message.message_id
    selected_btn = callback.data
    selected_btn = str(selected_btn).strip()
    
    args = str(selected_btn).strip().split('_')
    selected_callback = args[0]
    msg = MessageModel.get_one(args={'message_id': message_id}, filters={'_id': 0})
    if msg:
        print('I found a message')
        _task = TaskModel.get_one(args={'id': msg.get('id'), 'message_id': msg.get('message_id')}, filters={'_id': 0})
        sender_name = callback.from_user.full_name
        msg_txt = msg.get('text')
        print("selected_callback:")
        print(selected_btn)
        if selected_callback in ['reassign']:
            print('hey under reassign')
            sender_name = callback.from_user.full_name
            t_selected = args[2]
            msg_txt = msg.get('text')
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2])]
            t = '{txt} \n Reassigned: {p}(by {u})'.format(txt=msg_txt, p=p_lst[0]['name'] if p_lst else 'No Name', u=sender_name)
            _key = Utils.create_inlinekeyboard(buttons=Const.mainInKeyBoard, cols=2)
            #if chat_id<0 or chat_id>0:
            print("starting a task ;") 
            if callback.message.photo:
                res = bot.editMessageCaption(chat_id=chat_id, caption=t, message_id = message_id, parse_mode='Markdown', reply_markup=_key)
            else:
                res = bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id, parse_mode='Markdown', reply_markup=_key)
            #bot.delete_message(chat_id=chat_id, text=t) 
                  
            MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t}}) 
        
        elif selected_callback in ['department']:
            sender_name = callback.from_user.full_name
            _keyRA=[]
            peopleKey = []
            for people in peopleList:
                    peopleKey.append({'text': u'{name}'.format(name=people.get('name')), 'callback_data': 'people_{department}_{tid}'.format(department=args[1], tid=people.get('tid'))})
            _key2 = Utils.create_inlinekeyboard(buttons=peopleKey, cols=2)  
            print('Hey printing the depart: ',args[1])
            if callback.message.photo:
                res1 = bot.editMessageCaption(chat_id=chat_id, caption=msg.get('text'), message_id = message_id, parse_mode='Markdown', reply_markup=_key2) 
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'department': args[1], 'message_id': res1.message_id}})                 
            else:
                res1 = bot.editMessageText(chat_id=chat_id, text=msg.get('text'), message_id = message_id,parse_mode='Markdown', reply_markup=_key2)
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'department': args[1], 'message_id': res1.message_id}})                  
        
        elif selected_callback in ['people']:
            msg_txt = msg.get('text')
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2])]
            sender_name = callback.from_user.full_name
            t = '{txt} \nAssigned to: {person}(by {sender})'.format(txt=msg_txt, person=p_lst[0]['name'] if p_lst else 'No Name', sender=sender_name)
            people_tid = int(args[2])

            #task level inline keyboard 
            _keyTL=[]
            klevels = Const.task_levelInKeyBoard
            for level in klevels:
                _keyTL.append({
                    'text': level.get('text'),
                    'callback_data': level.get('callback_data').format(dep=args[1], tid=people_tid)
                })    
            _key3 = Utils.create_inlinekeyboard(buttons=_keyTL, cols=2)            
            print ('this is the: ', people_tid)
            if callback.message.photo:
                res2 = bot.editMessageCaption(chat_id=chat_id, message_id = message_id, caption=t, photo=callback.message.photo[-1].file_id, parse_mode='Markdown', reply_markup=_key3)
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t}}) 
                MessageModel.save_one({
                                        'message_id': res2.message_id,
                                        'text': t,
                                        'task':msg.get('task', ''),
                                        'chatid':people_tid,
                                        'keyboard':Const.approvalInKeyBoard,
                                        'photo': callback.message.photo[-1].file_id,
                                        'id': msg.get('id')
                                    })
            else:
                res2 = bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id,  parse_mode='Markdown', reply_markup=_key3) 
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t}}) 
                MessageModel.save_one({
                                        'message_id': res2.message_id,
                                        'text': t,
                                        'task':msg.get('task', ''),
                                        'chatid':people_tid,
                                        'keyboard':Const.approvalInKeyBoard,
                                        'photo': '',
                                        'id': msg.get('id')
                                    })
            #bot.delete_message(chat_id=chat_id, message_id=message_id)
            print (" I am done with people")
            
        elif selected_callback in ['asap']:          
            print ("I'm in asap")
            print (selected_callback)
            print(args)
            msg_txt = msg.get('text')
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2]) ]
            sender_name = callback.from_user.full_name
            pn = p_lst[0]['name'] if p_lst else 'No Name'
            print (msg_txt)
            t = '{txt} \nLevel: {level}'.format(txt=msg_txt,level='asap')           
            people_tid = int(args[2])
            _keyRA = []
            for k2 in Const.approvalInKeyBoard:    
                _keyRA.append({
                    'text': k2.get('text'),
                    'callback_data': k2.get('callback_data').format(dep=args[1], tid=people_tid)
                })
                _key2 = Utils.create_inlinekeyboard(buttons=_keyRA, cols=2)  
            if callback.message.photo:
                res2 = bot.send_photo(chat_id=people_tid, caption=t, photo=callback.message.photo[-1].file_id, parse_mode='Markdown', reply_markup=_key2)
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t, 'chatid': people_tid,'message_id': res2.message_id}})
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'level': 'asap', 'message_id': res2.message_id}})               
            else:
                res2 = bot.sendMessage(chat_id=people_tid, text=t, parse_mode='Markdown', reply_markup=_key2) 
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t, 'chatid': people_tid,'message_id': res2.message_id}}) 
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'level': 'asap', 'message_id': res2.message_id}})               
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            
        elif selected_callback in ['urgent']:
            print ("I'm in urgent")
            print(args)
            msg_txt = msg.get('text')
            p_lst = [x for x in peopleList if x.get('tid') == int(args[2]) ]
            sender_name = callback.from_user.full_name
            pn = p_lst[0]['name'] if p_lst else 'No Name'
            t = '{txt} \nLevel: {level}'.format(txt=msg_txt,level='asap')           
            people_tid = int(args[2])
            _keyRA = []
            for k2 in Const.approvalInKeyBoard:    
                _keyRA.append({
                    'text': k2.get('text'),
                    'callback_data': k2.get('callback_data').format(dep=args[1], tid=people_tid)
                })
                _key2 = Utils.create_inlinekeyboard(buttons=_keyRA, cols=2)  
            if callback.message.photo:
                res2 = bot.send_photo(chat_id=people_tid, caption=t, photo=callback.message.photo[-1].file_id, parse_mode='Markdown', reply_markup=_key2)
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t, 'chatid': people_tid,'message_id': res2.message_id}}) 
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'level': 'urgent', 'message_id': res2.message_id}}) 
                #print ('res2.message_id: ',res2.message_id)
            else:
                res2 = bot.sendMessage(chat_id=people_tid, text=t, parse_mode='Markdown', reply_markup=_key2) 
                MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t, 'chatid': people_tid,'message_id': res2.message_id}}) 
                TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'level': 'urgent', 'message_id': res2.message_id}}) 
                #print ('res2.message_id: ',res2.message_id)                
            bot.delete_message(chat_id=chat_id, message_id=message_id)

        elif selected_callback in ['done']:
            t = '{txt} \n\n Done! ✅ \n by {u}'.format(txt=msg_txt, u=sender_name)
            check=TaskModel.get_one(args={'id': msg.get('id')},filters={'issuer_id': 1})
            sender_id = check["issuer_id"]            
            if callback.message.photo:
                pid = callback.message.photo[-1].file_id
                res = bot.editMessageCaption(chat_id=chat_id, caption=t, message_id = message_id)
                bot.send_photo(chat_id=sender_id, caption=t, photo=pid)
            else:
                res = bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id)
                bot.sendMessage(chat_id=sender_id, text=t)
            MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t}}) 
            TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'status': 'Done', 'message_id': res.message_id}})
            #bot.sendMessage(chat_id=update.message.from_user.full_name, text=t) 

        elif selected_callback in ['reject']:
            t = '{txt} \n\n Rejected! ❌ \n by {u}'.format(txt=msg_txt, u=sender_name)
            check=TaskModel.get_one(args={'id': msg.get('id')},filters={'issuer_id': 1})
            sender_id = check["issuer_id"]
            if callback.message.photo:
                pid = callback.message.photo[-1].file_id
                try:
                    res = bot.editMessageCaption(chat_id=chat_id, caption=t, message_id = message_id)
                    #print ('issuer_id: ',sender_id)
                    bot.send_photo(chat_id=sender_id, caption=t, photo=pid)
                except Exception as err:
                    print('[Error in edit caption reject msg]: '+ str(err))
            else:
                try:
                    res = bot.editMessageText(chat_id=chat_id, text=t, message_id = message_id)
                    bot.sendMessage(chat_id=sender_id, text=t)
                except Exception as err2:
                    print('[Error in edit text reject msg]: '+ str(err2))
            MessageModel.update_message(args={'message_id': message_id,'id': msg.get('id')}, set_query={'$set':{'text': t}}) 
            TaskModel.update_task(args={'id': msg.get('id')}, set_query={'$set':{'status': 'Rejected', 'message_id': res.message_id}})             
        else:
            pass       
