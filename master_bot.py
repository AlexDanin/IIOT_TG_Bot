from telebot import types
from function_master_and_data import *
from draw_wheel_formula import get_result

lst = []


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    send_message(chat_id, '🔐 Войти в систему для старта.', reply_markup=markup, parse_mode='html')
    deleter(chat_id, message.id)


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    chat_id = message.chat.id

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Зарегистрировать авто', callback_data='car_reg'))
        markup.add(types.InlineKeyboardButton('Список зарегистрированных авто', callback_data='get_car'))
        send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=markup)
        deleter(chat_id, message.id, 40)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
    chat_id = message.chat.id

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_sign_in(chat_id):
        del_user_log(chat_id)
        send_message(chat_id, "🚪 Сессия завершена.\n", parse_mode='html')
        deleter(chat_id, message.id)


# Добавил команду для очистки чата
@bot.message_handler(commands=['clear'])
def clear_all_message(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    del_message(chat_id)  # Удаление всех сообщений в чате


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message

    # deleter(message)

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if 'sensor' in call_funk:
        sensor_settings(message, call_funk.split()[-1])
    elif 'clear_wheel' in call_funk:
        clear_wheel(message, call_funk.split()[-1])
    elif 'add_min' in call_funk:
        add_min(message, *call_funk.split()[1:])
    elif 'add_max' in call_funk:
        add_max(message, *call_funk.split()[1:])
    elif 'add_stand' in call_funk:
        add_stand(message, *call_funk.split()[1:])
    elif 'add_wheel_num' in call_funk:
        add_sensor_num(message, call_funk.split()[-1])
    elif 'save_wheel_data' in call_funk:
        save_wheel_data(message, call_funk.split()[-1])
    elif 'return_without_save' in call_funk:
        return_without_save(message, call_funk.split()[-1])
    elif 'get_data_from_previous' in call_funk:
        get_data_from_previous(message, call_funk.split()[-1])
    else:
        match call_funk:
            case 'sign_in':
                sign_in(message)
            case 'main_menu':
                main_message(message)
            case 'car_reg':
                car_registration(message)
            case 'exit_reg':
                exit_registration(message)
            case 'add_device':
                add_device(message)
            case 'add_name':
                add_name(message)
            case 'add_gosnum':
                add_gosnum(message)
            case 'add_brand':
                add_brand(message)
            case 'add_wheels':
                add_wheels(message)
            case 'end_reg':
                end_registration(message)
            case 'get_car':
                get_registration_cars(message)
            case 'create_wheels_formula':
                create_wheels_formula(message)
            case 'check_result':
                check_result(message)
            case 'save_wheels_formula':
                save_wheels_formula(message)


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


# Функция для регистрации пользователя
def get_login(message):
    chat_id = message.chat.id
    login = message.text

    # deleter(message)
    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if is_registered(login):
        send_message(chat_id, "🔑 Логин есть в системе. \nВведите пароль.\n", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_passwd, login=login)
    elif login == '/start':  # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        send_message(chat_id, "🚫 Логин не зарегистрирован в системе. \nПовторите попытку.\n",
                     parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_login)


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        send_message(chat_id, "💼 Введите логин компании.", parse_mode='html')
        deleter(chat_id, message.id)
        bot.register_next_step_handler(message, get_login)
    else:
        main_message(message)


def car_registration(message, **kwags):
    chat_id = message.chat.id

    add_car_reg_log(chat_id, **kwags)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🚫', callback_data='exit_reg'))
    send_message(chat_id, '❗❗ Отменить регистрацию. ❗❗', reply_markup=markup)

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('⚙️ Устройство', callback_data='add_device')
    btn2 = types.InlineKeyboardButton('🏢 Компания', callback_data='add_name')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🚘 Гос. номер', callback_data='add_gosnum')
    btn4 = types.InlineKeyboardButton('🚗 Марка автомобиля', callback_data='add_brand')
    markup.row(btn3, btn4)
    markup.add(types.InlineKeyboardButton('🛞 Количество осей', callback_data='add_wheels'))
    markup.add(types.InlineKeyboardButton('Завершить регистрацию ✅', callback_data='end_reg'))

    send_message(chat_id, form_text(chat_id, kwags), parse_mode='html', reply_markup=markup)
    deleter(chat_id, message.id)


def exit_registration(message):
    chat_id = message.chat.id
    del_car_reg_log(chat_id)
    send_message(chat_id, 'Регистрация завершена 🚫.')
    deleter(chat_id, message.id)
    main_message(message)


def get_registration_cars(message):
    chat_id = message.chat.id
    cars = get_cars_reg()
    user = get_sign_in_user(chat_id)

    send_message(chat_id, "🚗 Зарегистрированные вами авто:", parse_mode='html')
    deleter(chat_id, message.id)
    for value in cars:
        if str(value["master"]) == str(user):
            send_message(chat_id, value['gosnum'])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data=f'main_menu'))
    send_message(chat_id, "Вернуться в меню", reply_markup=markup)


def end_registration(message):
    global lst

    chat_id = message.chat.id

    chat_id = str(chat_id)

    if chat_id in get_car_reg_log(chat_id):
        if ('gosnum' and 'device' and 'name' and 'wheels' and 'brand') in get_car_reg_log(chat_id)[str(chat_id)].keys():
            save_car_reg_log(chat_id)
            send_message(chat_id, 'Регистрация завершена успешно ✅.')
            lst = get_created_sensors_list()

            add_new_wheels(int(get_cars_reg()[-1]['wheels']))
            create_wheels_formula(message)
        else:
            send_message(chat_id,
                         'Регистрация не завершина 🚫.\n Не все данные были введены')
            car_registration(message)
    else:
        send_message(chat_id, 'Регистрация не завершина 🚫.\n Заполните форму!')
        car_registration(message)


# add_func
def add_device(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🆔 Укажите ID устройства', parse_mode='html')
    bot.register_next_step_handler(message, device_property)


def add_name(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🏢 Введите наименование компании', parse_mode='html')
    bot.register_next_step_handler(message, name_property)


def add_gosnum(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚗 Введите государственный номер автомобиля в формате А111АА196', parse_mode='html')
    bot.register_next_step_handler(message, gosnum_property)


def add_brand(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚘 Укажите марку автомобиля', parse_mode='html')
    bot.register_next_step_handler(message, brand_property)


def add_wheels(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🛞 Введите количество осей автомобиля', parse_mode='html')
    bot.register_next_step_handler(message, wheels_property)


# property
def device_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Девайс {text} добавлен')
    car_registration(message, device=text)


def name_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Компания {text} добавлена')
    car_registration(message, name=text)


def gosnum_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Государственный номер {text} добавлен')
    car_registration(message, gosnum=text)


def brand_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Марка автомобиля {text} добавлена')
    car_registration(message, brand=text)


def wheels_property(message):
    chat_id = message.chat.id

    add_message(message)  # Добавление сообщения, которое ввёл пользователь

    text = message.text
    send_message(chat_id, f'Кол-во осей {text} добавлено')
    car_registration(message, wheels=text)


# Добавление колёс авто

def create_wheels_formula(message):
    global lst

    chat_id = message.chat.id
    num_of_axes = int(get_cars_reg()[-1]['wheels'])


    markup = types.InlineKeyboardMarkup()
    j = 1
    for i in range(num_of_axes):
        btn1 = types.InlineKeyboardButton(f'{lst[j - 1]}', callback_data=f'sensor {j}')
        btn2 = types.InlineKeyboardButton(f'{lst[j]}', callback_data=f'sensor {j + 1}')
        btn3 = types.InlineKeyboardButton(f'{lst[j + 1]}', callback_data=f'sensor {j + 2}')
        btn4 = types.InlineKeyboardButton(f'{lst[j + 2]}', callback_data=f'sensor {j + 3}')
        markup.row(btn1, btn2, btn3, btn4)
        j += 4
    btn1 = types.InlineKeyboardButton('Посмотреть результат', callback_data='check_result')
    btn2 = types.InlineKeyboardButton('Сохранить', callback_data='save_wheels_formula')
    markup.row(btn1, btn2)
    send_message(chat_id,
                 f"Редактирование колёс\nПеред вами шаблон колёс на авто. Это {num_of_axes} осей по 4 колеса вида:\n🛞🛞   🛞🛞\nНажмите на нужое колесо для установки параметров",
                 reply_markup=markup)
    deleter(chat_id, message.id)


def sensor_settings(message, id_sensor):
    chat_id = message.chat.id

    if not is_sensor_is(f"wheel_{id_sensor}"):
        add_sensor_to_wheels(f"wheel_{id_sensor}")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Номер датчика', callback_data=f'add_wheel_num {int(id_sensor)}'))
    btn1 = types.InlineKeyboardButton('🌡 Мин', callback_data=f'add_min {int(id_sensor)} t')
    btn2 = types.InlineKeyboardButton('🌡 Эталон', callback_data=f'add_stand {int(id_sensor)} t')
    btn3 = types.InlineKeyboardButton('🌡 Макс', callback_data=f'add_max {int(id_sensor)} t')
    markup.row(btn1, btn2, btn3)
    btn4 = types.InlineKeyboardButton('🧭 Мин', callback_data=f'add_min {int(id_sensor)} p')
    btn5 = types.InlineKeyboardButton('🧭 Эталон', callback_data=f'add_stand {int(id_sensor)} p')
    btn6 = types.InlineKeyboardButton('🧭 Макс', callback_data=f'add_max {int(id_sensor)} p')
    markup.row(btn4, btn5, btn6)
    btn7 = types.InlineKeyboardButton('Очистить', callback_data=f'clear_wheel {id_sensor}')
    btn8 = types.InlineKeyboardButton('Сохранить', callback_data=f'save_wheel_data {id_sensor}')
    markup.row(btn7, btn8)
    markup.add(
        types.InlineKeyboardButton('Взять данные с предыдущего', callback_data=f'get_data_from_previous {id_sensor}'))
    markup.add(types.InlineKeyboardButton('Назад', callback_data=f'return_without_save {id_sensor}'))

    send_message(chat_id, wheel_text_form(f"wheel_{id_sensor}"), parse_mode='html', reply_markup=markup)
    deleter(chat_id, message.id)


def add_min(message, *args):
    chat_id = message.chat.id

    if args[1] == 't':
        bot.send_message(chat_id, 'Введите минимальную температуру в °С вида 0.0 ', parse_mode='html')
    elif args[1] == 'p':
        bot.send_message(chat_id, 'Введите минимальное давление в Бар вида 0.0 ', parse_mode='html')
    bot.register_next_step_handler(message, min_property, id_sensor=args[0], param=args[1])


def add_max(message, *args):
    chat_id = message.chat.id

    if args[1] == 't':
        bot.send_message(chat_id, 'Введите максимальную температуру в °С вида 0.0 ', parse_mode='html')
    elif args[1] == 'p':
        bot.send_message(chat_id, 'Введите максимальное давление в Бар вида 0.0 ', parse_mode='html')
    bot.register_next_step_handler(message, max_property, id_sensor=args[0], param=args[1])


def add_stand(message, *args):
    chat_id = message.chat.id

    if args[1] == 't':
        bot.send_message(chat_id, 'Введите эталонную температуру в °С вида 0.0 ', parse_mode='html')
    elif args[1] == 'p':
        bot.send_message(chat_id, 'Введите эталонное давление в Бар вида 0.0 ', parse_mode='html')
    bot.register_next_step_handler(message, stand_property, id_sensor=args[0], param=args[1])


def add_sensor_num(message, id_sensor):
    chat_id = message.chat.id

    bot.send_message(chat_id, 'Введите номер датчика этого колеса', parse_mode='html')
    bot.register_next_step_handler(message, sensor_num_property, id_sensor=id_sensor)


def min_property(message, id_sensor, param):
    chat_id = message.chat.id

    text = message.text
    if param == 't':
        send_message(chat_id, f'Минимальная температура {text}°С установлена')
    elif param == 'p':
        send_message(chat_id, f'Минимальное давление {text}Бар установлено')

    add_data_to_wheel(f"wheel_{id_sensor}", f"min_{param}", float(text))

    sensor_settings(message, id_sensor)


def max_property(message, id_sensor, param):
    chat_id = message.chat.id

    text = message.text
    if param == 't':
        send_message(chat_id, f'Максимальная температура {text}°С установлена')
    elif param == 'p':
        send_message(chat_id, f'Максимальное давление {text}Бар установлено')

    add_data_to_wheel(f"wheel_{id_sensor}", f"max_{param}", float(text))

    sensor_settings(message, id_sensor)


def stand_property(message, id_sensor, param):
    chat_id = message.chat.id

    text = message.text
    if param == 't':
        send_message(chat_id, f'Эталонная температура {text}°С установлена')
    elif param == 'p':
        send_message(chat_id, f'Эталонное давление {text}Бар установлено')

    add_data_to_wheel(f"wheel_{id_sensor}", f"standard_{param}", float(text))

    sensor_settings(message, id_sensor)


def sensor_num_property(message, id_sensor):
    chat_id = message.chat.id

    text = message.text
    send_message(chat_id, f'Номер датчика этого колеса {text} установлен')

    add_data_to_wheel(f"wheel_{id_sensor}", "sensor_num", int(text))

    sensor_settings(message, id_sensor)


def get_data_from_previous(message, id_sensor):
    wheel = is_someone_wheel()
    for i in wheel:
        add_data_to_wheel(f"wheel_{id_sensor}", i, wheel[i])

    add_data_to_wheel(f"wheel_{id_sensor}", "sensor_num", None)

    sensor_settings(message, id_sensor)


def check_result(message):
    chat_id = message.chat.id
    get_result()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Назад', callback_data=f'create_wheels_formula'))

    with open("canvas_with_gradient_squares.png", 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=markup)

    deleter(chat_id, message.id)


def save_wheels_formula(message):
    chat_id = message.chat.id
    del_car_reg_log(chat_id)
    send_message(chat_id, 'Машина успешно сохранена')
    main_message(message)


def save_wheel_data(message, id_sensor):
    global lst

    chat_id = message.chat.id

    if is_wheel_ok(f"wheel_{id_sensor}"):
        lst[int(id_sensor) - 1] = '✅'
        send_message(chat_id, 'Данные добавлены успешно ✅.')
        create_wheels_formula(message)
    else:
        send_message(chat_id, 'Чтобы сохранить, нужно заполнить все данные')


def clear_wheel(message, id_sensor):
    global lst

    chat_id = message.chat.id
    lst[int(id_sensor) - 1] = ' '

    if is_sensor_is(f"wheel_{id_sensor}"):
        del_sensor_from_wheels(f"wheel_{id_sensor}")

    create_wheels_formula(message)
    deleter(chat_id, message.id)


def return_without_save(message, id_sensor):
    global lst

    if not is_wheel_ok(f"wheel_{id_sensor}"):
        lst[int(id_sensor) - 1] = ' '
        del_sensor_from_wheels(f"wheel_{id_sensor}")

    create_wheels_formula(message)


@bot.message_handler(func=lambda message: message)
def deleter(chat_id, message_id, num=10):
    deleter_message(chat_id, message_id, num)


bot.infinity_polling()
