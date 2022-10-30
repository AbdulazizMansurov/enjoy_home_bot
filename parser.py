import requests
from pprint import pprint
from config import link_of_site
from bs4 import BeautifulSoup

def get_categories():
    req = requests.get(link_of_site).text
    soup = BeautifulSoup(req, "html.parser")
    categories = soup.find("ul", class_="scf-ul")
    data = {
        "all categories": {

        }
    }
    s = 0
    for category in categories:
        try:
            name_of_category = category.get_text().split("\t")[0]
            link = "https://enjoyhome.ru" + category.find("a").get("href")
            data["all categories"][name_of_category] = {"link": link}
        except:
            pass

    return data

def get_product_from_categories(data):
    s = 1
    for name, link in data['all categories'].items():
        name = name
        link = link["link"].split("\t")[0]
        req = requests.get(link).text
        soup = BeautifulSoup(req, "html.parser")
        products = soup.find("div", class_="sc-items item-canvs_1")

        for product in products:
            try:
                product_text = product.find("div", class_="prod-txt").get_text().split("\n")
                product_name = str(product_text[1])
                product_price = str(product_text[2])
                product_link = link_of_site + product.get("href")
                product_image =product.find("span", class_="prod-i-bg").get("style").split("url")[1].split(";")[0]
                product_image = "https://enjoyhome.ru" + (product_image.split("(")[1].split(")")[0])
                data['all categories'][name][f"products{s}"] = {"product_id": s,
"product_name": product_name,
"product_link": product_link,
"product_price": product_price,
"product_image": product_image}
                s += 1
            except:
                pass


    return data

def give_products_by_cat(category: str, offset=0, limit=9):
    products_list = {}
    category = category
    categories = get_categories()
    data = get_product_from_categories(categories)['all categories'][category]
    s = 0
    for product_info in data.values():
        try:
            if s >= offset and len(products_list) < limit:
                products_name = product_info['product_name']
                product_id = product_info['product_id']
                product_photo = product_info['product_image']
                product_link = product_info["product_link"]
                product_price = product_info["product_price"]
                products_list[products_name] = [product_id, product_photo, product_link, product_price]
            s += 1
        except:
            pass
    return products_list

def give_product_by_id(category, product_id):
    product_info = give_products_by_cat(category)
    da = {}
    for product_name, product_all in product_info.items():
        if int(product_id) == product_all[0]:
            da["product_image"] = product_all[1]
            da["product_name"] = product_name
            da["product_link"] = product_all[2]
            da["product_price"] = product_all[3]
        else:
            pass
    return da
