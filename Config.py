token = '1641103903:AAF7kijmUmMA238laaKbjtKaBf10h5X1qqc'

import telebot
from telebot import types

bot = telebot.TeleBot(token)

def gen_dict(dict_type):
    local_dict = {}

    if dict_type == 0:
        a = 'C:/Users/Нико/Desktop/PythonBot/items.txt'
    elif dict_type == 1:
        a = 'C:/Users/Нико/Desktop/PythonBot/comps/movie_comp.txt'
    elif dict_type == 2:
        a = 'C:/Users/Нико/Desktop/PythonBot/comps/.book_comp.txt'
    elif dict_type == 3:
        a = 'C:/Users/Нико/Desktop/PythonBot/comps/`series_comp.txt'
    elif dict_type == 4:
        a = 'C:/Users/Нико/Desktop/PythonBot/All_Comps.txt'

    with open(a, 'r', encoding='utf-8-sig') as comp:
        compositions = comp.readlines()

    for i in range(len(compositions)):
        compositions[i] = compositions[i].split(',')
        compositions[i].pop()

    for i in range(len(compositions)):
        for j in range(len(compositions[i])):
            if j == 0:
                local_dict[compositions[i][j]]= compositions[i][1:]
        
    return local_dict

def choice(message, dict_type, markup_check):
    if message.text == 'Фильм / Movie 🎥':
        return "Рекомендую смотреть фильмы в оригинале и с субтитрами 🇺🇳 Выбери, пожалуйста, жанр"
    elif message.text == 'Книга / Book 📘':
        return "Интересно, сколько книг ты можешь прочитать за год 🤔 Выбери, пожалуйста, жанр"
    elif message.text == 'Сериал / Series 📺':
        return "Полагаю, вечер будет длинным 🍿 Выбери, пожалуйста, жанр"
    elif message.text in dict_type:
        if markup_check == 0: 
            return "К сожалению, пока нет рецензий на произведения этого жанра, но скоро они появятся!"
        else:
            return "Отлично, теперь выбери произведение! После прочтения ты сможешь поставить рецензии лайк, если она тебе понравится 🥰"
    elif message.text == '/start' or message.text == 'Назад':
        return 'Добро пожаловать, ' + message.chat.first_name + '! Здесь ты можешь прочитать рецензии на известные и не очень фильмы, книги и сериалы. Enjoy! ✌'
    else:
        return "Извини, но мне запрещено отвечать на сообщения. Я умею общаться только посредством нажатия на кнопки 😉"

def send_message(users_choice, message, markup):
    return bot.send_message(message.chat.id, users_choice.format(message.from_user, bot.get_me()),
        parse_mode = "Html", reply_markup = markup)

def mark_counts_reading():
    with open('C:/Users/Нико/Desktop/PythonBot/mark_counts.txt', 'r') as mc:
        mark_counts = mc.read().split(',')
        mark_counts = [int(i) for i in mark_counts]
        return mark_counts

def mark_counts_writing(mark_list):
    with open('C:/Users/Нико/Desktop/PythonBot/mark_counts.txt', 'w') as mc:
        mc.write(str(mark_list[0]) + ',' + str(mark_list[1]))

def markup_gen(pos, neg):
    markup = types.InlineKeyboardMarkup(row_width = 2)
    like = types.InlineKeyboardButton(pos, callback_data = 'like')
    dislike = types.InlineKeyboardButton(neg, callback_data = 'dislike')
    markup.row(like, dislike)
    return markup