from modules import db

import copy

task = db.tasks


class TaskModel:
    def __init__(self, data):
        data = data or {}
        for k, v in data.items():
            setattr(self, k, v)

    def to_json(self):
        return self.__dict__

    def save(self):
        try:
            res = task.insert_one(copy.deepcopy(self.__dict__))
            return res.acknowledged
        except Exception as exc:
            print("[Task Model Error] Insert New Message:", exc.args) 
        return False

    @staticmethod
    def save_one(data):
        try:
            res = task.insert_one(data)
            return res.acknowledged
        except Exception as exc:
            print ("[Task Model Error] Insert New Message:", exc.args)
        return False

    @staticmethod
    def update_task(args, set_query):
        try:
            res = task.update_one(args, set_query, upsert=False)
            if res.acknowledged:
                return True
            return False
        except Exception as e:
            print ('[Task Model Error] Update task: ' + str(e))
        return False

    @staticmethod
    def get_one(args, filters):
        try:
            message = task.find_one(args, filters)
            if message:
                return message
            return {}
        except Exception as e:
            print ('[Task Model Error] Find message: ' + str(e))
        return {}

    @staticmethod
    def get_all(args, filters):
        try:
            ids = task.find(args, filters)
            if ids:
                return list(ids)
            return []
        except Exception as e:
            print ('[Task Model Error] Get message ids: ' + str(e))
        return []

    @staticmethod
    def delete_one(args):
        try:
            task.remove(args)
            return True
        except Exception as e:
            print ('[Task Model Error] Delete message: ' + str(e))
        return False