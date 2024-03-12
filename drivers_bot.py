from telebot import types
from functions_driver_for_json import *

dict_def = {'Type1': "", 'Type2': "", 'car_id': "", 'driver_id': "", 'describe': ""}
dict_driver = {"Birthday": "", "Full_name": "", "ID": "", "Login": "", "Password": "", "Route": False, "Car": "", "Company": "",}


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    markup.add(types.InlineKeyboardButton('Зарегистрироваться', callback_data='registration'))
    send_message(chat_id, '🔐 Войти в систему/зарегистрироваться для старта.', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    global dict_def

    dict_def = {'Type1': "", 'Type2': "", 'car_id': "", 'driver_id': "", 'describe': ""}

    chat_id = message.chat.id

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        # TODO: здесь нужно еще сделать разветвление для просто просмотра состояния заявления
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Статус', callback_data='get_status'))
        status = get_driver_status(chat_id)
        print(status)
        if status == "Удтверждён":
            markup.add(types.InlineKeyboardButton('Добавить поломку', callback_data='add_defects'))
            driver = get_driver_data(chat_id)
            if not driver["Route"]:
                markup.add(types.InlineKeyboardButton('Войти на маршрут', callback_data='route false'))
            elif driver["Route"]:
                markup.add(types.InlineKeyboardButton('Уйти с маршрута', callback_data='route true'))
        send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=markup)
        deleter(chat_id, message.id)


def registration_driver(message):
    chat_id = message.chat.id
    send_message(chat_id, "Для регистрации ввведите свои ФИО", parse_mode='html')
    bot.register_next_step_handler(message, add_birthday)


def add_birthday(message):
    chat_id = message.chat.id
    dict_driver['Full_name'] = message.text
    send_message(chat_id, "Введите дату своего рождения в формате ДД.ММ.ГГГГ", parse_mode='html')
    # TODO: проверка на корректность введеных данных
    bot.register_next_step_handler(message, add_login)


def add_login(message):
    chat_id = message.chat.id
    dict_driver['Birthday'] = message.text
    send_message(chat_id, "Введите логин ", parse_mode='html')
    bot.register_next_step_handler(message, add_password)


def add_password(message):
    chat_id = message.chat.id
    dict_driver['Login'] = message.text
    send_message(chat_id, "Введите пароль", parse_mode='html')
    bot.register_next_step_handler(message, end_of_registration)


def end_of_registration(message):
    chat_id = message.chat.id
    dict_driver['Password'] = message.text
    dict_driver['ID'] = get_id("data/Drivers.json", "ID")
    add_to_file("data/Drivers.json", dict_driver)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Заполнить анкету на работу', callback_data='create_application'))
    send_message(chat_id, "Вы успешно вошли в аккаунт", parse_mode='html', reply_markup=markup)
    deleter(chat_id, message.id)
    add_user_log(chat_id, dict_driver['Login'])


def create_application(message):
    chat_id = message.chat.id
    all_companies()
    send_message(chat_id, "Введите через запятую компании, в которые вы хотите отправить заявления", parse_mode='html')
    send_message(chat_id, f"Список всех компаний:"
                          f"\n {all_companies()}", parse_mode='html')
    bot.register_next_step_handler(message, add_company)


def add_company(message):
    chat_id = message.chat.id
    # get_company(message)
    company = message.text
    app_dict = {"Anket_id": get_id("data/Ankets.json", "Anket_id"),
                'Company': get_company_id(company), "Status": 'На рассмотрении', "driver_id": dict_driver["ID"]}
    add_to_file("data/Ankets.json", app_dict)
    send_message(chat_id, "Заявление было успешно отправлено", parse_mode='html')
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
            case 'registration':
                registration_driver(message)
            case 'create_application':
                create_application(message)
            case 'description':
                send_message(chat_id, "Напишите описание поломки", parse_mode='html')
                deleter(chat_id, message.id)
                bot.register_next_step_handler(message, add_description_defects)
            case 'get_status':
                get_status(message)


def get_status(message):
    chat_id = message.chat.id

    status = get_driver_status(chat_id)
    if status == "Удтверждён":
        send_message(chat_id, f"Ваш текущий статус - Работаете в компании '{get_driver_company(chat_id)}'", parse_mode='html')
    if status == "Отклонён" or status == "На рассмотрении":
        send_message(chat_id, f"Ваш текущий статус - {status}", parse_mode='html')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)
    deleter(chat_id, message.id)


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

    add_to_file("data/Defects.json", dict_def)

    send_message(chat_id, "✅Сохранение было выполнно <u>успешно.</u>\n", parse_mode='html')
    deleter(chat_id, message.id)
    main_message(message)


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        send_message(chat_id, "Введите свой логин", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, check_login)
    else:
        main_message(message)


def check_login(message):
    chat_id = message.chat.id
    login = message.text
    if is_registered(login):
        send_message(chat_id, "Ваш логин есть в системе.\nВведите пароль.\n", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_passwd, login=login)
    else:
        send_message(chat_id, "Логин не зарегистрирован в системе.", parse_mode='html')
        start_message(message)


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

# def get_company(message):
#     chat_id = message.chat.id
#     company = message.text
#
#     # deleter(message)
#     # add_message(message)  # Добавление сообщения, которое ввёл пользователь
#
#     if is_company(company):
#         send_message(chat_id, "🔑 Компания есть <u>в системе.</u> \nВведите ваш <b>логин</b>.\n",
#                      parse_mode='html')
#         deleter(chat_id, message.id)
#         bot.register_next_step_handler(message, get_login, company=company)
#     elif company == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
#         start_message(message)
#     else:
#         send_message(chat_id,
#                      "🚫 Компания не зарегистрирован в системе. Возможно введена неправильно\nПовторите попытку.\n",
#                      parse_mode='html')
#         deleter(chat_id, message.id)
#         bot.register_next_step_handler(message, get_company)

@bot.message_handler(func=lambda message: message)
def deleter(chat_id, message_id, num=10):
    deleter_message(chat_id, message_id, num)


bot.infinity_polling()
