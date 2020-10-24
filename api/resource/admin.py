from typing import Any, Dict, List, Tuple, Optional

from flask import Flask, abort, request
from flask_mail import Mail, Message  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity  # type: ignore

from pymongo import MongoClient  # type:ignore


def admin_routes(app: Flask, db: MongoClient) -> None:
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

            {"message": "email sent to EMAIL"}

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
        return {"message": f"email sent to {body['email']}"}

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

          {"message": "successfully updated admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        if body["password"] != body["password_confirmation"]:
            return (
                {"message": "`password` and `password_confirmation` don't match"},
                401,
            )

        del body["password_confirmation"]

        collection = db.admins
        result = collection.replace_one({"email": email}, body)
        if result.matched_count == 0 or result.modified_count == 0:
            abort(500)

        return {"message": f"successfully updated admin <{email}>"}, 200

    @app.route("/v1/admin/<email>", methods=["DELETE"])
    @jwt_required
    def delete_admin(email: str) -> Dict[str, str]:
        """
        Delete Admin

        Parameters:
          email: email of Admin

        Returns:
          200 - admin successfully deleted

          {"message": "successfully deleted admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        collection = db.admins
        result = collection.delete_one({"email": email})
        if result.deleted_count == 0:
            abort(500)
        return {"message": f"successfully deleted admin <{email}>"}
