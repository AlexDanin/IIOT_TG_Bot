from telebot import TeleBot
import json
from pathlib import Path

token = '6821919054:AAGcj-d94HKSl8REdyJzRI-ahCmTDJDol-8'
bot = TeleBot(token)

message_id = {0: [0, 0]}


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(login):
    with open('data/Owners.json', 'r') as file:
        registered_users = json.load(file)
        return str(login) in registered_users.keys()


def is_acreditation(login, passwd):
    with open('data/Owners.json', 'r') as file:
        registered_users = json.load(file)
        return passwd == registered_users[login]["Password"]


def is_sign_in(chat_id):
    with open('sign_in_users_owner.json', 'r') as file:
        registered_users = json.load(file)
        return str(chat_id) in list(registered_users.keys())


def get_sign_in_user(chat_id):
    with open('sign_in_users_owner.json', 'r') as file:
        registered_users = json.load(file)
        return registered_users[str(chat_id)]


def add_user_log(chat_id, login):
    if not is_sign_in(chat_id):
        with open('sign_in_users_owner.json', 'r') as file:
            registered_users = json.load(file)

        registered_users[chat_id] = str(login)

        with open('sign_in_users_owner.json', 'w', encoding='utf-8') as file:
            json.dump(registered_users, file, ensure_ascii=False)


def del_user_log(chat_id):
    if is_sign_in(chat_id):
        with open("sign_in_users_owner.json", "r") as json_file:
            data = json.load(json_file)

        chat_id = str(chat_id)

        # Находим запись, которую нужно удалить (например, по ключу)
        if chat_id in data:
            del data[chat_id]

        # Сохраняем обновленные данные в файл
        with open("sign_in_users_owner.json", "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)


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


def get_app(company):
    with open("data/Ankets.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        ans = ""
        for i in file_:
            if company in i["Company"]:
                ans += f"ID анкеты = {str(i['Anket_id'])} Статус = {i['Status']}\n"
        return ans


def get_rej_app(company):
    with open("data/Ankets.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        list_ = [i for i in file_ if company in i["Company"] and i["Status"] == "Отклонён"]
    with open("data/Drivers.json", "r", encoding="utf-8") as json_file2:
        file_2 = json.load(json_file2)
    ans_ = ""
    for j in list_:
        ans_ += f"ID анкеты = {j['Anket_id']} ФИО водителя = {file_2[int(j['Anket_id'] - 1)]['Full_name']}\n"
    return str(ans_)


def get_g_app(company):
    with open("data/Ankets.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        list_ = [i for i in file_ if company in i["Company"] and i["Status"] == "Удтверждён"]
    with open("data/Drivers.json", "r", encoding="utf-8") as json_file2:
        file_2 = json.load(json_file2)
    ans_ = ""
    for j in list_:
        ans_ += f"ID анкеты = {j['Anket_id']} ФИО водителя = {file_2[int(j['Anket_id'] - 1)]['Full_name']}\n"
    return str(ans_)


def get_unw_app(company):
    with open("data/Ankets.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        return [i for i in file_ if str(company) in i["Company"] and i["Status"] == "На рассмотрении"]


def rej_applications_(message, anket_id):
    with open('data/Ankets.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[int(anket_id) - 1]['Status'] = 'Отклонён'
    with open('data/Ankets.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def proof_applications_(chat_id, anket_id):
    with open('data/Ankets.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[int(anket_id) - 1]['Status'] = 'Удтверждён'
    driver_id = data[int(anket_id) - 1]['driver_id']

    with open('data/Ankets.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    with open("data/Drivers.json", "r", encoding="utf-8") as json_file:
        driver_file = json.load(json_file)

    for i in range(len(driver_file)):
        if driver_file[i]["ID"] == driver_id:
            driver_file[i]["Company"] = get_name_company(chat_id)
            break

    with open('data/Drivers.json', 'w', encoding='utf-8') as f:
        json.dump(driver_file, f, ensure_ascii=False)
    # path = Path('data/Ankets.json')
    # data = json.loads(path.read_text(encoding='utf-8'))
    # print(data[int(anket_id)-1]['Driver_id'])
    # print(f"ФИО водителя = {driver_file[int(data[int(anket_id)-1]['Driver_id']-1)]['Full_name']}")
    # data['frames'].append({"Birthday": data[int(anket_id)-1]['Driver_id']})
    # path.write_text(json.dumps(data), encoding='utf-8')


def get_one_anket(anket_id):
    with open("data/Ankets.json", "r", encoding="utf-8") as json_file:
        file_ = json.load(json_file)
        driver_id = file_[int(anket_id) - 1]["driver_id"]
    with open("data/Drivers.json", "r", encoding="utf-8") as json_file2:
        file_2 = json.load(json_file2)
        driver = file_2[driver_id - 1]["Full_name"]
    return f"ID анкеты = {anket_id} ФИО водителя = {driver}"


def get_name_company(chat_id):
    with open("sign_in_users_owner.json", "r", encoding="utf-8") as json_file:
        number = json.load(json_file)[str(chat_id)]
    with open("data/Owners.json", "r", encoding="utf-8") as json_file:
        company = json.load(json_file)[number]["Company"]
    with open("data/Companies.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)[company]


def get_number_company(chat_id):
    with open("sign_in_users_owner.json", "r", encoding="utf-8") as json_file:
        number = json.load(json_file)[str(chat_id)]
    with open("data/Owners.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)[number]["Company"]


def get_drivers_data(chat_id):
    name_company = get_name_company(chat_id)
    lst = []
    with open("data/Drivers.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            if data[i]["Company"] == name_company:
                lst.append(data[i])
        return lst


def get_cars_reg():
    with open('data/Cars.json', 'r', encoding="utf-8") as file:
        return json.load(file)


def get_car_wheels(id):
    with open('data/Cars.json', 'r', encoding="utf-8") as file:
        return json.load(file)[int(id)]["wheels"]


def get_car_brand_wheel(id):
    with open('data/Cars.json', 'r', encoding="utf-8") as file:
        return json.load(file)[int(id)]["brandWs"]


def get_wheels_data(car_id):
    with open('data/Wheels.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    for i in range(len(data)):
        if data[i]["id_car"] == car_id:
            return data[i]


def get_sensors_data(car_id):
    with open('data/Cars.json', 'r', encoding="utf-8") as file:
        car = json.load(file)

    device_id = 0

    for i in car:
        if i["id"] == car_id:
            device_id = i["device"]
            break

    with open('data/Sensors_Data.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    for i in data:
        if int(i) == device_id:
            return data[i]

    return {}