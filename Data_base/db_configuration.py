from peewee import *

db = SqliteDatabase('data.db')
class Clients(Model):
    client_parent_name = CharField()
    client_Child_name = CharField()
    client_phone = CharField()
    client_national_id = CharField()
    client_Subscription_time = CharField()
    pay_prise_of_subscription = IntegerField()
    class Meta:
        database = db
class Users (Model):
    user_name = CharField()
    user_password = CharField()
    user_phone = CharField()
    user_national_id = CharField()
    time_of_add_user = CharField()
    class Meta:
        database = db
class historiq (Model):
    user_id = IntegerField()
    action = IntegerField()
    time = CharField()

    class Meta:
        database = db
class permishens(Model) :
    user_name = IntegerField()
    add_client = IntegerField()
    delete_client = IntegerField()
    historiq = IntegerField()
    setting = IntegerField()
    users = IntegerField()
    add_user = IntegerField()
    edit_or_delete_user = IntegerField()
    user_permishens = IntegerField()
    class Meta :
        database = db

db.connect()
db.create_tables([Clients , Users ,historiq, permishens])
print("done")