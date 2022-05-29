import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты цену которой хотите узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def valued(message: telebot.types.Message):
    text = 'Доступные для перевода валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
           raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
         bot.reply_to(message, f'Ощибка пользователя!\n{e}')

    except Exception as e:
         bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
         text = f'Цена {amount} {quote} в {base} = {total_base*int(amount)} {base}.'
         bot.send_message(message.chat.id, text)

bot.polling()