import datetime
import json
import logging
import os
import time

import requests
import telebot
from flask import Flask, request
from telebot import types, util

import connector
import settings
from reddit import RedditAPI

START, SEARCH_STRING, SUBREDDIT_CHOSEN, ADD_PHOTO, IS_LOCATION_NEEDED, ADD_LOCATION, END = range(7)

token = settings.bot_token
bot = telebot.TeleBot(token)

IS_REDIS = True
connection = connector.RedisConnector()
redditApi = RedditAPI()


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="find", callback_data="find_action"),
               types.InlineKeyboardButton(text="add", callback_data="add_action"),
               types.InlineKeyboardButton(text="list", callback_data="list_action"),
               types.InlineKeyboardButton(text="remove", callback_data="reset_action")]
    keyboard.add(*buttons)
    return keyboard


def create_yes_no_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text="Yes", callback_data="yes"),
               types.InlineKeyboardButton(text="No", callback_data="no")]
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
def handle_start_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id,
                     text="Hello. \n"
                          "Please use the following commands: \n"
                          "/find   to find the reddit channel \n"
                          "/add    to add known reddit channel \n"
                          "/list   to see you subscribers \n"
                          "/remove to remove your redit channel from subscribers",
                     reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda
        callback_query: callback_query.data == 'add_action' or callback_query.data == 'list_action' or callback_query.data == 'reset_action' or callback_query.data == 'find_action')
def handle_initial_commands(callback_query):
    if callback_query.data == 'add_action':
        handle_add_command(callback_query.message)
    elif callback_query.data == 'list_action':
        pass
    elif callback_query.data == 'find_action':
        handle_find_command(callback_query.message)
    elif callback_query.data == 'reset_action':
        pass


@bot.message_handler(commands=['find'])
def handle_find_command(message):
    connection.update_state(message.chat.id, SEARCH_STRING)
    bot.send_message(chat_id=message.chat.id, text="Input subreddit title")


@bot.message_handler(func=lambda message: connection.get_state(message.chat.id) == SEARCH_STRING)
def handle_search_string(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []

    connection.update_state(message.chat.id, SUBREDDIT_CHOSEN)

    subreddit_list = redditApi.search_subreddits(message.text)
    for subreddit in subreddit_list:
        buttons.append(
            types.InlineKeyboardButton(text="{} [{}]".format(subreddit["name"], subreddit["subscriber_count"]),
                                       callback_data=subreddit["name"]))
    keyboard.add(*buttons)

    bot.send_message(chat_id=message.chat.id,
                     text="Which subbreddit you would like to add?",
                     reply_markup=keyboard, parse_mode='HTML')


@bot.callback_query_handler(func=lambda message: connection.get_state(message.message.chat.id) == SUBREDDIT_CHOSEN)
def handle_subreddit_choosen(callback_query):
    message = callback_query.message
    subreddit_name = callback_query.data

    post_list = redditApi.get_last_posts_from_subreddit(subreddit_name)

    for item in post_list:
        date = datetime.datetime.fromtimestamp(int(item["created"]))
        date = date.strftime('%d-%m-%Y %H:%M:%S')

        # result_message = "<b>{}</b>\n".format(item["title"])
        result_message = ""

        url = get_gif_url_from_item_url(item["url"])
        if url and (url.endswith(".gif") or url.endswith(".mp4")):
            result_message += "<a href='{}'>{}</a>".format(url, "View on Reddit")
            result_message += "  {}\n".format(date)
            # result_message += "{}\n".format(item["text"])

            if len(result_message) > 4000:
                splitted_text = util.split_string(result_message, 4000)
                for text in splitted_text:
                    bot.send_message(message.chat.id, text, False, parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, result_message, False, parse_mode="HTML")
            time.sleep(1)


def get_gif_url_from_item_url(url: str):
    url = url.replace(".gifv", ".mp4")
    if url.endswith(".gif") or url.endswith(".mp4"):
        return url
    elif "gfycat.com" in url:
        src_name = url.split("gfycat.com/")[-1]
        response = requests.get("http://gfycat.com/cajax/get/{}".format(src_name))
        # Telegram does not show big GIFs, so try to get small version if presents
        try:
            gif_url = response.json()["gfyItem"].get('max5mbGif', response.json()["gfyItem"]["gifUrl"])
        except json.decoder.JSONDecodeError:
            return None
        return gif_url
    elif "imgur.com" in url and url.split("/")[-1].count('.') == 0:
        if requests.get(url + ".mp4").status_code == 200:
            return url + ".mp4"
        else:
            return None


@bot.message_handler(func=lambda message: connection.get_state(message.chat.id) == SUBREDDIT_CHOSEN)
def handle_find_command(message):
    connection.update_state(message.chat.id, SEARCH_STRING)
    handle_search_string(message)


@bot.message_handler(commands=['add'])
def handle_add_command(message):
    text = message.text.split(" ")


@bot.callback_query_handler(func=lambda message: connection.get_state(message.message.chat.id) == IS_REDIS)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        connection.update_state(message.chat.id, ADD_PHOTO)
        bot.send_message(message.chat.id, text='Пожалуйста загрузите фото')
    else:
        keyboard = create_yes_no_keyboard()
        connection.update_state(message.chat.id, IS_LOCATION_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                         reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def handle_message(message):
    messages_list = []
    for item in messages_list:
        date = datetime.datetime.fromtimestamp(int(item["created"]))
        date = date.strftime('%d-%m-%Y %H:%M:%S')

        result_message = "<b>{}</b>\n".format(item["title"])
        result_message += "<a href='{}'>{}</a>".format(item["url"], "View on Reddit")
        result_message += "  {}\n".format(date)
        # result_message += "{}\n".format(item["text"])

        if len(result_message) > 4000:
            splitted_text = util.split_string(result_message, 4000)
            for text in splitted_text:
                bot.send_message(message.chat.id, text, False, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, result_message, False, parse_mode="HTML")


if __name__ == '__main__':
    if "HEROKU" in list(os.environ.keys()):

        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)
        server = Flask(__name__)


        @server.route("/bot", methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200


        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(
                url="https://curserabot.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения
            return "?", 200


        server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    else:
        # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
        # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
        bot.remove_webhook()
        bot.polling(none_stop=True)
