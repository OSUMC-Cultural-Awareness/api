import os
import sys

sys.path.insert(0, "/appdata")
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from api.db_connection import connect

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


def create_admin(value):
    return db.admins.insert_one(value)


def delete_admin(admin_id):
    return db.admins.delete_one({"_id": admin_id})


def delete_all_admins():
    return db.admins.delete_many({})


def update_admin(value):
    return db.admins.replace_one({"_id": value["_id"]}, value)


# instantiate db
db = connect()
