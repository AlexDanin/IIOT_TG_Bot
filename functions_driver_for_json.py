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


def get_company_id(company):
    with open('data/Companies.json', 'r', encoding='utf-8') as file:
        company_ = json.load(file)
        for k, v in company_.items():
            if v == company:
                return k


# Функция для проверки, зарегистрирован ли пользователь


def is_registered(login):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login:
                return True
        return False


def is_password_login(login, password):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login and i["Password"] == password:
                return True
        return False


def is_not_work(login, password):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            print("login", i["Login"] == login, "Password", i["Password"] == password)
            print(i["Company"] == "" and i["Login"] == login and i["Password"] == password)
            if i["Company"] == "" and i["Login"] == login and i["Password"] == password:
                print("YES")
                return True
        return False


def is_acreditation(login, passwd):
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        for i in registered_users:
            if i["Login"] == login and i["Password"] == passwd:
                return True
        return False


def is_sign_in(chat_id):
    with open('sign_in_users_driver.json', 'r', encoding='utf-8') as file:
        registered_users = json.load(file)
        return str(chat_id) in list(registered_users.keys())


def all_companies():
    print("YES")
    with open("data/Companies.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        return ', '.join(list(file_.values()))


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


def change_status_anketa(chat_id, company):
    with open("data/Ankets.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    for i in range(len(data)):
        if data[i]["driver_id"] == get_driver_data(chat_id)["ID"]:
            data[i]["Status"] = "На рассмотрении"
            data[i]["Company"] = get_company_id(company)
            break
    with open("data/Ankets.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def add_to_file(file, dict_):
    with open(file, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    data.append(dict_)
    json.dump(data, open(file, 'w', encoding='utf-8'), ensure_ascii=False)


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


def get_id(file_, name):
    with open(file_, "r", encoding='utf-8') as json_file:
        file = json.load(json_file)
        if len(file) == 0:
            return 1
        return file[len(file) - 1][name] + 1


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


def get_driver_status(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    driver_id = 0
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        driver = json.load(file)
    for i in range(len(driver)):
        if driver[i]["Login"] == login:
            driver_id = driver[i]["ID"]
    print(driver_id)
    with open('data/Ankets.json', 'r', encoding='utf-8') as file:
        anketa = json.load(file)
    for i in range(len(anketa)):
        if anketa[i]["driver_id"] == driver_id:
            print(anketa[i]["Anket_id"])
            return anketa[i]["Status"]


def get_ankets_driver(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    driver_id = 0
    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        driver = json.load(file)
    for i in range(len(driver)):
        if driver[i]["Login"] == login:
            driver_id = driver[i]["ID"]
    with open('data/Ankets.json', 'r', encoding='utf-8') as file:
        anketa = json.load(file)
    for i in range(len(anketa)):
        if anketa[i]["driver_id"] == driver_id:
            return True
    return False


def get_driver_company(chat_id):
    with open("sign_in_users_driver.json", "r", encoding='utf-8') as json_file:
        login = json.load(json_file)[str(chat_id)]

    with open('data/Drivers.json', 'r', encoding='utf-8') as file:
        driver = json.load(file)
    for i in range(len(driver)):
        if driver[i]["Login"] == login:
            return driver[i]["Company"]
