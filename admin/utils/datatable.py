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
        super().__init__(**kwargs)

        products = table

        col_titles = [k for k in products.keys()]
        self.cols_len = len(col_titles)
        rows_len = len(products[col_titles[0]])
        table_data = []

        for t in col_titles:
            table_data.append({"text": str(t), "size_hint_y": None, "height": 50, "bcolor": (0.4, 0.5, 0.6, 1)})

        for i in range(rows_len):
            for j in col_titles:
                table_data.append({"text":str(products[j][i]), "size_hint_y": None, "height": 30, "bcolor": (0.4, 0.35, 0.45, 1)})

        self.ids.table_floor_layout.cols = self.cols_len
        self.ids.table_floor.data = table_data
