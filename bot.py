from  telebot import*#импорт библиотеки telebot
import pandas as pd #импорт библиотеки pandas для работы с файлом(расписанием)
import sqlite3 #импорт библиотеки sqlite3
f=pd.read_csv('7.csv',encoding='1251',delimiter=';') #создание переменной f для чтения файла расписания библиотекой pandas 
f=f.set_index('дни') #
keyboard1=types.InlineKeyboardMarkup() #создание клавиатуры
days=['понедельник','вторник','среда','четверг','пятница','суббота','изменить класс'] # создание переменной days для кнопок чат-бота
for i in days:
    keyboard1.add(types.InlineKeyboardButton(text=i, callback_data=f'{i}'))
bot = telebot.TeleBot('6060380118:AAFWaXBNZOSRnk5oFWxKzGBCiPk9F96oV6w') # переменная чат-бота,в скобках записан токен чат-бота

@bot.callback_query_handler(func=lambda query: True)             #функция работоспособности клавиатуры
def days(query):
    if query.data=='изменить класс':  #при нажатии на изменить класс,бот присылает сообщение человеку "введите ваш класс"
        bot.send_message(query.message.chat.id, "Введите ваш класс")

        bot.register_next_step_handler(query.message,echo) #бот запоминает(регистрирует ) то значение,которое введет человек

    else:   
        con = sqlite3.connect('schedule.db') #соединение библиотекb sqlite3 с файлом  schedule.db
        cur = con.cursor() #cur-курсор соединения
        #print(f.loc[query.data,['время',result_list[0]]].to_string(header=False, index=False))
        cur.execute(f'select class from schedule where id_telegram=={query.from_user.id}')     #вывод класса опр человека
        results = cur.fetchall() #таблица  результата запроса записывается в переменную  
        result_list = [row[0] for row in results] #записываем класс в массив
        answer=f.loc[query.data,['время',result_list[0]]].to_string(header=False, index=False, justify='left').replace('NaN',' ')#формирование ответа пользователю с расписанием на конкретный день недели
        bot.send_message(query.message.chat.id,answer, reply_markup=keyboard1)
       # bot.edit_message_text(answer, query.message.chat.id, query.message.message_id, reply_markup=keyboard1)











# Замените 'YOUR_BOT_TOKEN' на токен вашего бота


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message): #
    con = sqlite3.connect('schedule.db') #переменная соn-соединение с библиотекой sqlite3
    cur = con.cursor() #cur-курсор соединения
    
    bot.send_message(message.chat.id, "Введите ваш класс") #бот присылает сообщ "введите ваш класс"

    bot.register_next_step_handler(message,echo) #ждет ответа от  пользователя и переходит в функцию ввода класса
# Обработчик текстовых сообщений
#@bot.message_handler(func=lambda message: True)
def echo(message): #функция длдя ввода класса
    k=sqlite3.connect('schedule.db') #переменная к -соединение с файлом schedule.db 
    c=k.cursor() #переменная с-курсор
    c.execute(f"delete FROM schedule WHERE id_telegram == {message.chat.id}") #удаление из базы данных класса пользователя
    k.commit() #сохранение результатов выполнения запрпоса
    a=message.text
    a=a.replace(' ','')       #исправление ошибок при вводе класса
    a=a.capitalize()
    if a in ['5а',	'5б',	'5в',	'6а',	'6б',	'6в',	'6г',	'7а',	'7б',	'7в',	'8а',	'8б',	'8в',	'9а',	'9б',	'9в',	'10а',	'10б',	'11а',	'11б']:

        v='insert into schedule (id_telegram, class) values (?,?)' #вст id телеграма и класс пользователя
        d=(message.chat.id,a) #аргументы запроса(вместо ?)
        c.execute(v,d) #
        k.commit() #сохрангение рез-ов
        bot.send_message(message.chat.id,'выберите день недели',reply_markup=keyboard1) # клавиатура с днями недели
    else:
        bot.send_message(message.chat.id,'класс не найден') #в остальных случаях бот присылает сообщение "класс не найден"
        bot.register_next_step_handler(message,echo) #бот продолжает работу с другим классом,который введет человек

# Запуск бота
bot.polling()

