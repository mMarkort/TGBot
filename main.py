import requests
import telebot as tg
from telebot import types
import camelot
import pandas
import numpy
import re
from bs4 import BeautifulSoup


bot = tg.TeleBot('6420204074:AAF7qvPiPw8dDrDKVSTl9walEhuGIfHspS4')


def get_teach_cabs(teacher):
    url = 'http://www.fa.ru/org/spo/kip/Documents/raspisanie/%D0%90%D0%A3%D0%94%D0%98%D0%A2%D0%9E%D0%A0%D0%98%D0%982.pdf'
    response = requests.get(url)
    with open('test.pdf', 'wb') as f:
        f.write(response.content)

    url = "http://www.fa.ru/org/spo/kip/Pages/lesson_schedule.aspx"
    req = requests.get(url)
    bs = BeautifulSoup(req.text, features="html.parser")

    temp = bs.find('ul', "flex-item-list")

    table = camelot.read_pdf('test.pdf', pages='all')

    tables = []
    for i in range(table.n):
        tables.append(pandas.DataFrame(table[i].df))

    df = pandas.concat(tables)

    timestr = ""
    for i in range(1, len(df.columns)):
        timestr += df.iloc[0][i]

    time = re.findall("\d\d[:]\d\d[-]\d\d[:]\d\d", timestr)

    dicti = {1: "1 Ð¿Ð°Ñ€Ð°", 2: "2 Ð¿Ð°Ñ€Ð°", 3: "3 Ð¿Ð°Ñ€Ð°", 4: "4 Ð¿Ð°Ñ€Ð°", 5: "5 Ð¿Ð°Ñ€Ð°", 6: "6 Ð¿Ð°Ñ€Ð°", 7: "7 Ð¿Ð°Ñ€Ð°", }
    a = numpy.where(df == teacher)
    cabs = []

    for i in range(1, len(df.columns)):
        if df.iloc[a[0][0]][i] == '':
            continue
        else:
            cabs.append(dicti[i] + " ({})".format(time[i-1]) + "\nÐ“Ñ€ÑƒÐ¿Ð¿Ð°: " + df.iloc[a[0][0]][i] + " Ð°ÑƒÐ´. " + df.iloc[a[0][0] + 1][i])
    string_of_cabs = temp.find('strong').text + "\n"
    for i in cabs:
        string_of_cabs += i + "\n"

    return string_of_cabs


def get_lessons(group):
    url = 'http://www.fa.ru/org/spo/kip/Documents/raspisanie/%d0%90%d0%a3%d0%94%d0%98%d0%a2%d0%9e%d0%a0%d0%98%d0%98.pdf'
    response = requests.get(url)
    with open('test.pdf', 'wb') as f:
        f.write(response.content)

    url = "http://www.fa.ru/org/spo/kip/Pages/lesson_schedule.aspx"
    req = requests.get(url)
    bs = BeautifulSoup(req.text, features="html.parser")

    temp = bs.find('ul', "flex-item-list")

    table = camelot.read_pdf('test.pdf', pages='all')

    tables = []
    for i in range(table.n):
        tables.append(pandas.DataFrame(table[i].df))

    df = pandas.concat(tables)

    timestr = ""
    for i in range(1, len(df.columns)):
        timestr += df.iloc[0][i]

    time = re.findall("\d\d[:]\d\d[-]\d\d[:]\d\d", timestr)

    dicti = {1: "1 Ð¿Ð°Ñ€Ð°", 2: "2 Ð¿Ð°Ñ€Ð°", 3: "3 Ð¿Ð°Ñ€Ð°", 4: "4 Ð¿Ð°Ñ€Ð°", 5: "5 Ð¿Ð°Ñ€Ð°", 6: "6 Ð¿Ð°Ñ€Ð°", 7: "7 Ð¿Ð°Ñ€Ð°", }

    a = numpy.where(df == group.upper())
    cabs = []

    for i in range(len(a[0])):
        cabs.append(dicti[a[1][i]] + " ({})".format(time[a[1][i]-1]) + "\n" + df.iloc[a[0][i]][0] + " " + df.iloc[a[0][i]+1][a[1][i]])
    cabs.sort()
    string_of_cabs = temp.find('strong').text + "\n"
    for i in cabs:
        string_of_cabs += i + "\n"
    return string_of_cabs


@bot.message_handler(commands=['teachcabs'])
def send_teachcabs(message):
    command = message.text.split()
    new_sting_list = command[1:]
    new_sting = ' '.join(new_sting_list)
    if len(command) < 2:
        bot.reply_to(message, 'ÐÐ°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ð¿Ð¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñƒ Ð·Ð°Ð½Ð¾Ð²Ð¾ "/teachcabs Ð¤Ð˜Ðž", Ð½Ð°Ð¿Ñ€Ð¸Ð¼ÐµÑ€: Ð˜Ð²Ð°Ð½ Ð’Ð°ÑÐ¸Ð»ÑŒÐµÐ²Ð¸Ñ‡ ÐŸÑƒÐ¿ÐºÐ¸Ð½ ')
    else:
        try:
            bot.reply_to(message, get_teach_cabs(new_sting))
        except:
            bot.reply_to(message,'ÐÐ°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ð¿Ð¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñƒ Ð·Ð°Ð½Ð¾Ð²Ð¾ "/teachcabs Ð¤Ð˜Ðž", Ð½Ð°Ð¿Ñ€Ð¸Ð¼ÐµÑ€: Ð˜Ð²Ð°Ð½ Ð’Ð°ÑÐ¸Ð»ÑŒÐµÐ²Ð¸Ñ‡ ÐŸÑƒÐ¿ÐºÐ¸Ð½ ')


@bot.message_handler(commands=['cabs'])
def send_cabs(message):
    command = message.text.split()
    new_sting_list = command[1:]
    new_sting = ' '.join(new_sting_list)
    try:
        bot.reply_to(message, get_lessons(new_sting))
    except:
        bot.reply_to(message, 'ÐÐ°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ð¿Ð¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð° ÐºÐ¾Ð¼Ð°Ð½Ð´Ñƒ Ð·Ð°Ð½Ð¾Ð²Ð¾ "/cabs Ð³Ñ€ÑƒÐ¿Ð¿Ð°", Ð½Ð°Ð¿Ñ€Ð¸Ð¼ÐµÑ€: /cabs 4Ð¸ÑÐ¸Ð¿-123 ')


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Ð¡ÑÑ‹Ð»ÐºÐ° Ð½Ð° Ð³Ð¸Ñ‚", url="https://github.com/mMarkort")
    markup.add(button1)
    bot.send_message(message.chat.id, 'ÐŸÑ€Ð¸Ð²ÐµÑ‚ÑÑ‚Ð²ÑƒÑŽ!\nÐÐ°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñƒ "/cabs Ð³Ñ€ÑƒÐ¿Ð¿Ð°", Ñ‡Ñ‚Ð¾Ð±Ñ‹ ÑƒÐ·Ð½Ð°Ñ‚ÑŒ Ñ€Ð°ÑÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ ÐºÐ°Ð±Ð¸Ð½ÐµÑ‚Ð¾Ð², Ð½Ð°Ð¿Ñ€Ð¸Ð¼ÐµÑ€: /cabs 3Ð¾Ð¸Ð±Ð°Ñ-321', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_on_channel(message):
    bot.send_message(chat_id='-1002060083117', text=message.text)


@bot.message_handler(content_types=['photo'])
def send_photo(message):
    bot.send_photo(chat_id='-1002060083117', photo=message.photo[-1].file_id)


@bot.message_handler(content_types=['video'])
def send_video(message):
    bot.forward_message(chat_id='-1002060083117', from_chat_id=message.chat.id, message_id=message.message_id)


bot.infinity_polling()
