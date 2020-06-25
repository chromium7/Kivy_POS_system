from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pymongo import MongoClient
from collections import OrderedDict


Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: "CustomLabel"
        id: table_floor
        
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: None, 250
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            
<CustomLabel@Label>:
    bcolor: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')


class DataTable(BoxLayout):
    def __init__(self, table=None, **kwargs):
        super(DataTable, self).__init__(**kwargs)

        # products = self.get_products()
        products = table

        col_titles = [k for k in products.keys()]
        self.cols_len = len(col_titles)
        rows_len = len(products[col_titles[0]])
        table_data = []

        for t in col_titles:
            table_data.append({"text": str(t), "size_hint_y": None, "height": 50, "bcolor": (0.4, 0.5, 0.6, 1)})

        for i in range(rows_len):
            for j in col_titles:
                table_data.append({"text":str(products[j][i]), "size_hint_y": None, "height": 30, "bcolor": (0.4, 0.4, 0.5, 1)})

        self.ids.table_floor_layout.cols = self.cols_len
        self.ids.table_floor.data = table_data

    
#     def get_products(self):
#         client = MongoClient()
#         db = client.silverpos
#         stocks = db.stocks
#         _stocks = OrderedDict(
#             product_code={},
#             product_name={},
#             product_weight={},
#             in_stock={},
#             sold = {},
#             order={},
#             last_purchase={}
#         )
#         product_code = []
#         product_name = []
#         product_weight = []
#         in_stock = []
#         sold = []
#         order = []
#         last_purchase = []
#         for product in stocks.find():
#             product_code.append(product["product_code"])
#             product_name.append(product["product_name"])
#             product_weight.append(product["product_weight"])
#             in_stock.append(product["in_stock"])
#             sold.append(product["sold"])
#             order.append(product["order"])
#             last_purchase.append(product["last_purchase"])
#         products_length = len(product_code)
#         idx = 0
#         while idx < products_length:
#             _stocks["product_code"][idx] = product_code[idx]
#             _stocks["product_name"][idx] = product_name[idx]
#             _stocks["product_weight"][idx] = product_weight[idx]
#             _stocks["in_stock"][idx] = in_stock[idx]
#             _stocks["sold"][idx] = sold[idx]
#             _stocks["order"][idx] = order[idx]
#             _stocks["last_purchase"][idx] = last_purchase[idx]
#
#             idx += 1
#
#         return _stocks
#
#
# class DataTableSys(App):
#     def build(self):
#         return DataTable()
#
#
# if __name__ == '__main__':
#     DataTableSys().run()