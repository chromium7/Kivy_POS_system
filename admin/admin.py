from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK
from pymongo import MongoClient
from collections import OrderedDict
from utils.datatable import DataTable
from datetime import datetime
import hashlib
import pandas as pd
import matplotlib.pyplot as plt


# SETTING UP DATABASE IN MONGO
# restore database in mongodb
# in command prompt mongodb directory run mongod
# mongorestore -d silverpos --drop C:/Desktop/silverpos
# mongo
# use silverpos

Builder.load_file("admin/adminsys.kv")


class Notify(ModalView):
    def __init__(self, **kwargs):
        super(Notify, self).__init__(**kwargs)

        self.size_hint = (0.3, 0.5)


class AdminScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        client = MongoClient()
        db = client.silverpos
        self.users = db.users
        self.products = db.stocks
        self.notify = Notify()

        product_code = []
        product_name = []
        spinvals = []
        for product in self.products.find():
            product_code.append(product["product_code"])
            name = product["product_name"]
            if len(name) > 30:
                name = name[:30] + "..."
            product_name.append(name)

        for i in range(len(product_code)):
            line = " | ".join([product_code[i], product_name[i]])
            spinvals.append(line)

        self.ids.target_product.values = spinvals

        # Display users
        content = self.ids.screen_contents
        users = self.get_users()
        users_table = DataTable(table=users)
        content.add_widget(users_table)

        # Display products
        product_content = self.ids.screen_product_contents
        products = self.get_products()
        products_table = DataTable(table=products)
        product_content.add_widget(products_table)

    def kill_switch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_user_fields(self):
        target = self.ids.ops_field
        target.clear_widgets()
        crud_first = TextInput(hint_text="First Name", multiline=False)
        crud_last = TextInput(hint_text="Last Name", multiline=False)
        crud_user = TextInput(hint_text="Username", multiline=False)
        crud_password = TextInput(hint_text="Password", multiline=False)
        crud_des = Spinner(text="Operator", values=["Operator", "Administrator"], background_color=(0.4, 0.5, 0.6, 1),
                           background_normal="")
        crud_submit = Button(text="Add", size_hint_x=None, width=100, on_release=lambda x:
        self.add_user(crud_first.text, crud_last.text, crud_user.text, crud_password.text, crud_des.text),
                             background_color=(0.4, 0.5, 0.6, 1), background_normal="")

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def add_user(self, first, last, user, password, dest):
        content = self.ids.screen_contents
        content.clear_widgets()
        password = hashlib.sha256(password.encode()).hexdigest()
        if first == "" or last == "" or user == "" or password == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All Fields Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)

        else:
            self.users.insert_one({"first_name": first, "last_name": last, "user_name": user, "password": password,
                                   "designation": dest, "date": datetime.now()})

        users = self.get_users()
        users_table = DataTable(table=users)
        content.add_widget(users_table)

    def update_user_fields(self):
        target = self.ids.ops_field
        target.clear_widgets()
        crud_first = TextInput(hint_text="First Name", multiline=False)
        crud_last = TextInput(hint_text="Last Name", multiline=False)
        crud_user = TextInput(hint_text="Username", multiline=False)
        crud_password = TextInput(hint_text="Password", multiline=False)
        crud_des = Spinner(text="Operator", values=["Operator", "Administrator"], background_color=(0.4, 0.5, 0.6, 1),
                           background_normal="")
        crud_submit = Button(text="Update", size_hint_x=None, width=100, on_release=lambda x:
        self.update_user(crud_first.text, crud_last.text, crud_user.text, crud_password.text, crud_des.text),
                             background_color=(0.4, 0.5, 0.6, 1), background_normal="")

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def update_user(self, first, last, user, password, dest):
        content = self.ids.screen_contents
        content.clear_widgets()
        password = hashlib.sha256(password.encode()).hexdigest()

        if user == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Username Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_user = self.users.find_one({"user_name": user})
            if target_user == None:
                self.notify.add_widget(Label(text="[color=#FF0000][b]Invalid Username[/b][/color]", markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)

            else:
                if first == "":
                    first = target_user["first_name"]
                if last == "":
                    last = target_user["last_name"]
                if password == "":
                    password = target_user["password"]

                self.users.update_one({"user_name": user},
                                      {"$set": {"first_name": first, "last_name": last, "user_name": user,
                                                "password": password, "designation": dest,
                                                "date": datetime.now()}})

        users = self.get_users()
        users_table = DataTable(table=users)
        content.add_widget(users_table)

    def remove_user_fields(self):
        target = self.ids.ops_field
        target.clear_widgets()
        crud_user = TextInput(hint_text="Username", multiline=False)
        crud_submit = Button(text="Remove", size_hint_x=None, width=100, on_release=lambda x:
        self.remove_user(crud_user.text),
                             background_color=(0.4, 0.5, 0.6, 1), background_normal="")

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_user(self, username):
        content = self.ids.screen_contents
        content.clear_widgets()

        if username == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Username Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_username = self.users.find_one({"user_name": username})
            if target_username == None:
                self.notify.add_widget(Label(text="[color=#FF0000][b]Invalid Username[/b][/color]", markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                self.users.delete_one({"user_name": username})

        users = self.get_users()
        users_table = DataTable(table=users)
        content.add_widget(users_table)

    def add_product_fields(self):
        target = self.ids.ops_field_p
        target.clear_widgets()

        crud_code = TextInput(hint_text="Product Code", multiline=False)
        crud_name = TextInput(hint_text="Product Name", multiline=False)
        crud_weight = TextInput(hint_text="Product Weight", multiline=False)
        crud_stock = TextInput(hint_text="Product In Stock", multiline=False)
        crud_sold = TextInput(hint_text="Product Sold", multiline=False)
        crud_order = TextInput(hint_text="Product Order", multiline=False)
        crud_purchase = TextInput(hint_text="Product Last Purchase", multiline=False)

        crud_submit = Button(text="Add", size_hint_x=None, width=100, on_release=lambda x:
        self.add_product(crud_code.text, crud_name.text, crud_weight.text, crud_stock.text, crud_sold.text,
                         crud_order.text, crud_purchase.text), background_color=(0.4, 0.5, 0.6, 1),
                             background_normal="")

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def add_product(self, code, name, weight, stock, sold, order, purchase):
        content = self.ids.screen_product_contents
        content.clear_widgets()
        if code == "" or name == "" or weight == "" or stock == "" or order == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All Fields Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)

        else:
            self.products.insert_one(
                {"product_code": code, "product_name": name, "product_weight": weight, "in_stock": stock,
                 "sold": sold, "order": order, "last_purchase": purchase})

        prods = self.get_products()
        prods_table = DataTable(table=prods)
        content.add_widget(prods_table)

    def update_product_fields(self):
        target = self.ids.ops_field_p
        target.clear_widgets()

        crud_code = TextInput(hint_text="Product Code", multiline=False)
        crud_name = TextInput(hint_text="Product Name", multiline=False)
        crud_weight = TextInput(hint_text="Product Weight", multiline=False)
        crud_stock = TextInput(hint_text="Product In Stock", multiline=False)
        crud_sold = TextInput(hint_text="Product Sold", multiline=False)
        crud_order = TextInput(hint_text="Product Order", multiline=False)
        crud_purchase = TextInput(hint_text="Product Last Purchase", multiline=False)

        crud_update = Button(text="Update", size_hint_x=None, width=100, on_release=lambda x:
        self.update_product(crud_code.text, crud_name.text, crud_weight.text, crud_stock.text, crud_sold.text,
                            crud_order.text, crud_purchase.text), background_color=(0.4, 0.5, 0.6, 1),
                             background_normal="")

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_update)

    def update_product(self, code, name, weight, stock, sold, order, purchase):
        content = self.ids.screen_product_contents
        content.clear_widgets()

        if code == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Product Code Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_code = self.products.find_one({"product_code": code})
            if target_code == None:
                self.notify.add_widget(Label(text="[color=#FF0000][b]Invalid Code[/b][/color]", markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                if name == "":
                    name = target_code["product_name"]
                if weight == "":
                    weight = target_code["product_weight"]
                if stock == "":
                    stock = target_code["in_stock"]
                if sold == "":
                    sold = target_code["sold"]
                if order == "":
                    order = target_code["order"]
                if purchase == "":
                    purchase = target_code["last_purchase"]

                self.products.update_one({"product_code": code}, {"$set":
                                                                      {"product_code": code, "product_name": name,
                                                                       "product_weight": weight, "in_stock": stock,
                                                                       "sold": sold, "order": order,
                                                                       "last_purchase": purchase}})

        prods = self.get_products()
        prods_table = DataTable(table=prods)
        content.add_widget(prods_table)

    def remove_product_fields(self):
        target = self.ids.ops_field_p
        target.clear_widgets()
        crud_code = TextInput(hint_text="Product Code", multiline=False)
        crud_submit = Button(text="Remove", size_hint_x=None, width=100, on_release=lambda x:
        self.remove_product(crud_code.text),
                             background_color=(0.4, 0.5, 0.6, 1), background_normal="")

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_product(self, code):
        content = self.ids.screen_product_contents
        content.clear_widgets()
        if code == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Product Code Required[/b][/color]", markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_code = self.products.find_one({"product_code": code})
            if target_code == None:
                self.notify.add_widget(Label(text="[color=#FF0000][b]Invalid Product Code[/b][/color]", markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                self.products.delete_one({"product_code": code})

        prods = self.get_products()
        prods_table = DataTable(table=prods)
        content.add_widget(prods_table)

    def change_screen(self, instance):
        if instance.text == "Manage Products":
            self.ids.screen_manager.transition = NoTransition()
            self.ids.screen_manager.current = "screen_product_content"
        elif instance.text == "Manage Users":
            self.ids.screen_manager.transition = NoTransition()
            self.ids.screen_manager.current = "screen_content"
        else:
            self.ids.screen_manager.transition = NoTransition()
            self.ids.screen_manager.current = "screen_analysis"

    def get_users(self):
        client = MongoClient()
        db = client.silverpos
        users = db.users
        _users = OrderedDict(
            first_names={},
            last_names={},
            user_names={},
            passwords={},
            designations={}
        )
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []
        for user in users.find():
            first_names.append(user["first_name"])
            last_names.append(user["last_name"])
            user_names.append(user["user_name"])
            pwd = user["password"]
            if len(pwd) > 10:
                pwd = pwd[:10] + "..."
            passwords.append(pwd)
            designations.append(user["designation"])
        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users["first_names"][idx] = first_names[idx]
            _users["last_names"][idx] = last_names[idx]
            _users["user_names"][idx] = user_names[idx]
            _users["passwords"][idx] = passwords[idx]
            _users["designations"][idx] = designations[idx]

            idx += 1

        return _users

    def get_products(self):
        client = MongoClient()
        db = client.silverpos
        stocks = db.stocks
        _stocks = OrderedDict(
            product_code={},
            product_name={},
            product_weight={},
            in_stock={},
            sold={},
            order={},
            last_purchase={}
        )
        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []
        for product in stocks.find():
            product_code.append(product["product_code"])
            name = product["product_name"]
            if len(name) > 10:
                name = name[:10] + "..."
            product_name.append(name)
            product_weight.append(product["product_weight"])
            in_stock.append(product["in_stock"])
            try:
                sold.append(product["sold"])
            except KeyError:
                sold.append("")
            try:
                order.append(product["order"])
            except KeyError:
                order.append("")
            try:
                last_purchase.append(product["last_purchase"])
            except KeyError:
                last_purchase.append("")
        products_length = len(product_code)
        idx = 0
        while idx < products_length:
            _stocks["product_code"][idx] = product_code[idx]
            _stocks["product_name"][idx] = product_name[idx]
            _stocks["product_weight"][idx] = product_weight[idx]
            _stocks["in_stock"][idx] = in_stock[idx]
            _stocks["sold"][idx] = sold[idx]
            _stocks["order"][idx] = order[idx]
            _stocks["last_purchase"][idx] = last_purchase[idx]

            idx += 1

        return _stocks

    def view_stats(self):
        plt.cla()
        self.ids.analysis_res.clear_widgets()

        target_product = self.ids.target_product.text
        target = target_product[:target_product.find(" | ")]
        name = target_product[target_product.find(" | "):]

        df = pd.read_csv("admin/products_purchased.csv")
        purchases = []
        dates = []
        count = 0
        for i in range(len(df)):
            if str(df.Product_Code[i]) == target:
                purchases.append(df.Purchased[i])
                dates.append(count)
                count += 1
        plt.bar(dates, purchases, color="green", label=name)
        plt.ylabel("Total Purchases")
        plt.xlabel("Day")

        self.ids.analysis_res.add_widget(FCK(plt.gcf()))

    def logout(self):
        self.parent.parent.current = "login_screen"


class AdminSys(App):
    def build(self):
        return AdminScreen()


if __name__ == '__main__':
    AdminSys().run()
