from telebot import types
from functions_driver_for_json import *

dict_def = {'Type1': "", 'Type2': "", 'car_id': "", 'driver_id': "", 'describe': ""}


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    send_message(chat_id, '🔐 Войти в систему для старта.', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    global dict_def

    dict_def = {'Type1': "", 'Type2': "", 'car_id': "", 'driver_id': "", 'describe': ""}

    chat_id = message.chat.id

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Добавить поломку', callback_data='add_defects'))
        driver = get_driver_data(chat_id)
        if not driver["Route"]:
            markup.add(types.InlineKeyboardButton('Войти на маршрут', callback_data='route false'))
        elif driver["Route"]:
            markup.add(types.InlineKeyboardButton('Уйти с маршрута', callback_data='route true'))
        send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=markup)
        deleter(chat_id, message.id)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
    chat_id = message.chat.id

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_sign_in(chat_id):
        del_user_log(chat_id)
        send_message(chat_id, "🚪 <b>Сессия завершена.</b>\n", parse_mode='html')
        deleter(chat_id, message.id)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message

    # deleter(message)
    #
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if "def_err" in call_funk:
        add_description(message, call_funk[7:])
    elif "route" in call_funk:
        route(message, call_funk.split()[1])
    else:
        match call_funk:
            case 'sign_in':
                sign_in(message)
            case 'main_menu':
                main_message(message)
            case 'add_defects':
                add_defects(message)
            case 'mechanic':
                add_mechanic_defects(message)
            case 'electronic':
                add_electronic_defects(message)
            case 'other':
                add_other_defects(message)
            case 'save':
                save_defects(message)
            case 'description':
                send_message(chat_id, "Напишите описание поломки", parse_mode='html')
                deleter(chat_id, message.id)
                bot.register_next_step_handler(message, add_description_defects)


def route(message, flag):
    chat_id = message.chat.id

    print(flag)

    if flag == "false":
        send_message(chat_id, "Введите гос. номер авто в формате А111АА196", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, change_car)
    elif flag == "true":
        set_route(chat_id, False)
        send_message(chat_id, "Вы успешно завершили маршрут", parse_mode='html')
        deleter(chat_id, message.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
        send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def change_car(message):
    chat_id = message.chat.id

    set_route(chat_id, True)
    set_car(chat_id, message.text)
    send_message(chat_id, "Вы успешно вошли на маршрут", parse_mode='html')
    deleter(chat_id, message.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)



def add_defects(message):
    chat_id = message.chat.id
    # deleter(message)

    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(f"Механическая", callback_data=f'mechanic')
    b2 = types.InlineKeyboardButton(f"Электрические", callback_data=f'electronic')
    markup.row(b1, b2)
    send_message(chat_id, f"Выберете тип поломки", parse_mode='html', reply_markup=markup)
    deleter(chat_id, message.id)


def add_mechanic_defects(message):
    dict_def["Type1"] = "Механическая"
    chat_id = message.chat.id
    # deleter(message)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Система охлаждения', callback_data='def_err' + "Система охлаждения"))
    markup.add(types.InlineKeyboardButton('Водяной насос', callback_data='def_err' + 'Водяной насос'))
    markup.add(types.InlineKeyboardButton('Шины', callback_data='def_err' + 'Шины'))
    markup.add(types.InlineKeyboardButton('Привод ГРМ', callback_data='def_err' + 'Привод ГРМ'))
    markup.add(types.InlineKeyboardButton('Другое', callback_data='other'))
    send_message(chat_id, 'Где именно', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


def add_electronic_defects(message):
    dict_def["Type1"] = "Электрическая"
    chat_id = message.chat.id
    # deleter(message)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Система (ABS)', callback_data='def_err' + "Система (ABS)"))
    markup.add(types.InlineKeyboardButton('Системы комфорта', callback_data='def_err' + 'Системы комфорта'))
    markup.add(types.InlineKeyboardButton('Система торможения (EBS)', callback_data='def_err' + 'Система торможения (EBS)'))
    markup.add(types.InlineKeyboardButton('Круиз контроль (ACC)', callback_data='def_err' + 'Круиз контроль (ACC)'))
    markup.add(types.InlineKeyboardButton('Другое', callback_data='other'))
    send_message(chat_id, 'Где именно', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


def add_description(message, type_data):
    dict_def["Type2"] = type_data
    chat_id = message.chat.id
    # deleter(message)

    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Добавить описание', callback_data='description')
    b2 = types.InlineKeyboardButton('Сохранить', callback_data='save')
    markup.row(b1, b2)
    send_message(chat_id, "Добавить описание поломки?", reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


def add_other_defects(message):
    chat_id = message.chat.id
    # deleter(message)

    send_message(chat_id, "Введите тип поломки", parse_mode='html')
    deleter(chat_id, message.id)
    bot.register_next_step_handler(message, get_other_defects)


def get_other_defects(message):
    chat_id = message.chat.id
    # deleter(message)

    dict_def["Type2"] = message.text
    send_message(chat_id, "Напишите описание поломки", parse_mode='html')
    deleter(chat_id, message.id)
    bot.register_next_step_handler(message, add_description_defects)


def add_description_defects(message):
    chat_id = message.chat.id
    # deleter(message)
    #
    # add_message(message)

    dict_def["describe"] = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сохранить', callback_data='save'))
    send_message(chat_id, "Сохранить поломку?", reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


def save_defects(message):
    global dict_def
    chat_id = message.chat.id
    # deleter(message)

    dict_def["car_id"] = get_car(chat_id)
    dict_def["driver_id"] = get_driver(chat_id)

    add_new_defects(dict_def)

    send_message(chat_id, "✅Сохранение было выполнно <u>успешно.</u>\n", parse_mode='html')
    deleter(chat_id, message.id)
    main_message(message)


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        send_message(chat_id, "💼 Введите наименование компании", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_company)
    else:
        main_message(message)


def get_company(message):
    chat_id = message.chat.id
    company = message.text

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_company(company):
        send_message(chat_id, "🔑 Компания есть <u>в системе.</u> \nВведите ваш <b>логин</b>.\n",
                     parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_login, company=company)
    elif company == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        send_message(chat_id,
                     "🚫 Компания не зарегистрирован в системе. Возможно введена неправильно\nПовторите попытку.\n",
                     parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_company)


# Функция для регистрации пользователя
def get_login(message, company):
    chat_id = message.chat.id
    login = message.text

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_registered(login, company):
        send_message(chat_id, "🔑 Логин есть в системе. \nВведите пароль.\n", parse_mode='html')
        bot.register_next_step_handler(message, get_passwd, login=login, company=company)
        deleter(chat_id, message.id)
    elif login == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        send_message(chat_id, "🚫 Логин не зарегистрирован в системе. \nПовторите попытку.\n",
                     parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_login)


def get_passwd(message, login, company):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    passwd = message.text
    if is_acreditation(passwd, login, company):
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
def deleter(chat_id, message_id, num=10):
    deleter_message(chat_id, message_id, num)


bot.infinity_polling()
