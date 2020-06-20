from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class LoginScreen(Screen):
    user_field = ObjectProperty(None)
    pw_field = ObjectProperty(None)
    info = ObjectProperty(None)

    def validate_user(self):
        username = self.user_field.text.strip()
        password = self.pw_field.text.strip()

        if username == "" or password == "":
            self.info.text = "[color=#FF0000]Username and/ or password required[/color]"
        else:
            if username == "admin" and password == "admin":
                self.info.text = "[color=#00FF00]Logged in Successfully[/color]"
            else:
                self.info.text = "[color=#FF0000]Invalid username and/ or password[/color]"


class ScreenManagement(ScreenManager):
    pass


class MainSys(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    MainSys().run()