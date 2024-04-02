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

    # gosnum = car_reg_logs['gosnum']

    # if gosnum not in dict(cars).keys():
    #     cars[gosnum] = car_reg_logs
    # else:
    #     cars[gosnum] = cars[gosnum] | car_reg_logs
    if len(cars) != 0:
        if cars[-1]['gosnum'] != car_reg_logs['gosnum']:
            id = len(cars)
            car_reg_logs["id"] = id + 1
            cars.append(car_reg_logs)

            with open('data/Cars.json', 'w', encoding='utf-8') as file:
                json.dump(cars, file, ensure_ascii=False)
    else:
        id = len(cars)
        car_reg_logs["id"] = id + 1
        cars.append(car_reg_logs)

        with open('data/Cars.json', 'w', encoding='utf-8') as file:
            json.dump(cars, file, ensure_ascii=False)

    # del_car_reg_log(chat_id)


def form_text(chat_id, kwags):
    main_text = f"⚙️ <b>Добавление <u>устройств</u> в базу данных</b> \n"
    device_text = f"🆔 <b>Укажите</b> <u>ID</u> устройства\n"
    name_text = f"🏢 <b>Введите</b> <u>наименование компании</u>\n"
    gosnum_text = f"🚘 <b>Введите</b> государственный <u>номер автомобиля</u>\n"
    brand_text = f"🚗 <b>Укажите</b> <u>марку автомобиля</u>\n"
    wheels_text = f"🛞 <b>Введите</b> количество <u>осей</u> автомобиля\n"

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
                    wheels_text = f"🛞 <b>{kwags['wheels']}</b> количество <u>осей</u> автомобиля\n"

    return main_text + device_text + name_text + gosnum_text + brand_text + wheels_text


def add_new_wheels(num_of_axes):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    wheel = {
        "id": len(wheels) + 1,
        "id_car": get_cars_reg()[-1]['id'],
        "count": num_of_axes,
        "brand_wheel": ""
    }

    if len(wheels) != 0:
        if wheels[-1]['id_car'] != wheel['id_car']:
            wheels.append(wheel)

            with open('data/Wheels.json', 'w', encoding='utf-8') as file:
                json.dump(wheels, file, ensure_ascii=False)
    else:
        wheels.append(wheel)

        with open('data/Wheels.json', 'w', encoding='utf-8') as file:
            json.dump(wheels, file, ensure_ascii=False)


def wheel_text_form(wheel_id):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    main_text = f"Конфигурация колеса\n"
    id_sensor_text = f"Номер датчика:  <b>{wheels[-1][wheel_id]['sensor_num']}</b>\n"
    min_t_text = f"Мин. температура:  <b>{wheels[-1][wheel_id]['min_t']}</b>\n"
    max_t_text = f"Макс. температура:  <b>{wheels[-1][wheel_id]['max_t']}</b>\n"
    standard_t_text = f"Эталонная температура:  <b>{wheels[-1][wheel_id]['standard_t']}</b>\n"
    min_p_text = f"Мин. давление:  <b>{wheels[-1][wheel_id]['min_p']}</b>\n"
    max_p_text = f"Макс. давление:  <b>{wheels[-1][wheel_id]['max_p']}</b>\n"
    standard_p_text = f"Эталонное давление:  <b>{wheels[-1][wheel_id]['standard_p']}</b>\n"

    # chat_id = str(chat_id)
    # kwags = get_car_reg_log(chat_id)
    #
    # if chat_id in kwags:
    #
    #     kwags = get_car_reg_log(chat_id)[chat_id]
    #
    #     for key in get_car_reg_log(chat_id)[chat_id].keys():
    #         match key:
    #             case 'device':
    #                 device_text = f"🆔 <b>{kwags['device']}</b> <u>ID</u> устройства\n"
    #             case 'name':
    #                 name_text = f"🏢 <b>{kwags['name']}</b> <u>наименование компании</u>\n"
    #             case 'gosnum':
    #                 gosnum_text = f"🚘 <b>{kwags['gosnum']}</b> государственный <u>номер автомобиля</u>\n"
    #             case 'brand':
    #                 brand_text = f"🚗 <b>{kwags['brand']}</b> <u>марку автомобиля</u>\n"
    #             case 'wheels':
    #                 wheels_text = f"🛞 <b>{kwags['wheels']}</b> количество <u>осей</u> автомобиля\n"

    return main_text + id_sensor_text + min_t_text + max_t_text + standard_t_text + min_p_text + max_p_text + standard_p_text


def is_sensor_is(sensor_id):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    return wheels[-1].get(sensor_id)


def add_sensor_to_wheels(num_wheels):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    sensor = {
        "sensor_num": None,
        "min_t": None,
        "max_t": None,
        "standard_t": None,
        "min_p": None,
        "max_p": None,
        "standard_p": None
    }

    wheels[-1][num_wheels] = sensor

    with open('data/Wheels.json', 'w', encoding='utf-8') as file:
        json.dump(wheels, file, ensure_ascii=False)


def del_sensor_from_wheels(num_wheels):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    del wheels[-1][num_wheels]

    with open('data/Wheels.json', 'w', encoding='utf-8') as file:
        json.dump(wheels, file, ensure_ascii=False)


def get_created_sensors_list():
    lst = [' '] * 4 * int(get_cars_reg()[-1]['wheels'])

    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    if len(wheels) != 0 and len(wheels) == len(get_cars_reg()):
        for i in wheels[-1].keys():
            if 'wheel_' in i:
                lst[int(i.replace('wheel_', '')) - 1] = '✅'

    return lst


def add_data_to_wheel(wheel_id, param, data):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    wheels[-1][wheel_id][param] = data

    with open('data/Wheels.json', 'w', encoding='utf-8') as file:
        json.dump(wheels, file, ensure_ascii=False)


def is_wheel_ok(wheel_id):
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    for i in wheels[-1][wheel_id]:
        if wheels[-1][wheel_id][i] == None:
            return False
    return True


def is_someone_wheel():
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    if len(wheels) != 0:
        for i in wheels[-1].keys():
            if 'wheel_' in i:
                return wheels[-1][i]
    # return False

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
