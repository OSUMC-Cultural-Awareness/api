"""Module for admin routes."""
from datetime import timedelta
from typing import Dict, List, Tuple, Union

from flask import Flask, request
from flask_jwt_extended import create_access_token  # type: ignore
from flask_jwt_extended import jwt_required
from pymongo import MongoClient  # type:ignore

from ..mailer import send_invite_email, send_recovery_email
from ..request_schemas import (AdminEmailSchema, AdminUpdateSchema,
                               validate_request_body)


def admin_routes(app: Flask, db: MongoClient) -> None:
    """Adds Admin routes to Flask App.

    Arguments:
    app: Flask app

    db: MongoDB client
    """

    @app.route("/api/v1/admins")
    @jwt_required
    def admins() -> Dict[str, List[Dict[str, Union[str, bool]]]]:
        """List all admins.

        Returns:
          200 - list of admin's emails

          {"admins": ["admin1@test.com", "admin2@test.com", ...]}

          401 - bad auth token
          500 - otherwise
        """
        collection = db.admins
        admins = [
            {
                "email": admin["email"],
                "name": admin["name"],
                "superUser": admin["superUser"],
            }
            for admin in collection.find().sort("email")
        ]
        return {"admins": admins}

    @app.route("/api/v1/admins/<email>")
    @jwt_required
    def admin(email: str) -> Tuple[Dict[str, str], int]:
        """Fetch information about an admin.

        Arguments:
          email: email of admin to get information on

        Returns:
          200 - admin information

          {"email": "test@gmail.com", "superUser": false, "name": "test"}

          401 - bad auth

          404 - can't find admin
        """
        admin = db.admins.find_one({"email": email})
        if admin is None:
            return {"msg": f"unknown admin `{email}`"}, 404

        del admin["password"]
        del admin["_id"]
        return admin, 200

    @app.route("/api/v1/admins/invite", methods=["POST"])
    @jwt_required
    def invite() -> Tuple[Dict[str, str], int]:
        """Invite admin via Email.

        Arguments:
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
        body = validate_request_body(AdminEmailSchema, request.json)
        if isinstance(body, str):
            return {"msg": body}, 400

        email = body["email"]
        if db.admins.find_one({"email": email}) is not None:
            return (
                {"msg": f"<{email}>: duplicate"},
                409,
            )

        token = create_access_token(identity=email, expires_delta=timedelta(days=1))

        send_invite_email(app, token, email)

        return {"msg": f"email sent to {email}"}, 200

    @app.route("/api/v1/admins/<email>", methods=["PUT"])
    @jwt_required
    def admin_update(email: str) -> Tuple[Dict[str, str], int]:
        """Update Admin.

        Arguments:
          email: email of Admin

          PUT Body:

          {
            "name": "name",
          }

        Returns:
          200 - admin successfully updated

          {"msg": "successfully updated admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        body = validate_request_body(AdminUpdateSchema, request.json)
        if isinstance(body, str):
            return {"msg": body}, 400

        admin = db.admins.find_one({"email": email})

        if "name" not in body:
            return {"msg": f"no changes to admin <{email}>"}, 200

        admin["name"] = body["name"]
        result = db.admins.replace_one({"email": email}, admin)
        if result.matched_count == 0 or result.modified_count == 0:
            return {"msg": "Internal server error"}, 500

        return {"msg": f"successfully updated admin <{email}>"}, 200

    @app.route("/api/v1/admins/<email>", methods=["DELETE"])
    @jwt_required
    def admin_delete(email: str) -> Tuple[Dict[str, str], int]:
        """Delete Admin.

        Arguments:
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

    @app.route("/api/v1/admins/recover", methods=["POST"])
    def admin_recover() -> Tuple[Dict[str, str], int]:
        """Recover admin password.

        Arguments:
            POST Body:
              {
                "email": "test@gmail.com"
              }

        Returns:
          200 - admin email recover email sent

          {"msg": "email sent to <EMAIL>"}

          400 - bad request
          404 - admin not found
          500 - otherwise
        """
        body = validate_request_body(AdminEmailSchema, request.json)
        if isinstance(body, str):
            return {"msg": body}, 400

        email = body["email"]

        collection = db.admins
        result = collection.find_one({"email": email})
        if result is None:
            return {"msg": f"unknown admin {email}"}, 404

        token = create_access_token(identity=email, expires_delta=timedelta(days=1))

        send_recovery_email(app, token, email)

        return {"msg": f"email sent to {email}"}, 200
