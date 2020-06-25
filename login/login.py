from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from pymongo import MongoClient
import hashlib

Builder.load_file("login/mainsys.kv")


class LoginScreen(BoxLayout):
    user_field = ObjectProperty(None)
    pw_field = ObjectProperty(None)
    info = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def validate_user(self):
        client = MongoClient()
        db = client.silverpos
        users = db.users

        username = self.user_field.text.strip()
        password = self.pw_field.text.strip()

        if username == "" or password == "":
            self.info.text = "[color=#FF0000]Username and/ or password required[/color]"
        else:
            target_user = users.find_one({"user_name": username})
            if not target_user:
                self.info.text = "[color=#FF0000]Invalid username and/ or password[/color]"
            else:
                pw = hashlib.sha256(password.encode()).hexdigest()
                if pw == target_user["password"]:
                    des = target_user["designation"]
                    self.info.text = "[color=#00FF00]Logged in Successfully[/color]"
                    if des == "Administrator":
                        self.parent.parent.current = "admin_screen"
                    else:
                        self.parent.parent.parent.ids.operator_screen.children[0].ids.loggedin_user.text = username
                        self.parent.parent.current = "operator_screen"
                    self.user_field.text = ""
                    self.pw_field.text = ""
                    self.info.text = ""


class MainSys(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MainSys().run()