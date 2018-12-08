
from peewee import *

db = SqliteDatabase('../db.sqlite3')

class Users(Model):
    tel_id=IntegerField()
    name = TextField()
    efka_id = IntegerField()
    balance = IntegerField()
    mes_stat = IntegerField()
    qid = IntegerField()

    class Meta:
        database = db
        db_table='Users'

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

# db.connect()
# db.create_tables([Quiz,Users,Shops,Info], safe = True)
# db.close()

#Quiz.create_table()
# uncle_bob = Subs(name='Bob', tel_id=121212)
# uncle_bob.save()