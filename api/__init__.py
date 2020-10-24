"""
Flask API for interacting with OSUMC-Cultural Awareness App

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
from typing import Any, Dict, List, Tuple, Optional

from flask import Flask, abort, request
from flask_mail import Mail, Message  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity  # type: ignore

from pymongo import MongoClient  # type:ignore


def error_handlers(app: Flask) -> None:
    """
    Define common Flask error handlers
    """

    @app.errorhandler(400)
    def malformed_request(error):
        return {"message": "malformed request"}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {"message": "unauthorized"}, 401

    @app.errorhandler(500)
    def internal_server_error(error):
        return {"message": "internal server error"}, 500

    @app.errorhandler(404)
    def not_found(error):
        return {"message": "resource not found"}


def create_app(app: Flask, db: MongoClient) -> None:
    """
    Construct Flask App with all Endpoints

    Returns:

      Flask app
    """
    mail = Mail(app)

    error_handlers(app)

    @app.route("/")
    def index() -> Dict[str, List[Dict[str, Any]]]:
        """
        Index that informs user about routes

        Returns:

          200 - JSON containing all routes

          {
            "routes": [
              {
                "methods": [
                  "POST",
                  "OPTIONS"
                ],
                "url": "/v1/admin/invite"
              },
              ...
            ]
          }

          500 - otherwise
        """
        response: Dict[str, List[Dict[str, Any]]] = {"routes": []}
        for rule in app.url_map.iter_rules():
            route = {"url": f"{rule.rule}", "methods": list(rule.methods)}
            response["routes"].append(route)
        return response

    @app.route("/v1/health")
    def health():
        return {"message": "healthy"}

    @app.route("/v1/culture")
    def cultures() -> Dict[str, List[str]]:
        """
        Fetch a list of all culture groups in alphabetical order

        Returns:

          200 - list of the all the names of culture groups
          {
            "cultures": [culture1, culture2, ...]
          }

          500 - otherwise
        """
        collection = db.cultures
        cultures = [culture["name"] for culture in collection.find().sort("name")]
        return {"cultures": cultures}

    @app.route("/v1/culture/<name>")
    def culture_snapshot(name: str) -> Dict[str, Any]:
        """
        Fetch a snapshot of information about a specific Culture Group

        Parameters:

          group_name: name of Culture Group

        Returns:
          200 - all general insights for a group
          500 - otherwise
        """
        collection = db.cultures
        culture = collection.find_one({"name": name})
        if culture is None:
            abort(500)

        del culture["specialized_insights"]
        culture["_id"] = str(culture["_id"])
        return culture

    @app.route("/v1/culture/<name>/all")
    def culture_detailed(name: str) -> Dict[str, Any]:
        """
        Fetch all information about a specific Culture Group

        Parameters:

          group_name: name of Culture Group

        Returns:
          200 - all insights for a group
          404 - culture doesn't exist
          500 - otherwise
        """
        collection = db.cultures
        culture = collection.find_one({"name": name})
        if culture is None:
            abort(404, message={"message": f"unknown culture `{name}`"})

        culture["_id"] = str(culture["_id"])
        return culture

    @app.route("/v1/<name>/download")
    def download_culture(name: str) -> Any:
        """
        Fetch all information about a specific Culture Group in downloadable
        and storeable form

        Parameters:

          group_name: name of Culture Group

        Returns:

          200 - file sent to browser for download
          500 - otherwise
        """
        pass

    @app.route("/v1/culture", methods=["POST"])
    @jwt_required
    def create_culture() -> Tuple[Dict[str, str], int]:
        """
        Create a Culture with information

        Parameters:

          POST Body:

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
           }

        Returns:
          200 - group successfully added
          400 - malformed POST body
          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        collection = db.cultures
        if collection.find_one({"name": body["name"]}) is not None:
            return (
                {"message": f"failed to create culture {body['name']}: already exists"},
                409,
            )

        result = collection.insert_one(body)

        if not result.acknowledged:
            return {"message": f"failed to create culture {body['name']}"}, 500

        body["_id"] = str(body["_id"])
        return body, 201

    @app.route("/v1/culture/<name>", methods=["PUT"])
    @jwt_required
    def update_culture(name: str) -> Tuple[Dict[str, str], int]:
        """
        Update an existing Culture

        Parameters:

          PUT Body:

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
           }

        Returns:
          200 - group successfully updated

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
           }

          201 - group renamed

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
           }

          400 - malformed POST body
          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        collection = db.cultures
        result = collection.replace_one({"name": name}, body)

        if result.matched_count == 0:
            return body, 201
        if result.matched_count == 0 and result.modified_count == 0:
            abort(500)

        return body, 200

    @app.route("/v1/culture/<name>", methods=["DELETE"])
    @jwt_required
    def delete_culture(name: str) -> Dict[str, str]:
        """
        Delete an existing Culture

        Returns:

          200 - culture deleted

          {"message": "deleted CULTURE_GROUP"}

          401 - not authorized
          500 - otherwise
        """
        collection = db.cultures
        result = collection.delete_one({"name": name})
        if result.deleted_count == 0:
            abort(500)

        return {"message": f"deleted {name}"}

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
