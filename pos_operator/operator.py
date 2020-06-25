from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from pymongo import MongoClient
import re

Builder.load_file("pos_operator/operatorsys.kv")


class OperatorScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(OperatorScreen, self).__init__(**kwargs)
        client = MongoClient()
        self.db = client.silverpos
        self.stocks = self.db.stocks

        self.cart = []
        self.quantity = []
        self.total = 0.00

    def update_purchases(self):
        p_code = self.ids.code_inp.text
        products_container = self.ids.products

        target_code = self.stocks.find_one({"product_code":p_code})
        if not target_code:
            pass
        else:
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={"top": 1})

            code = Label(text=p_code, size_hint_x=0.25, color=(0.4, 0.5, 0.6, 1))
            name = Label(text=target_code["product_name"], size_hint_x=0.25, color=(0.4, 0.5, 0.6, 1))
            qty = Label(text="1", size_hint_x=0.1, color=(0.4, 0.5, 0.6, 1))
            disc = Label(text="0.00", size_hint_x=0.1, color=(0.4, 0.5, 0.6, 1))
            price = Label(text=target_code["product_price"], size_hint_x=0.1, color=(0.4, 0.5, 0.6, 1))
            total = Label(text="0.00", size_hint_x=0.2, color=(0.4, 0.5, 0.6, 1))

            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

            products_container.add_widget(details)

            # Update preview
            p_name = name.text

            p_price = float(price.text)
            p_qty = str(1)
            self.total += p_price
            purchase_total = f"`\n\nTotal\t\t\t\t\t\t\t\t{str(self.total)}"
            self.ids.cur_product.text = p_name
            self.ids.cur_price.text = str(p_price)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find("`")
            if _prev > 0:
                prev_text = prev_text[:_prev]

            p_target = -1
            for i, c in enumerate(self.cart):
                if c == p_code:
                    p_target = i

            if p_target >= 0:
                p_qty = self.quantity[p_target] + 1
                self.quantity[p_target] = p_qty
                expr = "%s\t\tx\d\t"%(p_name)
                rexpr = p_name+"\t\tx"+str(p_qty)+"\t"
                new_text = re.sub(expr, rexpr, prev_text) + purchase_total
                preview.text = new_text
            else:
                self.cart.append(p_code)
                self.quantity.append(1)
                new_preview = "\n".join([prev_text, p_name+"\t\tx"+p_qty+"\t\t"+str(p_price), purchase_total])
                preview.text = new_preview

            self.ids.qty_inp.text = str(p_qty)
            self.ids.disc_inp.text = "0.00"
            self.ids.disc_perc_inp.text = "0"
            self.ids.vat_inp.text = "15%"
            self.ids.price_in.text = str(p_price)
            self.ids.total_inp.text = str(p_price)

    def logout(self):
        self.parent.parent.current = "login_screen"


class OperatorSys(App):
    def build(self):
        return OperatorScreen()


if __name__ == '__main__':
    OperatorSys().run()
