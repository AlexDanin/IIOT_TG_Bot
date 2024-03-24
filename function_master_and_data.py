# Тут я решил оставить все функции и переменную, которые не уникальны

from telebot import TeleBot
# from telegram.ext import Updater, CommandHandler
import json

TOKEN = '6971909537:AAGbRyjyE2WfLqLpBxZobDuLCo8iSjM21BY'
bot = TeleBot(TOKEN)

message_id = {0: [0, 0]}


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(login):
    with open('registered_users.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return str(login) in registered_users.keys()


def is_acreditation(login, passwd):
    with open('registered_users.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return passwd == registered_users[login]


def is_sign_in(chat_id):
    with open('sign_in_users_master.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return str(chat_id) in list(registered_users.keys())


def get_sign_in_user(chat_id):
    with open('sign_in_users_master.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return registered_users[str(chat_id)]


def add_user_log(chat_id, login):
    if not is_sign_in(chat_id):
        with open('sign_in_users_master.json', 'r', encoding='utf-8') as file:
            registered_users = json.load(file)

        registered_users[chat_id] = str(login)

        with open('sign_in_users_master.json', 'w', encoding='utf-8') as file:
            json.dump(registered_users, file, ensure_ascii=False)


def del_user_log(chat_id):
    if is_sign_in(chat_id):
        with open("sign_in_users_master.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)

        chat_id = str(chat_id)

        # Находим запись, которую нужно удалить (например, по ключу)
        if chat_id in data:
            del data[chat_id]

        # Сохраняем обновленные данные в файл
        with open("sign_in_users_master.json", "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)


# Функция для удаления сообщений
def del_message(chat_id):
    for i in message_id[chat_id]:
        try:
            bot.delete_message(chat_id, i)
        except Exception as e:
            print(e)
    message_id[chat_id].clear()


# Функция для добавления сообщений в список для удаления
def add_message(message):
    if message.chat.id not in message_id:
        message_id[message.chat.id] = []
    message_id[message.chat.id].append(message.id)


# Функция для отправки сообщения
def send_message(chat_id, message, **kwargs):
    m = bot.send_message(chat_id, message, **kwargs)
    add_message(m)


def get_car_reg_log(chat_id):
    with open('car_reg_log.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def add_car_reg_log(chat_id, **kwags):
    if kwags:
        registered_users = get_car_reg_log(chat_id)

        if str(chat_id) not in dict(registered_users).keys():
            registered_users[str(chat_id)] = kwags
        else:
            registered_users[str(chat_id)] = registered_users[str(chat_id)] | kwags

        with open('car_reg_log.json', 'w', encoding='utf-8') as file:
            json.dump(registered_users, file, ensure_ascii=False)


def del_car_reg_log(chat_id):
    with open('car_reg_log.json', 'r', encoding='utf-8') as file:
        reg_logs = json.load(file)

    chat_id = str(chat_id)

    if chat_id in reg_logs:
        del reg_logs[chat_id]

    with open('car_reg_log.json', 'w', encoding='utf-8') as file:
        json.dump(reg_logs, file, ensure_ascii=False)


def get_cars_reg():
    with open('data/Cars.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def save_car_reg_log(chat_id):
    with open('data/Cars.json', 'r', encoding='utf-8') as file:
        cars = json.load(file)

    car_reg_logs = get_car_reg_log(chat_id)[str(chat_id)]

    car_reg_logs["master"] = get_sign_in_user(chat_id)

    gosnum = car_reg_logs.pop('gosnum')

    if gosnum not in dict(cars).keys():
        cars[gosnum] = car_reg_logs
    else:
        cars[gosnum] = cars[gosnum] | car_reg_logs

    with open('data/Cars.json', 'w', encoding='utf-8') as file:
        json.dump(cars, file, ensure_ascii=False)

    del_car_reg_log(chat_id)


def form_text(chat_id, kwags):
    main_text = f"⚙️ <b>Добавление <u>устройств</u> в базу данных</b> \n"
    device_text = f"🆔<b>Укажите</b> <u>ID</u> устройства\n"
    name_text = f"🏢<b>Введите</b> <u>наименование компании</u>\n"
    gosnum_text = f"🚘<b>Введите</b> государственный <u>номер автомобиля</u>\n"
    brand_text = f"🚗 <b>Укажите</b> <u>марку автомобиля</u>\n"
    wheels_text = f"🛞 <b>Введите</b> количество <u>колёс</u> автомобиля\n"
    brandWs_text = f"🔄 <b>Укажите</b> <u>марку шин</u>\n"

    chat_id = str(chat_id)
    kwags = get_car_reg_log(chat_id)

    if chat_id in kwags:

        kwags = get_car_reg_log(chat_id)[chat_id]

        for key in get_car_reg_log(chat_id)[chat_id].keys():
            match key:
                case 'device':
                    device_text = f"🆔 <b>{kwags['device']}</b> <u>ID</u> устройства\n"
                case 'name':
                    name_text = f"🏢 <b>{kwags['name']}</b> <u>наименование компании</u>\n"
                case 'gosnum':
                    gosnum_text = f"🚘 <b>{kwags['gosnum']}</b> государственный <u>номер автомобиля</u>\n"
                case 'brand':
                    brand_text = f"🚗 <b>{kwags['brand']}</b> <u>марку автомобиля</u>\n"
                case 'wheels':
                    wheels_text = f"🛞 <b>{kwags['wheels']}</b> количество <u>колёс</u> автомобиля\n"
                case 'brandWs':
                    brandWs_text = f"🔄 <b>{kwags['brandWs']}</b> <u>марку шин</u>\n"

    return main_text + device_text + name_text + gosnum_text + brand_text + wheels_text + brandWs_text


# this is "tomuch"
def deleter_message(chat_id, message_id, count_del=1):
    if count_del < 0:
        del_list = range(0, count_del, -1)
    else:
        del_list = range(count_del)

    for i in del_list:
        try:
            bot.delete_message(chat_id, message_id - i)
        except Exception as error:
            continue
