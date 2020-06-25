from pymongo import MongoClient
import random

client = MongoClient()
db = client.silverpos
stocks = db.stocks


def purchase_products():
    codes = []
    for product in stocks.find():
        codes.append(product["product_code"])

        with open("products_purchased.csv", "w") as file:
            file.write("Product_Code,Purchased\n")

            for day in range(1, 31):
                for code in codes:
                    purchased = random.randint(0, 50)
                    line = ",".join([str(code), str(purchased)])
                    file.write(line+"\n")
    return len(codes)


if __name__ == '__main__':
    purchase_products()