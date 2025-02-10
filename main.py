import os
import telebot
import random
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
import db
from db import check, add_user, add_data_user_table, del_data_user_table, select_user_words, select_words

print('Телеграм бот запущен.')


state_storage = StateMemoryStorage()
token='***'
bot = telebot.TeleBot(token, state_storage=state_storage)

class Command:
    ADD_WORD = 'Добавить слово+'
    DELETE_WORD = 'Удалить слово-'
    NEXT = 'Дальше->'

class MyStates(StatesGroup):
    word = State()
    translate_word = State()
    other_words = State()
    adding_new_word = State()
    saving_new_word = State()
    deleting_word = State()

@bot.message_handler(commands=['start'])
def start_bot(message):
    cid = message.chat.id
    name = message.from_user.first_name
    bot.send_message(cid, f"Привет <b>{name}</b>. Начни изучать английский вместе с нами. ", parse_mode="html")
    check(cid)
    create_cards(message)

def create_cards(message):
    cid = message.chat.id
    all_worda = select_user_words([cid]) + select_words()
    words = random.sample(all_worda, 4)
    target_word, translate_word = words[0]
    other_words = [w[0] for w in words[1:]]
    options = other_words + [target_word]
    random.shuffle(options)

    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(option) for option in options]
    buttons.append(types.KeyboardButton(Command.NEXT))
    buttons.append(types.KeyboardButton(Command.ADD_WORD))
    buttons.append(types.KeyboardButton(Command.DELETE_WORD))
    markup.add(*buttons)

    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=MyStates.word)
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data['word'] = target_word
        data['translate_word'] = translate_word
        data['all'] = words

    bot.send_message(cid, f"Выбери перевод слова: \n <b>{translate_word.upper()}</b>", reply_markup=markup, parse_mode="html")

def menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [
        types.KeyboardButton(Command.ADD_WORD),
        types.KeyboardButton(Command.DELETE_WORD),
        types.KeyboardButton(Command.NEXT)
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите дальнейшее действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_word(message):
    create_cards(message)

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word_start(message):
    cid = message.chat.id
    bot.set_state(user_id=message.from_user.id, chat_id=cid, state=MyStates.adding_new_word)
    bot.send_message(cid, "Введите слово на английском и через пробел его перевод:")


@bot.message_handler(state=MyStates.adding_new_word)
def add_translate_word(message):
    cid = message.chat.id
    word = []
    translat = []
    input_text = message.text
    wd_tr = []
    wd_tr.append(input_text)
    x = wd_tr[0].split()
    word.append(x[0])
    translat.append(x[1])

    with bot.retrieve_data(user_id=message.from_user.id, chat_id=cid) as data:
        data['word'] = word
        data['translate_word'] = translat
        add_data_user_table((cid), data['word'], data['translate_word'])
    bot.delete_state(user_id=message.from_user.id, chat_id=cid)
    menu(cid)

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word_start(message):
    cid = message.chat.id

    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=MyStates.deleting_word)
    bot.send_message(cid, "Введите слово, которое хотите удалить, на английском:")


@bot.message_handler(state=MyStates.deleting_word)
def delete_word(message):
    cid = message.chat.id
    del_word = []
    input_text = message.text
    del_word.append(input_text)
    del_data_user_table(cid, del_word)
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
    menu(cid)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    user_response = message.text.strip()
    state = bot.get_state(user_id=message.from_user.id, chat_id=message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data.get('target_word')
        translate_word = data.get('translate_word')
        attempts = data.get('attempts', 0)
        c = data['all']

    wr = []
    tr = []
    for x in c:
        wr.append(x[0])
        tr.append(x[1])
    ob = {o: s for o, s in zip(wr, tr)}
    if ob[user_response] == translate_word:
        bot.send_message(message.chat.id, f"Отлично! Идём дальше.")
        create_cards(message)
    else:
        bot.send_message(message.chat.id, f"Ошибка! Попробуйте еще раз.")














bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)