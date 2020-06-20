from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from pymongo import MongoClient

# restore database in mongodb
# in command prompt run mongod
# mongorestore -d silverpos --drop C:/Desktop/silverpos
# mongo
# use silverpos


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

        client = MongoClient()
        db = client.silverpos
        users = db.users
        _users = dict()
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []
        for user in users.find():
            first_names.append(user["first_name"])
            last_names.append(user["last_name"])
            user_names.append(user["user_name"])
            passwords.append(user["password"])
            designations.append(user["designation"])
        print(designations)


class ScreenManagement(ScreenManager):
    pass


class AdminSys(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    AdminSys().run()