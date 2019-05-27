from modules import mongo

staff = mongo.staff


class StaffModel:
    def __init__(self, data):
        data = data or {}
        for k, v in data.items():
            setattr(self, k, v)

    def to_json(self):
        return self.__dict__

    def save(self):
        pass

    def update(self, status, value, duration=0):
        pass

    @staticmethod
    def check_for_no_conflicts(userid):
        pass

    @staticmethod
    def find_one(userid):
        pass

    @staticmethod
    def delete_one(userid):
        staff.remove({'id': userid})

    @staticmethod
    def get_staffs():
        pass