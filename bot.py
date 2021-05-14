import telebot
import logging
from telebot import types
import datetime
from time import sleep
from os import environ  
from flask import Flask, request
from modules.data_trat import join_titles_and_schedules
from modules.html_scraping import prog_date_extract
from modules.date_formating import date_convert_ptbr



logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


API_TOKEN = environ['CINE_BOT_TOKEN']
WEBHOOK_URL_PATH = f"https://api.telegram.org/bot{API_TOKEN}/setWebhook?url="

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)


command_text_words_list = ['programação','programacao', 'horarios','horáios', 'filmes', 
                            'start', 'olá', 'ola', 'olaa','oi', 'oii', 'oiê',
                            'bom dia', "bom diaa","boa tarde", 'bom diaa',
                            "boa noite", "boa noitee", "sessoes", "sessões", 'sessão', 'sessao']


def message_tele_verify(message_from_client):

    message = str(message_from_client).lower()

    is_msg_in_list = bool

    for word in command_text_words_list:
        if word in message:
            is_msg_in_list = True
            break
        else:
            is_msg_in_list = False

    return is_msg_in_list


@bot.message_handler(commands=command_text_words_list)
def send_welcome(message):

    formated_date = date_convert_ptbr()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for day in formated_date:
        markup.row(types.KeyboardButton(day))

    bot.reply_to(
    message,
    f'Olá, <strong>{message.from_user.first_name}</strong>. Que bom te ver por aqui!'
    '\n\nEu sou 🤖 do <strong>Topázio Cinemas</strong> e irei te ajudar a encontrar os horários dos filmes 😁.'
    '\n\nVamos lá!'
    '\n\nEscolha um dia de programação:',
    parse_mode='HTML',reply_markup=markup)
    print(message.text, message.message_id)

@bot.message_handler(content_types=['text'])
def reply(message):

    message_text_verified = message_tele_verify(message.text)

    hideBoard = types.ReplyKeyboardRemove(selective=False)
    formated_date = date_convert_ptbr()
    date_list = prog_date_extract()

    if message.text in formated_date:

        index_date = formated_date.index(message.text)
        prog = join_titles_and_schedules(date_list[index_date])

        for movie in prog:
            bot.send_message(
                message.chat.id, f'{movie}', reply_markup=hideBoard, parse_mode='HTML')
            sleep(.1)

    elif message_text_verified and message.text not in formated_date:
        send_welcome(message)

    elif not message_text_verified and message.text not in formated_date:
        bot.reply_to(
        message, 
        f'Não consegui entender, <strong>{message.from_user.first_name}</strong> 😞. Vamos tentar novamente!'
        '\n\nPara receber a programação clique ou toque aqui  ➡️   /filmes'
        '\n\nEspero ter ajudado! Até a próxima.  🎞️ ☺️',
                            reply_markup=hideBoard, parse_mode='HTML')


@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
