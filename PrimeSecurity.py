# Импортируем библиотеку Telegram
import telebot
# Импортируем библиотеку MySQL
import pymysql
from datetime import date


# Токен бота. Нужно для подключения кода к боту
bot = telebot.TeleBot('1111935246:AAHX_JegW2HyF7HIAZI8VV-szfrEsUmi3bI')
# Временные переменные
temp_password = '0'
temp_chat_id = None

# Словарь платежей
PAYMENT = dict()
PAYMENT['transaction_id'] = 0
PAYMENT['transaction_type'] = 'defrayal'
PAYMENT['transaction_amount'] = 0
# Словарь сессии
SESSION = dict()
SESSION['is_auth'] = False
SESSION['client_id'] = '000000000'
SESSION['client_contract'] = '00/00/00'
SESSION['client_debt'] = 0
SESSION['client_tariff'] = 0
SESSION['client_recommended_payment'] = SESSION['client_debt'] + SESSION['client_tariff']
SESSION['client_for_year_payment'] = SESSION['client_tariff'] * 0.9


# Создание пользовательской клавиатуры - кнопки меню бота.
# Декоратор обработки команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Устанавливаем параметры клавиатуры:
    # True - оптимизируем клавиатуру по размеру, False - снимаем возможность убрать клавиатуру
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    # В пользовательское меню добавляем кнопки "Войти" и "Стать клиентом"
    user_markup.row('Увійти', 'Стати клієнтом')
    # По команде из декоратора бот отправляет сообщение
    bot.send_message(message.from_user.id, 'Оберіть одну з кнопок нижче.', reply_markup=user_markup)


# Декоратор обработки сообщений
@bot.message_handler(content_types=['text'])
# Внутри декоратора объявляем функцию обработки сообщений
def handle_message(message):
    # Предоставляем функции возможность редактировать глобальную переменную
    global temp_password
    # Если текст сообщения "Войти"
    if message.text == "Увійти":
        # Отправляем сообщение с просьбой ввести лицевой счет
        bot.send_message(message.from_user.id, 'Введіть, будь ласка, свій особовий рахунок')

    # Если сообщение длиной в 9 символов, распознаем его как лицевой счет
    elif len(message.text) == 9:
        # Создаем функцию приема и сохранения пароля, которая принимает значение лицевого счета клиента
        def password_saving(client_id):
            # Функция отправляет сообщение с просьбой ввести пароль
            bot.send_message(message.from_user.id, 'Введіть, будь ласка, свій пароль')
            # Коды доступа к БД MySQL
            link = pymysql.connect('prime00.mysql.tools', 'prime00_clients', '8y&@40oInG', 'prime00_clients')
            # Подключаемся к БД
            with link:
                # Формируем текст запроса fksyf 0676158021 0676155049
                password_query = """SELECT user_password
                                    FROM users
                                    WHERE user_id='""" + client_id + """'"""
                # Присваиваем курсор
                cur = link.cursor()
                # Отправляем запрос со сформированным заранее текстом запроса
                cur.execute(password_query)
                # Результат запроса присваиваем переменной password
                password = cur.fetchone()
                # Результат возвращения функции - переменная password
                return password
        SESSION['client_id'] = message.text
        # Глобальной переменной temp_password присваиваем возвращаемое значение описаной функции
        temp_password = password_saving(message.text)

    # Если текст сообщения совпадает со значением, содержащимся в переменной temp_password
    elif len(message.text) == 10:
        str_correct_password = str(temp_password)
        maybe_password = "('" + message.text + "',)"
        if str_correct_password == maybe_password:
            global temp_chat_id
            temp_chat_id = message.from_user.id
            # Приветствуем клиента в персональном кабинете
            bot.send_message(message.from_user.id, 'Вітаємо в персональному кабінеті! Ви успішно залоговані.')
            # Устанавливаем параметры клавиатуры:
            # True - оптимизируем клавиатуру по размеру, False - снимаем возможность убрать клавиатуру
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            # В пользовательское меню добавляем кнопки "Войти" и "Стать клиентом"
            user_markup.row('Стан рахунку', 'Перейти до оплати')
            user_markup.row('Інформація по рахунку', 'Наші реквізити')
            user_markup.row('Фінансова історія')
            user_markup.row('Контакти', 'Графік роботи')
            user_markup.row('Вийти')

            def client_contract_extracting(client_id):
                # Коды доступа к БД MySQL
                link = pymysql.connect('prime00.mysql.tools', 'prime00_clients', '8y&@40oInG', 'prime00_clients')
                # Подключаемся к БД
                with link:
                    # Формируем текст запроса
                    client_contract_query = """SELECT user_contract_num
                                               FROM users
                                               WHERE user_id='""" + client_id + """'"""
                    # Присваиваем курсор
                    cur = link.cursor()
                    # Отправляем запрос со сформированным заранее текстом запроса
                    cur.execute(client_contract_query)
                    # Результат запроса присваиваем переменной password
                    contract = cur.fetchone()
                    # Результат возвращения функции - переменная password
                    return contract

            def client_tariff_extracting(client_id):
                # Коды доступа к БД MySQL
                link = pymysql.connect('prime00.mysql.tools', 'prime00_clients', '8y&@40oInG', 'prime00_clients')
                # Подключаемся к БД
                with link:
                    # Формируем текст запроса
                    client_contract_query = """SELECT user_tax
                                               FROM users
                                               WHERE user_id='""" + client_id + """'"""
                    # Присваиваем курсор
                    cur = link.cursor()
                    # Отправляем запрос со сформированным заранее текстом запроса
                    cur.execute(client_contract_query)
                    # Результат запроса присваиваем переменной password
                    tariff = cur.fetchone()
                    # Результат возвращения функции - переменная password
                    return tariff[0]

            def client_debt_extracting(client_id):
                # Коды доступа к БД MySQL
                link = pymysql.connect('prime00.mysql.tools', 'prime00_clients', '8y&@40oInG', 'prime00_clients')
                # Подключаемся к БД
                with link:
                    # Формируем текст запроса
                    client_rev_query = """SELECT SUM(transaction_sum)
                                          FROM payment_story
                                          WHERE transaction_client='""" + client_id + """'"""
                    # Присваиваем курсор
                    cur = link.cursor()
                    # Отправляем запрос со сформированным заранее текстом запроса
                    cur.execute(client_rev_query)
                    # Результат запроса присваиваем переменной password
                    rev = cur.fetchone()
                    # Формируем текст запроса
                    client_debt_at_the_start_query = """SELECT user_balance
                                          FROM users
                                          WHERE user_id='""" + client_id + """'"""
                    # Отправляем запрос со сформированным заранее текстом запроса
                    cur.execute(client_debt_at_the_start_query)
                    # Результат запроса присваиваем переменной password
                    debt_at_the_start = cur.fetchone()
                    if rev[0]:
                        result_sum = debt_at_the_start[0] + rev[0]
                    else:
                        result_sum = debt_at_the_start[0] + 0
                    # Результат возвращения функции - переменная password
                    return result_sum

            SESSION['is_auth'] = True
            SESSION['client_contract'] = client_contract_extracting(SESSION['client_id'])
            SESSION['client_tariff'] = client_tariff_extracting(SESSION['client_id'])
            SESSION['client_debt'] = client_debt_extracting(SESSION['client_id'])
            SESSION['client_recommended_payment'] = SESSION['client_debt'] + SESSION['client_tariff']
            SESSION['client_for_year_payment'] = float(SESSION['client_tariff']) * 12 * 0.9

            bot.send_message(message.from_user.id, 'В меню ви можете знайти доступні операції та здійснити оплату', reply_markup=user_markup)
        elif str_correct_password != maybe_password:
            bot.send_message(message.from_user.id, 'Введені дані некоректні! Перевірте пароль та спробуйте ще раз.')
    elif message.text == 'Стан рахунку' and SESSION['is_auth']:
        if SESSION['client_debt'] > 0:
            bot.send_message(message.from_user.id, """Ваша заборгованість: """ + str(SESSION['client_debt']) +
                             """ гривень. Будь ласка, сплатіть її до 10 числа поточного місяця.""")
            bot.send_message(message.from_user.id, 'Рекомендований платіж: ' + str(SESSION['client_recommended_payment']) + ' гривень')
            bot.send_message(message.from_user.id, 'Разовий платіж за рік: ' + str(SESSION['client_for_year_payment']) + ' гривень')
        else:
            bot.send_message(message.from_user.id, 'Шановний клієнте, у вас відсутня заборгованість! ' +
                             'Ваш авансовий платіж: ' + str(SESSION['client_debt']) +
                             ' гривень. Дякуємо, що вчасно сплачуєте рахунки!')
            bot.send_message(message.from_user.id, 'Разовий платіж за рік: ' + str(SESSION['client_for_year_payment']) + ' гривень')
    elif message.text == 'Інформація по рахунку' and SESSION['is_auth']:
        bot.send_message(message.from_user.id, 'Ваш особовий рахунок: ' + str(SESSION['client_id']))
        bot.send_message(message.from_user.id, 'Ваш номер договору: ' + str(SESSION['client_contract']).replace('(','').replace("'",'').replace(',','').replace(')',''))
        bot.send_message(message.from_user.id, 'Сума щомісячного платежу: ' + str(SESSION['client_tariff']) + ' гривень')
    elif message.text == 'Наші реквізити' and SESSION['is_auth']:
        bot.send_message(message.from_user.id, 'ТОВ "Прайм Секьюріті"')
    elif message.text == 'Фінансова історія' and SESSION['is_auth']:
        def payment_extracting(client_id):
            # Коды доступа к БД MySQL
            link = pymysql.connect('prime00.mysql.tools', 'prime00_clients', '8y&@40oInG', 'prime00_clients')
            # Подключаемся к БД
            with link:
                # Формируем текст запроса
                query_4_countcheck = "SELECT transaction_id FROM payment_story WHERE transaction_client='" + client_id + "' ORDER BY transaction_id DESC LIMIT 10"
                query_id = "SELECT transaction_id FROM payment_story WHERE transaction_client='" + client_id + "' ORDER BY transaction_id DESC"
                query_datetime = "SELECT transaction_datetime FROM payment_story WHERE transaction_client='" + client_id + "' ORDER BY transaction_id DESC"
                query_type = "SELECT transaction_type FROM payment_story WHERE transaction_client='" + client_id + "' ORDER BY transaction_id DESC"
                query_sum = "SELECT transaction_sum FROM payment_story WHERE transaction_client='" + client_id + "' ORDER BY transaction_id DESC"
                cur = link.cursor()
                cur.execute(query_4_countcheck)
                countcheck = cur.fetchall()
                # Присваиваем курсор
                cur = link.cursor()
                # Отправляем запрос со сформированным заранее текстом запроса
                cur.execute(query_id)
                # Результат запроса присваиваем переменной password
                payment_ids = cur.fetchall()
                cur.execute(query_datetime)
                # Результат запроса присваиваем переменной password
                payment_datetimes = cur.fetchall()
                cur.execute(query_type)
                # Результат запроса присваиваем переменной password
                payment_types = cur.fetchall()
                cur.execute(query_sum)
                # Результат запроса присваиваем переменной password
                payment_sums = cur.fetchall()
                # Результат возвращения функции - переменная password
                i = 0
                while i < len(countcheck):
                    bot.send_message(message.from_user.id, 'id: ' + str(payment_ids[i]).replace('(','').replace(',','').replace(')','') + ''', 
дата: ''' + str(payment_datetimes[i]).replace('(','').replace(',','').replace(')','').replace('d','').replace('a','').replace('t','').replace('e','').replace('i','').replace('m','').replace('.','').replace(' ','-').replace('-0-0','') + ''',
тип транзакції: ''' + str(payment_types[i]).replace('(','').replace(',','').replace(')','').replace("'",'').replace('nachislenie','нарахування').replace('oplata schota','оплата') + ''', 
сума: ''' + str(payment_sums[i]).replace('D','').replace('e','').replace('c','').replace('i','').replace('m','').replace('a','').replace('l','').replace('(','').replace("'",'').replace(')','').replace(',','') + ' гривень')
                    i = i + 1
        bot.send_message(message.from_user.id, 'Останні транзакції:')
        payment_extracting(SESSION['client_id'])
    elif message.text == 'Вийти' and SESSION['is_auth']:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # В пользовательское меню добавляем кнопки "Войти" и "Стать клиентом"
        user_markup.row('Увійти', 'Стати клієнтом')
        bot.send_message(message.from_user.id, 'Ви успішно вийшли з персонального кабінету!', reply_markup=user_markup)
        SESSION['is_auth'] = False
        SESSION['client_id'] = None
        SESSION['client_contract'] = None
        SESSION['client_debt'] = None
        SESSION['client_tariff'] = None
        SESSION['client_recommended_payment'] = None
        SESSION['client_for_year_payment'] = None
    elif message.text == 'Контакти' and SESSION['is_auth']:
        bot.send_message(message.from_user.id, 'Бухгалтерія: 066-597-95-18')
        bot.send_message(message.from_user.id, 'Гаряча лінія: 067-323-80-08')
        bot.send_message(message.from_user.id, 'admin@prime.net.ua')
        bot.send_message(message.from_user.id, 'с. Петропавлівська Борщагівка ЖК «Львівський», вул. Миру 11')
    elif message.text == 'Графік роботи' and SESSION['is_auth']:
        bot.send_message(message.from_user.id, '''Понеділок: 09:00-18:00
Вівторок: 09:00-18:00
Середа: 09:00-18:00
Четвер: 09:00-18:00
П'ятниця: 09:00-18:00

Субота: вихідний
Неділя: вихідний

13:00-14:00 - обід''')
    today = date.today()
    if today.day == 1 and SESSION['is_auth'] and SESSION['client_debt'] > 0:
        bot.send_message(message.from_user.id, 'Шановний клієнте, будь ласка, не забудьте сплатити рахунок до 10 числа поточного місяця')
    if today.day == 10 and SESSION['is_auth'] and SESSION['client_debt'] > 0:
        bot.send_message(message.from_user.id, 'Шановний клієнте, нагадуємо, сьогодні останній день для внесення щомісячного платежу. В разі несплати ми залишаємо за собою право припинити обслуговування до отримання оплати.')


# Команда на непрерывное исполнение программы, чтобы бот не отключался по достижению последней строки
bot.polling(none_stop=True)
