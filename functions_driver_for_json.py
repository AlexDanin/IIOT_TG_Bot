from telebot import TeleBot
import json

token = '6466418502:AAG6J0gJE04bQ4uNBpDlBKKp0s6uLzjFCkI'
bot = TeleBot(token)

message_id = {0: [0, 0]}


# Функция для проверки, зарегистрирован ли пользователь
def is_company(login):
    with open('data/Companies.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return str(login) in registered_users.values()


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(login, company):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login and i["Company"] == company:
                return True
        return False


def is_acreditation(passwd, login, company):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login and i["Company"] == company and i["Password"] == passwd:
                return True
        return False


def is_sign_in(chat_id):
    with open('sign_in_users_driver.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return str(chat_id) in list(registered_users.keys())


def get_sign_in_user(chat_id):
    with open('sign_in_users_driver.json', 'r') as file:
        registered_users = json.load(file)
        return registered_users[str(chat_id)]


def add_user_log(chat_id, login):
    if not is_sign_in(chat_id):
        with open('sign_in_users_driver.json', 'r') as file:
            registered_users = json.load(file)

        registered_users[chat_id] = str(login)

        with open('sign_in_users_driver.json', 'w', encoding='utf-8') as file:
            json.dump(registered_users, file, ensure_ascii=False)


def del_user_log(chat_id):
    if is_sign_in(chat_id):
        with open("sign_in_users_driver.json", "r") as json_file:
            data = json.load(json_file)

        chat_id = str(chat_id)

        # Находим запись, которую нужно удалить (например, по ключу)
        if chat_id in data:
            del data[chat_id]

        # Сохраняем обновленные данные в файл
        with open("sign_in_users_driver.json", "w") as json_file:
            json.dump(data, json_file)


# Функция для добавления сообщений в список для удаления
def add_message(message):
    if message.chat.id not in message_id:
        message_id[message.chat.id] = []
    message_id[message.chat.id].append(message.id)


# Функция для отправки сообщения
def send_message(chat_id, message, **kwargs):
    m = bot.send_message(chat_id, message, **kwargs)
    add_message(m)


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


def add_new_defects(dict):
    with open("data/Defects.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    data.append(dict)
    json.dump(data, open('data/Defects.json', 'w', encoding='utf-8'), ensure_ascii=False)


def get_driver(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        return json.load(json_file)[str(chat_id)]


def get_car(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login:
                return i["Car"]


def get_driver_data(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login:
                return i


def set_route(chat_id, flag):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        driver = json.load(file)
        for i in range(len(driver)):
            if driver[i]["Login"] == login:
                driver[i]["Route"] = flag
                json.dump(driver, open('data/Drivers.json', 'w', encoding='utf-8'), ensure_ascii=False)
                return


def set_car(chat_id, car):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        driver = json.load(file)
        for i in range(len(driver)):
            if driver[i]["Login"] == login:
                driver[i]["Car"] = car
                json.dump(driver, open('data/Drivers.json', 'w', encoding='utf-8'), ensure_ascii=False)
                return