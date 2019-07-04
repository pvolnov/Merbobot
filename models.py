
from peewee import *

db = SqliteDatabase('../db.sqlite3')

class Users(Model):
    tel_id=IntegerField()
    name = TextField()
    efka_id = IntegerField()
    balance = IntegerField()
    mes_stat = IntegerField()
    qid = IntegerField(default=-1)

    class Meta:
        database = db
        db_table='Users'

class Lotery(Model):
    ef_id=IntegerField()
    name = TextField()
    secondname = TextField()
    email = TextField()
    phone = TextField()

    class Meta:
        database = db
        db_table='Lotery'

class Quiz(Model):
    text = TextField()
    answers = TextField()
    results=TextField(default='0;0;0;0')


    class Meta:
        database = db
        db_table='Quiz'

class Shops(Model):
    latitude = FloatField()
    longitude = FloatField()
    name = TextField()


    class Meta:
        database = db
        db_table='Shops'

class Info(Model):
    shopname = TextField()
    datatime = DateTimeField()
    user_id=IntegerField()
    status=FloatField()
    photo_name=TextField()

    class Meta:
        database = db
        db_table='Information'

class Dset(Model):
    name = TextField()
    stutus  = FloatField()
    shop = TextField(null=True)

    class Meta:
        database = db
        db_table='Dset'

#Dset.create_table()
# # db.connect()
# db.create_tables([Quiz,Users,Shops,Info,Lotery], safe = True)
# # db.close()

#Quiz.create_table()
# uncle_bob = Subs(name='Bob', tel_id=121212)
# uncle_bob.save()