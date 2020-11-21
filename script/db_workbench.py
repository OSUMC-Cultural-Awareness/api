"""
Developer db functions
"""

import os
import sys
from flask_jwt_extended import create_access_token, JWTManager
from flask_bcrypt import Bcrypt

sys.path.insert(0, "/appdata")

from api import create_app
from api.db_connection import connect


# general functions
def list_collections():
    """
    all collections in the db
    """
    return db.list_collection_names()


def print_all():
    """
    print cultures and admins
    """
    print_cultures()
    print_admins()


# culture functions
def print_cultures():
    """
    print cultures
    """
    for culture in db.cultures.find():
        print(culture["name"])
    print(db.cultures.count_documents({}))


def print_culture_general_insights(culture_name):
    """
    print given culture's general insights
    """
    culture = db.cultures.find_one({"name": culture_name})
    insights = culture["general_insights"]
    for insight in insights:
        print(insight["text"][0:50])


def create_culture(value):
    """
    create a new culture
    """
    return db.cultures.insert_one(value)


def delete_culture(culture_id):
    """
    delete a culture
    """
    return db.cultures.delete_one({"_id": culture_id})


def delete_all_cultures():
    """
    delete all cultures
    """
    return db.cultures.delete_many({})


def update_culture(value):
    """
    update the given culture
    """
    return db.cultures.replace_one({"_id": value["_id"]}, value)


# admin functions


def print_admins():
    """
    print all admins
    """
    for admin in db.admins.find():
        print(admin["name"])
    print(db.admins.count_documents({}))


def create_su_admin(name, email, password):
    """
    create a new super user admin
    """
    return db.admins.insert_one(
        {
            "name": name,
            "email": email,
            "password": bcrypt.generate_password_hash(password),
            "superUser": True,
        }
    )


def create_admin(name, email, password):
    """
    create a non-super-user admin
    """
    return db.admins.insert_one(
        {
            "name": name,
            "email": email,
            "password": bcrypt.generate_password_hash(password),
            "superUser": False,
        }
    )


def get_admin(name):
    """
    fetch admin with the given name
    """
    return db.admins.find_one({"name": name})


def delete_admin(admin_id):
    """
    delete the given admin
    """
    return db.admins.delete_one({"_id": admin_id})


def delete_all_admins():
    """
    delete all admins
    """
    return db.admins.delete_many({})


def update_admin(value):
    """
    update the given admin
    """
    return db.admins.replace_one({"_id": value["_id"]}, value)


# auth functions


def create_token(email):
    """
    generate an access toekn
    """
    ret = ""
    with app.app_context():
        ret = create_access_token(identity=email)

    return ret


if __name__ == "__main__":
    # instantiate db and app
    db = connect()
    app = create_app()
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
