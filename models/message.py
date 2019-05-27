from modules import mongo
#from helpers import async

import copy

messages = mongo.messages


class MessageModel:
    def __init__(self, data):
        data = data or {}
        for k, v in data.items():
            setattr(self, k, v)

    def to_json(self):
        return self.__dict__

    def save(self):
        try:
            res = messages.insert_one(copy.deepcopy(self.__dict__))
            return res.acknowledged
        except Exception as exc:
            print "[Message Model Error] Insert New Message:", exc.args
        return False

    @staticmethod
    def find_one(args):
        try:
            message = messages.find_one(args, {'_id': 0})
            if message:
                return message
            return {}
        except Exception as e:
            print '[Message Model Error] Find message: ' + str(e)
        return {}

    @staticmethod
    def get_all_msgid(args=None):
        try:
            ids = messages.find({}, {'_id': 0, 'message_id': 1})
            if ids:
                return list(ids)
            return []
        except Exception as e:
            print '[Message Model Error] Get message ids: ' + str(e)
        return []

    @staticmethod
    @async
    def delete_one(args):
        try:
            messages.remove(args)
        except Exception as e:
            print '[Message Model Error] Delete message: ' + str(e)
        pass