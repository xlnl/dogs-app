from peewee import *
from flask_login import UserMixin

import datetime

DATABASE = PostgresqlDatabase('dogs_app', host='localhost', port=5432)

class BaseModel(Model):
    class Meta: 
        database = DATABASE

class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

class Dog(BaseModel):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

class UserDog(BaseModel):
    user = ForeignKeyField(User, backref='pets')
    dog = ForeignKeyField(Dog, backref='human')

# method definiation
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User, UserDog], safe=True) 
    print("Tables created")
    DATABASE.close()