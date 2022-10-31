from data.loader import bot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.default import *
from config import link_of_site, LINK_OF_ADMINS
from parser import *

@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Добро пожаловать в бота {message.from_user.first_name}", reply_markup=show_main_menu())

@bot.message_handler(func= lambda message: message.text=="Каталог")
def reaction_to_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вы не должны это увидеть", reply_markup=ReplyKeyboardRemove())
    bot.delete_message(chat_id, message.id+1)
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=show_categories(get_categories()["all categories"]))

@bot.callback_query_handler(func= lambda call: call.data in ('Все', 'Кровати', '11 MINUTES', 'Библиотеки', 'Диваны', 'Кухни',
'Свет ALCHEMY','Гардеробные', 'Свет', 'Столы', 'Стулья и кресла', 'Тумбы и консоли', 'Фурнитура', 'Банкетки и пуфы'))
def reaction_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    callback = call.data
    bot.delete_message(chat_id, call.message.id)
    bot.answer_callback_query(call.id, "Продукты подбираются подождите...")
    bot.send_message(chat_id, f"Продукты категории {callback}", reply_markup=show_products(callback, 1))

@bot.callback_query_handler(func=lambda call: "previous_page|" in call.data)
def reaction_to_previous_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    callback = call.message.text.split("Продукты категории ")[1]
    page = int(call.data.split("|")[1])
    bot.answer_callback_query(call.id, "Подождите, подбирается информация")
    try:
        if page > 1:
            bot.send_message(chat_id, call.message.text, reply_markup=show_products(callback, page-1))
            bot.delete_message(chat_id, call.message.id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: "next_page|" in call.data)
def reaction_to_previous_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    callback = call.message.text.split("Продукты категории ")[1]
    page = int(call.data.split("|")[1])
    bot.answer_callback_query(call.id, "Подождите, подбирается информация")
    try:
        bot.send_message(chat_id, call.message.text, reply_markup=show_products(callback, page+1))
        bot.delete_message(chat_id, call.message.id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == "back_to_cat")
def reaction_to_back_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=show_categories(get_categories()["all categories"]))

@bot.callback_query_handler(func= lambda call: "product|" in call.data)
def reaction_to_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = call.data.split("|")[1]
    category = call.message.text.split("Продукты категории ")[1]
    product_info = give_product_by_id(category, product_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_photo(chat_id, photo=product_info['product_image'], caption=f'''Категория: {category}\n
Продукт: 
<b>{product_info['product_name']}</b>\n
Цена: {product_info['product_price']};
<a href="{product_info['product_link']}">Подробная информация</a>
''', reply_markup=order_product())

@bot.callback_query_handler(func=lambda call: call.data=="order")
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, f"""Вы точно хотите заказать этот продукт?
{call.message.caption}""", reply_markup=order_product_sure())

@bot.callback_query_handler(func=lambda call: call.data=="sure")
def reaction_to_sure_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Ваш заказ отправлен. Спасибо что выбрали этот товар.Ждите ответ от нас.", reply_markup=back_categories())
    bot.send_message(LINK_OF_ADMINS, f"""<b>Заказ</b>\n
Заказчик: <b>{call.from_user.first_name}
@{call.from_user.username}</b>\n
Продукт:
{call.message.text.split("Вы точно хотите заказать этот продукт?")[1]}""")


@bot.callback_query_handler(func=lambda call: call.data == "back_to_products")
def reaction_to_back_products(call: CallbackQuery):
    chat_id = call.from_user.id
    try:
        category = call.message.caption.split("Категория: ")[1].split("\n\nПродукт:")[0]
    except:
        category = call.message.text.split("Категория: ")[1].split("\n\nПродукт:")[0]
    bot.delete_message(chat_id, call.message.id)
    bot.answer_callback_query(call.id, "Продукты подбираются подождите...")
    bot.send_message(chat_id, f"Продукты категории {category}", reply_markup=show_products(category, 1))


@bot.callback_query_handler(func=lambda call: "page|" in call.data)
def reaction_to_page(call: CallbackQuery):
    page = call.data.split("|")[1]
    bot.answer_callback_query(call.id, f"Вы сейчас в {page} сранице")
