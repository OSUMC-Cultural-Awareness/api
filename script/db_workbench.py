import os
import sys

sys.path.insert(0, "/appdata")

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from flask_jwt_extended import create_access_token, JWTManager
from flask_bcrypt import Bcrypt

from api.db_connection import connect
from api import create_app


# general functions
def list_collections():
    return db.list_collection_names()


def print_all():
    print_cultures()
    print_admins()


# culture functions
def print_cultures():
    for culture in db.cultures.find():
        print(culture["name"])
    print(db.cultures.count_documents({}))


def print_culture_general_insights(culture_name):
    culture = db.cultures.find_one({"name": culture_name})
    insights = culture["general_insights"]
    for insight in insights:
        print(insight["text"][0:50])


def create_culture(value):
    return db.cultures.insert_one(value)


def delete_culture(culture_id):
    return db.cultures.delete_one({"_id": culture_id})


def delete_all_cultures():
    return db.cultures.delete_many({})


def update_culture(value):
    return db.cultures.replace_one({"_id": value["_id"]}, value)


# admin functions
def print_admins():
    for admin in db.admins.find():
        print(admin["name"])
    print(db.admins.count_documents({}))


def create_admin(name, email, password):
    return db.admins.insert_one(
        {
            "name": name,
            "email": email,
            "password": bcrypt.generate_password_hash(password),
        }
    )


def get_admin(name):
    return db.admins.find_one({"name": name})


def delete_admin(admin_id):
    return db.admins.delete_one({"_id": admin_id})


def delete_all_admins():
    return db.admins.delete_many({})


def update_admin(value):
    return db.admins.replace_one({"_id": value["_id"]}, value)


# auth functions
def create_token(email):
    ret = ""
    with app.app_context():
        ret = create_access_token(identity="J.Simpson@example.com")

    return ret


if __name__ == "__main__":
    # instantiate db and app
    db = connect()
    app = create_app(db)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
