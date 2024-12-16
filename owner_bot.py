from telebot import types
from functions_owner_for_json import *
from random import randint
from IoTRightechMain import get_state


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
        btn6 = types.InlineKeyboardButton('Заявки', callback_data='get_applications')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.add(btn6)
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
    elif 'anket' in call_funk:
        one_unwatched_anket(message, call_funk.split()[1])
    elif 'rej_applications' in call_funk:
        rej_applications(message, call_funk.split()[1])
    elif 'proof_applications' in call_funk:
        proof_applications(message, call_funk.split()[1])
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
            # case 'get_driver_statistic':
            #     get_driver_statistic(message)
            case 'get_applications':
                get_applications(message)
            case 'all_app':
                get_all_app(message)
            case 'rejected_app':
                get_rejected_app(message)
            case 'good_app':
                get_good_app(message)
            case 'unwatched_app':
                get_unwatched_app(message)


def get_applications(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Одобренные заявления', callback_data='good_app')
    btn2 = types.InlineKeyboardButton('Все', callback_data='all_app')
    btn3 = types.InlineKeyboardButton('Непросмотренные', callback_data='unwatched_app')
    btn4 = types.InlineKeyboardButton('Отвергнутые', callback_data='rejected_app')
    btn5 = types.InlineKeyboardButton('Назад', callback_data='main_menu')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.add(btn5)
    send_message(chat_id, 'Выберите категорию заявлений', reply_markup=markup)
    deleter(chat_id, message.id)


def get_all_app(message):
    chat_id = message.chat.id
    company = get_number_company(chat_id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='get_applications')
    markup.add(btn1)
    send_message(chat_id, get_app(company), reply_markup=markup)
    # TODO: норм вывод


def get_rejected_app(message):
    chat_id = message.chat.id
    company = get_number_company(chat_id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='get_applications')
    markup.add(btn1)
    send_message(chat_id, get_rej_app(company), reply_markup=markup)


def get_good_app(message):
    chat_id = message.chat.id
    company = get_number_company(chat_id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='get_applications')
    markup.add(btn1)
    send_message(chat_id, get_g_app(company), reply_markup=markup)
    deleter(chat_id, message.id)


# TODO: потом эти 3 функции можно будет красиво свернуть в одну


def get_unwatched_app(message):
    chat_id = message.chat.id
    company = get_number_company(chat_id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='get_applications')
    markup.add(btn1)
    list_apps = get_unw_app(company)
    for i in list_apps:
        markup.add(types.InlineKeyboardButton(f"Анкета № {i['Anket_id']}", callback_data=f'anket {i["Anket_id"]}'))
    send_message(chat_id, "Выберите нужный вам номер анкеты", reply_markup=markup)
    deleter(chat_id, message.id)


def one_unwatched_anket(message, anket_id):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='get_applications')
    btn2 = types.InlineKeyboardButton('Отклонить', callback_data=f'rej_applications {anket_id}')
    btn3 = types.InlineKeyboardButton('Подтвердить', callback_data=f'proof_applications {anket_id}')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    send_message(chat_id, get_one_anket(anket_id), reply_markup=markup)
    deleter(chat_id, message.id)
# TODO: КНОПКИ НЕ РАБОТАЮТ


def rej_applications(message, anket_id):
    chat_id = message.chat.id
    rej_applications_(message, anket_id)
    deleter(chat_id, message_id)
    send_message(chat_id, "Вы успешно отклонили заявку")
    get_unwatched_app(message)
    deleter(chat_id, message.id)


def proof_applications(message, anket_id):
    chat_id = message.chat.id
    proof_applications_(chat_id, anket_id)
    deleter(chat_id, message_id)
    send_message(chat_id, "Вы успешно подтвердили заявку")
    get_unwatched_app(message)
    deleter(chat_id, message.id)


def get_statistic(message, time, car_id):
    chat_id = message.chat.id

    cars = get_cars_reg()

    if time == "week":
        send_message(chat_id, f"Статистика по машине с гос номером - {cars[int(car_id)]['gosnum']} за <b>неделю</b>", parse_mode='html')
    elif time == "month":
        send_message(chat_id, f"Статистика по машине с гос номером - {cars[int(car_id)]['gosnum']} за <b>месяц</b>", parse_mode='html')
    elif time == "all_time":
        send_message(chat_id, f"Статистика по машине с гос номером - {cars[int(car_id)]['gosnum']} за <b>всё время</b>", parse_mode='html')

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
        if i["Route"]:
            send_message(chat_id, f'Машина - {i["Car"]} на маршруте', parse_mode='html')
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
                     f'ФИО Водителя - {i["Full_name"]} | Гос. Номер - {i["Car"]} | Логин - {i["Login"]} | Пароль - {i["Password"]}',
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
        if str(value["name"]) == str(company):
            send_message(chat_id, f"Гос.Номер - {value['gosnum']}  |  Марка авто - {value['brand']}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def get_data_car(message):
    chat_id = message.chat.id

    cars = get_cars_reg()
    company = get_name_company(chat_id)

    markup = types.InlineKeyboardMarkup()
    i = 0
    for value in cars:
        if str(value["name"]) == str(company):
            markup.add(types.InlineKeyboardButton(str(value['gosnum']), callback_data=f'car {i}'))
        i += 1
    send_message(chat_id, "🚗 Выбирите авто, которое хотите посмотреть", reply_markup=markup)
    deleter(chat_id, message.id)


def get_current_state_data(message, value):
    chat_id = message.chat.id
    # deleter(message)

    cars = get_cars_reg()
    markup = types.InlineKeyboardMarkup()

    wheel = get_wheels_data(int(value) + 1)
    print(wheel)
    sensors = get_sensors_data((int(value) + 1))

    j = 1
    x = 1
    for i in range(1, int(cars[int(value)]['wheels']) + 1):
        lst_w = []
        for _ in range(1, 5):
            print(f"wheel_{j}")
            if f"wheel_{j}" in wheel.keys() and sensors != {}:
                lst_w.append(types.InlineKeyboardButton(f"{sensors[f'sens_{x}']['temp'][-1]}°С | {sensors[f'sens_{x}']['pres'][-1]} Бар", callback_data='Noneee'))
            else:
                lst_w.append(types.InlineKeyboardButton(" ", parse_mode='html', callback_data='Noneee'))
            j += 1
            x += 1
        markup.row(*lst_w)

        # # data = get_state(i)
        # # print(data)
        # b1 = types.InlineKeyboardButton(f"№ {i} | {20}°С | {9} Бар", callback_data=f'wheel {i} {value}')
        # data2 = get_state(i + 1)
        # b2 = types.InlineKeyboardButton(f"№ {i + 1} | {26}°С | {9} Бар", callback_data=f'wheel {i + 1} {value}')
        # b3 = types.InlineKeyboardButton(f"№ {i} | T = 26°С | P = 6 Бар", callback_data=f'wheel {i} {value}')
        # b4 = types.InlineKeyboardButton(f"№ {i + 1} | T = 26°С | P = 6 Бар", callback_data=f'wheel {i + 1} {value}')
        # markup.row(b1, b2)

    send_message(chat_id, f"🚗 Данные по машине с номером - {cars[int(value)]['gosnum']}", parse_mode='html', reply_markup=markup)
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
