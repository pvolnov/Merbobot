from telebot import types

from models import *
import telebot
from config import *
bot = telebot.TeleBot(tel_token)

def new_mes(text):

    for u in Users.select():
        bot.send_message(u.tel_id,text)

def send_to(mid,text):
    telid=Users.get(Users.efka_id==mid).tel_id
    bot.send_message(telid,text)

def new_shop(lat,lon,name):
    s=Shops(latitude=lat,longitude=lon,name=name)
    s.save()

def new_quiz(text,answers):
    q=Quiz(text=text,answers=answers)
    q.save()
    qid=Quiz.select()[-1].id

    ans=answers.split(';')



    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=ans[0], callback_data='ans1')
    button2 = types.InlineKeyboardButton(text=ans[1], callback_data='ans2')
    button3 = types.InlineKeyboardButton(text=ans[2], callback_data='ans3')
    button4 = types.InlineKeyboardButton(text=ans[3], callback_data='ans4')

    markup.row(button, button2)
    markup.row(button3, button4)


    for u in Users.select().where(Users.qid==-1):
        u.qid=qid
        u.save()
        bot.send_message(u.tel_id,
                         text, reply_markup=markup)
