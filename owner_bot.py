from telebot import types
from functions_owner_for_json import *
from random import randint


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # if not is_sign_in(chat_id):
    #     bot.send_message(chat_id, 'Добро пожаловать в Систему Мониторига Грузового Транспорта')

    # deleter(chat_id, message.id - 1)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    send_message(chat_id, '🔐 Войти в систему для старта.', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    chat_id = message.chat.id

    # deleter(chat_id, message.id - 1)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Список всех водителей', callback_data='get_drivers')
        btn2 = types.InlineKeyboardButton('Список всех авто', callback_data='get_cars')
        btn3 = types.InlineKeyboardButton('Текущее состояние авто', callback_data='get_data_from_auto')
        btn4 = types.InlineKeyboardButton('Машины в пути', callback_data='get_route')
        btn5 = types.InlineKeyboardButton('Статистика по водителям', callback_data='get_driver_statistic')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.add(btn5)
        send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=markup)
        deleter(chat_id, message.id)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
    chat_id = message.chat.id

    # deleter(chat_id, message.id - 1)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_sign_in(chat_id):
        del_user_log(chat_id)
        send_message(chat_id, "🚪 Сессия завершена.\n", parse_mode='html')
        deleter(chat_id, message.id)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if "car " in call_funk:
        get_current_state_data(message, call_funk[4:])
    elif "wheel" in call_funk:
        get_wheel_data(message, call_funk.split()[1], call_funk.split()[2])
    elif "statistic" in call_funk:
        get_statistic(message, call_funk.split()[1], call_funk.split()[2])
    else:
        match call_funk:
            case 'sign_in':
                sign_in(message)
            case 'main_menu':
                main_message(message)
            case 'get_drivers':
                get_drivers(message)
            case 'get_cars':
                get_cars(message)
            case 'get_data_from_auto':
                get_data_car(message)
            case 'get_route':
                get_route(message)
            case 'get_driver_statistic':
                get_driver_statistic(message)


def get_driver_statistic(message):
    chat_id = message.chat.id


def get_statistic(message, time, car_id):
    chat_id = message.chat.id

    if time == "week":
        send_message(chat_id, f"Статистика по машине с гос номером - {car_id} за <b>неделю</b>", parse_mode='html')
    elif time == "month":
        send_message(chat_id, f"Статистика по машине с гос номером - {car_id} за <b>месяц</b>", parse_mode='html')
    elif time == "all_time":
        send_message(chat_id, f"Статистика по машине с гос номером - {car_id} за <b>всё время</b>", parse_mode='html')

    send_message(chat_id, f"Дата события: 22.10.2022\n"
                          f"Событие: Прокол колеса\n"
                          f"Длительность: {randint(5, 50)} минут", parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'car {car_id}'))
    send_message(chat_id, "Вернуться назад", reply_markup=markup)
    deleter(chat_id, message.id + 1)


def get_wheel_data(message, number, car_id):
    chat_id = message.chat.id

    brand_wheel = get_car_brand_wheel(car_id)
    send_message(chat_id, f"Данные по колесу №{number}:\n"
                          f"Марка шины - {brand_wheel}\n"
                          f"Пробег - {randint(1200, 3000)} км.\n"
                          f"Количество перегревов - {randint(0, 1)}", parse_mode='html')
    # deleter(chat_id, message.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'car {car_id}'))
    send_message(chat_id, "Вернуться назад", reply_markup=markup)
    deleter(chat_id, message.id + 2)


def get_route(message):
    chat_id = message.chat.id

    drivers = get_drivers_data(chat_id)
    send_message(chat_id, f'Сейчас на маршруте', parse_mode='html')

    deleter(chat_id, message.id)
    for i in drivers:
        if (drivers[i]["Route"]):
            send_message(chat_id, f'Машина - {drivers[i]["Car"]} на маршруте', parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def get_drivers(message):
    chat_id = message.chat.id
    # deleter(message)

    drivers = get_drivers_data(chat_id)
    send_message(chat_id, "Список ваших водителей", parse_mode='html')
    deleter(chat_id, message.id)
    for i in drivers:
        send_message(chat_id,
                     f'ФИО Водителя - {i["Full name"]} | Гос. Номер - {i["Car"]} | Логин - {i["Login"]} | Пароль - {i["Password"]}',
                     parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def get_cars(message):
    chat_id = message.chat.id

    cars = get_cars_reg()
    company = get_name_company(chat_id)

    send_message(chat_id, "🚗 Авто в вашем автопарке", parse_mode='html')
    deleter(chat_id, message.id)
    for value in cars:
        if str(cars[value]["name"]) == str(company):
            send_message(chat_id, f"Гос.Номер - {value}  |  Марка авто - {cars[value]['brand']}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def get_data_car(message):
    chat_id = message.chat.id
    # deleter(message)

    cars = get_cars_reg()
    company = get_name_company(chat_id)

    markup = types.InlineKeyboardMarkup()
    for value in cars:
        if str(cars[value]["name"]) == str(company):
            markup.add(types.InlineKeyboardButton(value, callback_data=f'car {value}'))
    send_message(chat_id, "🚗 Выбирите авто, которое хотите посмотреть", parse_mode='html', reply_markup=markup)
    deleter(chat_id, message.id)


def get_current_state_data(message, value):
    chat_id = message.chat.id
    # deleter(message)

    num = int(get_car_wheels(value))
    markup = types.InlineKeyboardMarkup()
    for i in range(1, num + 1, 2):
        b1 = types.InlineKeyboardButton(f"№ {i} | T = 26°С | P = 6 Бар", callback_data=f'wheel {i} {value}')
        b2 = types.InlineKeyboardButton(f"№ {i + 1} | T = 26°С | P = 6 Бар", callback_data=f'wheel {i + 1} {value}')
        markup.row(b1, b2)
    send_message(chat_id, f"🚗 Данные по машине с номером - {value}", parse_mode='html', reply_markup=markup)
    markup1 = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(f"неделю", callback_data=f'statistic week {value}')
    b2 = types.InlineKeyboardButton(f"месяц", callback_data=f'statistic month {value}')
    b3 = types.InlineKeyboardButton(f"всё время", callback_data=f'statistic all_time {value}')
    markup1.row(b1, b2, b3)
    send_message(chat_id, f"Статистика по машине за", parse_mode='html', reply_markup=markup1)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)
    deleter(chat_id, message.id)


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        send_message(chat_id, "💼 Введите номер телефона в +7**********", parse_mode='html')
        bot.register_next_step_handler(message, get_login)
    else:
        main_message(message)


# Функция для регистрации пользователя
def get_login(message):
    chat_id = message.chat.id
    login = message.text

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_registered(login):
        send_message(chat_id, "🔑 Телефон есть в системе. \nВведите пароль.\n", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_passwd, login=login)
    elif login == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        send_message(chat_id, "🚫 Телефон не зарегистрирован в системе. \nПовторите попытку.\n",
                     parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_login)


def get_passwd(message, login):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    passwd = message.text
    if is_acreditation(login, passwd):
        send_message(chat_id, "✅ Вход в систему выполнен.\n", parse_mode='html')
        deleter(chat_id, message.id)
        add_user_log(chat_id, login)
        main_message(message)
    elif passwd == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    elif passwd == '/sign_out':
        out_message(message)
    else:
        send_message(chat_id, "🚫 Неверный пароль. \nПовторите попытку.\n", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_passwd, login=login)


@bot.message_handler(func=lambda message: message)
def deleter(chat_id, message_id):
    deleter_message(chat_id, message_id, 10)


bot.infinity_polling()
