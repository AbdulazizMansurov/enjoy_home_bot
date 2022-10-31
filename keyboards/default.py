from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import bot
from parser import *

def show_main_menu():
    mrkup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Каталог")
    mrkup.add(btn)
    return mrkup

def show_categories(data:dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for category in data.keys():
        btn = InlineKeyboardButton(category, callback_data=category)
        markup.add(btn)
    return markup

def show_products(category, page):
    markup = InlineKeyboardMarkup()
    offset = 0 if page == 1 else (page - 1) * 9
    products = give_products_by_cat(category, offset=offset)
    for product_name, product_info in products.items():
        markup.add(InlineKeyboardButton(product_name, callback_data=f"product|{product_info[0]}"))
    previous_page = InlineKeyboardButton("⏮", callback_data=f"previous_page|{page}")
    n_page = InlineKeyboardButton(page, callback_data=f"page|{page}")
    next_page = InlineKeyboardButton("⏭", callback_data=f"next_page|{page}")
    markup.row(previous_page, n_page, next_page)
    markup.add(InlineKeyboardButton("Назад", callback_data=f"back_to_cat"))
    return markup

def back_categories():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Назад", callback_data=f"back_to_cat"))

def order_product():
    btn_1 = InlineKeyboardButton("Заказать", callback_data="order")
    btn_2 = InlineKeyboardButton("Назад", callback_data="back_to_products")
    return InlineKeyboardMarkup().row(btn_1, btn_2)

def order_product_sure():
    btn_1 = InlineKeyboardButton("Да", callback_data="sure")
    btn_2 = InlineKeyboardButton("Нет. Вернуться к продуктам", callback_data="back_to_products")
    return InlineKeyboardMarkup().row(btn_1, btn_2)
