from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from admin.admin import AdminScreen
from login.login import LoginScreen
from pos_operator.operator import OperatorScreen


class MainScreen(BoxLayout):
    login_widget = LoginScreen()
    admin_widget = AdminScreen()
    operator_widget = OperatorScreen()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.ids.login_screen.add_widget(self.login_widget)
        self.ids.admin_screen.add_widget(self.admin_widget)
        self.ids.operator_screen.add_widget(self.operator_widget)


class MainApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MainApp().run()
