import os
import sqlite3


import telebot
from PIL import Image
from fpdf import FPDF
from  telebot import types

from Celery import config

bot = telebot.TeleBot(config.token)

#status message:
#0 - wait quiz
#1 - thinhing
#2 - making
def executebd(c):
    try:
        print(c)
        conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
        db = conn.cursor()
        db.execute(c)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def tel_sent_all(text):
    conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
    db = conn.cursor()
    subs = db.execute("""
                           SELECT `tel_id` FROM T_bot_subscriber WHERE status_message=0
                        """).fetchall()
    conn.commit()
    conn.close()
    for s in subs:
        bot.send_message(s[0], text)
    return True
#
def tel_sent_docs(id):
    pdf = FPDF()

    path = r"..\files\photos\{}".format(id)
    try:
        imagelist = os.listdir(path)
        # imagelist is the list with all image filenames
        for image in imagelist:
            if image.find('.pdf'):
                continue
            cover = Image.open(path + '\\' + image)
            width, height = cover.size
            pdf.add_page()
            pdf.image(path + '\\' + image, 10, 10, min(width / 5, 206), min(height / 5, 290))
        pdf.output(path + '\\'"ans.pdf", "F")

        conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
        db = conn.cursor()
        subs = db.execute("""
                               SELECT `tel_id` FROM T_bot_subscriber WHERE status_message=0
                            """).fetchall()
        conn.commit()
        conn.close()

        for s in subs:
            doc = open(path + '\\'"ans.pdf", 'rb')
            bot.send_document(s[0], doc)

    except Exception as e:
        print(e)
    return True


def tel_sent_quizs(text):
    st = text.split(';')


    conn = sqlite3.connect("../db.sqlite3")  # или :memory: чтобы сохранить в RAM
    db = conn.cursor()
    subs = db.execute("""
                       SELECT `tel_id` FROM T_bot_subscriber WHERE status_message=0
                    """).fetchall()
    qid=db.execute("""
                       SELECT MAX(id)  FROM T_bot_card
                    """).fetchall()[0][0]
    conn.commit()
    conn.close()

    i=0
    for s in subs:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Done', callback_data='/done')
        button.OneTimeKeyboard = True
        markup.add(button)

        bot.send_message(s[0], st[i], reply_markup=markup)
        executebd("""
                    INSERT INTO T_bot_question (`qstID`,`text`,`subsID`,answer) VALUES({},'{}',{},' ')
                """.format(qid, st[i], s[0]))

        executebd("""
            UPDATE T_bot_subscriber SET  status_message=1, quis_now={} WHERE `tel_id`={}
        """.format(qid,s[0]))

        i+=1

    return 0