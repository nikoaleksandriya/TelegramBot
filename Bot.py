import Config
from Config import choice, send_message, gen_dict, mark_counts_reading, mark_counts_writing, markup_gen
import telebot
from telebot import types

bot = telebot.TeleBot(Config.token)

category_genre_dict = gen_dict(0)
movie_genre_dict = gen_dict(1)
book_genre_dict = gen_dict(2)
series_genre_dict = gen_dict(3)
all_comps_dict = gen_dict(4)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    for item in category_genre_dict:
        markup.add(item)

    send_message(choice(message, 'None', markup), message, markup)

@bot.message_handler(content_types=["text"])
def send_text(message):  
    markup_check = 1 
    if message.text == 'Назад':
        welcome(message)

    elif message.text in category_genre_dict:
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        
        for genre in category_genre_dict[message.text]:
            markup.add(genre)
        markup.add('Назад')

        send_message(choice(message, category_genre_dict, markup), message, markup)
    
    elif message.text in movie_genre_dict:
        markup = types.InlineKeyboardMarkup()

        if len(movie_genre_dict[message.text]) == 0:
            markup_check = 0
        else:
            for comp in movie_genre_dict[message.text]:
                comp = types.InlineKeyboardButton(comp, callback_data = comp)
                markup.add(comp)

        send_message(choice(message, movie_genre_dict, markup_check), message, markup)

    elif message.text in book_genre_dict:
        markup = types.InlineKeyboardMarkup()

        if len(book_genre_dict[message.text]) == 0:
            markup_check = 0
        else:
            for comp in book_genre_dict[message.text]:
                comp = types.InlineKeyboardButton(comp, callback_data = comp)
                markup.add(comp)
            
        send_message(choice(message, book_genre_dict, markup_check), message, markup)

    elif message.text in series_genre_dict:
        markup = types.InlineKeyboardMarkup()
        
        if len(series_genre_dict[message.text]) == 0:
            markup_check = 0
        else:
            for comp in series_genre_dict[message.text]:
                comp = types.InlineKeyboardButton(comp, callback_data = comp)
                markup.add(comp)
            
        send_message(choice(message, series_genre_dict, markup_check), message, markup)
    else:
        send_message(choice(message, 'None', 'None'), message, None)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data in all_comps_dict:
            path_text = 'C:/Users/Нико/Desktop/PythonBot/texts/'
            text = all_comps_dict[call.data][0]

            path_img = 'C:/Users/Нико/Desktop/PythonBot/pics/'
            img = all_comps_dict[call.data][1]
            
            good = '👍 Мне нравится'
            not_good = '👎 Не нравится'
            markup = markup_gen(good, not_good)

            bot.send_photo(call.message.chat.id, photo = open(path_img + img, 'rb'))
            bot.send_message(call.message.chat.id, text = open(path_text + text, 'rb').read(), reply_markup = markup)
        
        else:
            if call.data == 'like':
                mark_counts = mark_counts_reading()
                mark_counts[0] += 1
                mark_counts_writing(mark_counts)

            elif call.data == 'dislike':
                mark_counts = mark_counts_reading()
                mark_counts[1] += 1
                mark_counts_writing(mark_counts)
            
            good = '👍 Мне нравится' + ' ' + str(mark_counts[0])
            not_good = '👎 Не нравится' + ' ' + str(mark_counts[1])
            markup_new = markup_gen(good, not_good)

            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id, reply_markup = markup_new)

if __name__ == '__main__':
    bot.infinity_polling()