"""
Module for admin routes
"""
from typing import Dict, List, Tuple

from flask import Flask, request
from flask_bcrypt import Bcrypt  # type: ignore
from flask_mail import Mail, Message  # type: ignore
from flask_jwt_extended import jwt_required  # type: ignore

from pymongo import MongoClient  # type:ignore


def admin_routes(app: Flask, db: MongoClient, bcrypt: Bcrypt) -> None:
    """
    Adds Admin routes to Flask App

    Parameters:

    app: Flask app

    db: MongoDB client
    """

    mail = Mail(app)

    @app.route("/v1/admin")
    @jwt_required
    def admins() -> Dict[str, List[str]]:
        """
        List all admins

        Returns:

          200 - list of admins returned

          {"admins": ["admin1", "admin2", ...]}

          401 - bad auth token
          500 - otherwise
        """
        collection = db.admins
        admins = [admin["name"] for admin in collection.find().sort("name")]
        return {"admins": admins}

    @app.route("/v1/admin/invite", methods=["POST"])
    @jwt_required
    def invite_admin() -> Dict[str, str]:
        """
        Invite admin via Email

        Parameters:

          POST Body:

          {
            "email": "email",
          }

          Returns:
            200 - admin successfully added

            {"msg": "email sent to EMAIL"}

            401 - bad auth token
            500 - otherwise
        """

        body = request.get_json()
        msg = Message(
            "Account Activation",
            sender="osumc.cultural.awareness@gmail.com",
            recipients=[f"{body['email']}"],
        )
        msg.html = """\
          <!DOCTYPE html>
          <html>
            <body>
              <h1 style="color:SlateGray;">This is an HTML Email!</h1>
            </body>
          </html>
          """
        mail.send(msg)
        return {"msg": f"email sent to {body['email']}"}

    @app.route("/v1/admin/<email>", methods=["PUT"])
    @jwt_required
    def update_admin(email: str) -> Tuple[Dict[str, str], int]:
        """
        Update Admin

        Parameters:

          email: email of Admin

          PUT Body:

          {
            "name": "name",
            "email": "email",
            "password": "password",
            "password_confirmation": "password",
          }

        Returns:
          200 - admin successfully updated

          {"msg": "successfully updated admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        if body["password"] != body["password_confirmation"]:
            return (
                {"msg": "`password` and `password_confirmation` don't match"},
                401,
            )

        del body["password_confirmation"]

        body["password"] = bcrypt.generate_password_hash(body["password"])

        collection = db.admins
        result = collection.replace_one({"email": email}, body)
        if result.matched_count == 0 or result.modified_count == 0:
            return {"msg": "Internal server error"}, 500

        return {"msg": f"successfully updated admin <{email}>"}, 200

    @app.route("/v1/admin/<email>", methods=["DELETE"])
    @jwt_required
    def delete_admin(email: str) -> Tuple[Dict[str, str], int]:
        """
        Delete Admin

        Parameters:
          email: email of Admin

        Returns:
          200 - admin successfully deleted

          {"msg": "successfully deleted admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        collection = db.admins
        result = collection.delete_one({"email": email})
        if result.deleted_count == 0:
            return {"msg": "Internal server error"}, 500
        return {"msg": f"successfully deleted admin <{email}>"}, 200
