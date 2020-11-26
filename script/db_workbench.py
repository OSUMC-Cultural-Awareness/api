"""Developer db functions."""

import os
import sys

from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash

sys.path.insert(0, "/appdata")

from api import create_app
from api.db_connection import connect


# general functions
def list_collections():
    """All collections in the db."""
    return db.list_collection_names()


def print_all():
    """Print cultures and admins."""
    print_cultures()
    print_admins()


# culture functions
def print_cultures():
    """Print cultures."""
    for culture in db.cultures.find():
        print(culture["name"])
    print(db.cultures.count_documents({}))


def print_culture_general_insights(culture_name):
    """Print given culture's general insights.

    Arguments:
      culture_name: culture to print general insight for
    """
    culture = db.cultures.find_one({"name": culture_name})
    insights = culture["general_insights"]
    for insight in insights:
        print(insight["text"][0:50])


def create_culture(value):
    """Create a new culture.

    Arguments:
      value: value of Culture to insert directly into database.

    Note:
      Avoid this operation on a live database connected to users as errors
      he could negatively affect their experience, instead use the Api.
    """
    return db.cultures.insert_one(value)


def delete_culture(culture_id):
    """Delete a culture.

    Arguments:
      culture_id: ID of culture to delete

    Note:
      Avoid this operation on a live database connected to users as errors
      he could negatively affect their experience, instead use the Api.
    """
    return db.cultures.delete_one({"_id": culture_id})


def delete_all_cultures():
    """Delete all cultures.

    Note:
      Avoid this operation on a live database connected to users as errors
      he could negatively affect their experience, instead use the Api.
    """
    return db.cultures.delete_many({})


def update_culture(value):
    """Update the given culture.

    Note:
      Avoid this operation on a live database connected to users as errors
      he could negatively affect their experience, instead use the Api.

      This operation could also create a new culture if one with the provided "_id" doesn't exist.
    """
    return db.cultures.replace_one({"_id": value["_id"]}, value)


def print_admins():
    """Print all admins."""
    for admin in db.admins.find():
        print(admin["name"])
    print(db.admins.count_documents({}))


def create_su_admin(name, email, password):
    """Create a new super user admin.

    Arguments:
      name: name of Admin
      email: email for Admin
      password: password for Admin
    """
    return db.admins.insert_one(
        {
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "superUser": True,
        }
    )


def create_admin(name, email, password):
    """Create a non-super-user admin.

    Arguments:
      name: name of Admin
      email: email for Admin
      password: password for Admin
    """
    return db.admins.insert_one(
        {
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "superUser": False,
        }
    )


def get_admin(name):
    """Fetch admin with the given name.

    Arguments:
      name: name of admin to fetch
    """
    return db.admins.find_one({"name": name})


def delete_admin(admin):
    """Delete the given admin.

    Arguments:
      admin_id: _id of admin to delete
    """
    return db.admins.delete_one(admin)


def delete_all_admins():
    """Delete all admins.

    Note:
      This will delete your Admin account as well and therefore would require using
      the `create_admin` in order to recreate an account.
    """
    return db.admins.delete_many({})


def update_admin(admin):
    """Update the given admin."""
    return db.admins.replace_one({"_id": admin["_id"]}, admin)


def create_token(email):
    """Generate an access token.

    Arguments:
      email: email to use for the JSON Web Token
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
        SECRET_KEY=os.getenv("SECRET_KEY"), JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )
    jwt = JWTManager(app)
