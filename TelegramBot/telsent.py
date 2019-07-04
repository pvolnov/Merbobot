# -*- coding: utf-8 -*-
import datetime
import random
import sys

sys.path.append('../')

from config import *
from models import *

import telebot
from  telebot import types
from TelegramBot.supfile import *


def log(txt):
    print(txt)

bot = telebot.TeleBot(tel_token)
base_keyboard = types.ReplyKeyboardMarkup( resize_keyboard=True)
base_button_1 = types.KeyboardButton(text="Get Balanse")
base_button_2 = types.KeyboardButton(text="Get Card Cod")
base_keyboard.row(base_button_1, base_button_2)

#Suppurt Fancs
def add_bal(chat_id,k=1):
    bal = random.randint(8, 15)
    bot.send_message(chat_id=chat_id, text="Спасибо, вам начислено: " + str(int(bal*k)) + " баллов")

    user = Users.select().where(Users.tel_id == chat_id)[0]
    user.balance += bal
    user.save()

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        lat=message.location.latitude
        lot=message.location.longitude

        print("latitude: %s; longitude: %s" % (lat,lot))
        shops=Shops.select()
        sname=shops[0].name
        dl=abs(shops[0].latitude-lat) + abs(shops[0].longitude-lot)

        for shop in shops:
            dl2 = abs(shop.latitude - lat) + abs(shop.longitude - lot)
            if(dl2<dl):
                dl=dl2
                sname = shop.name

        print(sname)
        #Сохраним информацию о магазине
        inf = Info.select().where(Info.user_id==message.chat.id)[-1]
        inf.shopname=sname
        inf.save()

        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         "Принято 🌏",  reply_markup=base_keyboard)

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='No', callback_data='/geofalse')
        button2 = types.InlineKeyboardButton(text='Yes', callback_data='/geotrue')
        markup.row(button,button2)

        bot.send_message(message.chat.id,
                         "Выш магазин: "+sname+"?", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        bot.reply_to(message, "Обработка..")

        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        path="../res/photos/"
        photo_name=str(message.chat.id)+"_"+str(message.message_id)+'.jpg'

        out = open(path+photo_name, "wb")
        out.write(downloaded_file)
        out.close()
        import ml
        stat=ml.get_arrage_status(path+photo_name)

        log("Добавлено фото:" +str(message.from_user.last_name))
        #Создадим запись о добавлении информации
        Dset(name=photo_name, stutus=-1).save()

        bot.send_message(message.chat.id, "[test] Качество: "+str(stat))
        if(stat<7):
            bot.send_message(message.chat.id, "Майонез не найден, отправьте фото еще раз")
            return 0

        inf=Info(shopname="none",datatime=datetime.datetime.now() , user_id=message.chat.id,
             status=stat,photo_name=photo_name).save()#Status - состояние полки по мнению нейросети



        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение 🌏.", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста ваше местоположение, что бы мы могли определить, в каком магазине вы находитесь",
                         reply_markup=keyboard)


        #bot.reply_to(message, "Обработка..")

    except Exception as e:
        log( e)
        bot.send_message(message.chat.id,"[test] Качество: 0")

@bot.message_handler(commands=['admin_'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    print(message.chat.id)
    log("Стал админом :" + str(message.from_user.last_name))
    bot.send_message(message.chat.id, "Получены права суперпользователя")

#Start Fanction
@bot.message_handler(commands=['start'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе

    if len( Users.select().where(Users.tel_id==message.chat.id) )==0:
        u = Users( tel_id=message.chat.id, name=str(message.from_user.last_name),
                   balance=0,mes_stat=0,efka_id=random.randint(10000000,99999999),true_ans_now=-1)
        u.save()
        bot.send_message(message.chat.id, hello_text,reply_markup=base_keyboard)
    else:
        u=Users.select().where(Users.tel_id==message.chat.id)[0]
        print(u.tel_id)
        bot.send_message(message.chat.id, "Вы уже с нами.",reply_markup=base_keyboard)



@bot.callback_query_handler(func=lambda call: True)
def repeat_all_messages(call):
    if call.from_user:
        log('callbac'+call.data)

        if call.data == "/geofalse":
            inf=Info.select().where(Info.user_id==call.message.chat.id)[-1]
            inf.shopname="none"
            inf.save()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Пришлите название магазина")

            user=Users.select().where(Users.tel_id==call.message.chat.id)[0]
            user.mes_stat=1
            user.save()

        elif call.data == "/geotrue":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Геопозиция подтверждена")
            add_bal(call.message.chat.id)

        elif call.data in ['ans1','ans2','ans3','ans4']:
            ans=['ans1','ans2','ans3','ans4'].index(call.data)#Узнаем номер ответа
            u=Users.select().where(Users.tel_id==call.message.chat.id)[0]
            qid=u.qid
            u.qid=-1
            u.save()
            try:
                q=Quiz.select().where(Quiz.id==qid)[0]
                r=q.results.split(';')
                r[ans]=str( int(r[ans])+1 )
                q.results=r[0]+';'+r[1]+';'+r[2]+';'+r[3]
                q.save()

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбран правильный ответ, поздравляю")
                add_bal(call.message.chat.id)
            except Exception as e:
                print(e)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Вопрос уже удален, надо отвечать быстрее")




@bot.message_handler(content_types=["text"])
#обработка ответа от участника
def repeat_all_messages(message):
    if(message.text=="Get Balanse"):
        ef_id=Users.get(Users.tel_id==message.chat.id).efka_id

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Получить подарок', url=host+'users/'+str(ef_id))
        markup.row(button)
        b=Users.select().where(Users.tel_id==message.chat.id)[0]
        bot.send_message(message.chat.id, str(b.balance)+" баллов",reply_markup=markup)

    elif (message.text == "Get Card Cod"):
        b = Users.select().where(Users.tel_id == message.chat.id)[0]
        try:
            f=make_barcode(b.efka_id)
            f.save('qr')
        except:
            pass
        qr=open('qr.png','rb')
        bot.send_photo(message.chat.id, qr)
    else:
        bot.send_message(message.chat.id, "Я не отвечаю на сообщения")
        return
        user=Users.select().where(Users.tel_id==message.chat.id)[0]
        if(user.mes_stat==1):
            user.mes_stat=0
            inf=Info.select().where(Info.user_id==message.chat.id)[-1]
            inf.shopname=message.text
            inf.save()
            bot.send_message(message.chat.id,"Название добавлено")
            add_bal(message.chat.id)


    log(str(message.from_user.last_name)+' : '+message.text)

#Main Fanction
if __name__ == '__main__':
    #bot.send_message(445330281, "123")
    try:
        print("start")
        bot.polling(none_stop=True)
    except:
        print("Error")
        bot.polling(none_stop=True)