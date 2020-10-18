"""
Flask API for interacting with OSUMC-Cultural Awareness App

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
import os
from typing import Any, Dict, List, Tuple
from flask import Flask, abort, request
from flask_mail import Mail, Message # type: ignore

MAIL_USERNAME = os.getenv("GMAIL_ADDRESS")
MAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


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


def create_app(db) -> Flask:
    """
    Construct Flask App with all Endpoints

    Returns:

      Flask app
    """
    app = Flask(__name__)
    app.config.update(
        # EMAIL SETTINGS
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
    )
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

    @app.route("/v1/culture_groups")
    def culture_groups() -> Dict[str, List[str]]:
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

    @app.route("/v1/<group_name>")
    def culture_snapshot(group_name: str) -> Dict[str, Any]:
        """
        Fetch a snapshot of information about a specific Culture Group

        Parameters:

          group_name: name of Culture Group

        Returns:
          200 - all general insights for a group
          500 - otherwise
        """
        collection = db.cultures
        culture = collection.find_one({"name": group_name})
        if culture is None:
            abort(500)

        del culture["specialized_insights"]
        culture["_id"] = str(culture["_id"])
        return culture

    @app.route("/v1/<group_name>/all")
    def culture_detailed(group_name: str) -> Dict[str, Any]:
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
        culture = collection.find_one({"name": group_name})
        if culture is None:
            abort(404, message={"message": f"unknown culture `{group_name}`"})

        culture["_id"] = str(culture["_id"])
        return culture

    @app.route("/v1/<group_name>/all/download")
    def download_culture(group_name: str) -> Any:
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

    @app.route("/v1/login", methods=["POST"])
    def login() -> Dict[str, str]:
        """
        Login a User

        Parameters:

          POST body:

          {
            "email": "email",
            "password": "password"
          }

          Returns:
            200 - Oauth token

            {"Message": "Authenticated"}

            400 - malformed request body
            401 - wrong password
            500 - otherwise
        """
        body = request.get_json()
        if not body["email"] or not body["password"]:
            abort(400)

        admin = db.admins.find_one({"email": body["email"]})
        if admin is None:
            abort(401)

        # Authenticate user

        return {"message": "Authenticated"}

    @app.route("/v1/culture_groups", methods=["POST"])
    def create_culture() -> Tuple[Dict[str, str], int]:
        """
        Create a Culture with information

        Parameters:

          POST Body:

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
            "oauth": "token"
           }

        Returns:
          200 - group successfully added

          POST Body without "oauth" field

          400 - malformed POST body
          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        if not body["oauth"]:
            abort(400)

        token = body["oauth"]
        del body["oauth"]
        # TODO: Authorize token

        collection = db.cultures
        result = collection.insert_one(body)

        if not result.acknowledged:
            return {"message": f"failed to create culture {body['name']}"}, 500

        body["_id"] = str(body["_id"])
        return body, 200

    @app.route("/v1/<culture_group>", methods=["PUT"])
    def update_culture(culture_group: str) -> Dict[str, str]:
        """
        Update an existing Culture

        Parameters:

          PUT Body:

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
            "oauth": "token"
           }

        Returns:
          200 - group successfully updated

          {"message": "successfully updated CULTURE_GROUP"}

          400 - malformed POST body
          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()

        if not body["oauth"]:
            abort(400, message="required field `oauth` not provided")

        token = body["oauth"]
        del body["oauth"]
        # TODO: Authorize token

        collection = db.cultures
        result = collection.replace_one({"name": body["name"]}, body)
        if result.matched_count == 0 or result.modified_count == 0:
            abort(500)

        return body

    @app.route("/v1/<culture_group>", methods=["DELETE"])
    def delete_culture(culture_group: str) -> Dict[str, str]:
        """
        Delete an existing Culture

        Returns:

          200 - culture deleted

          {"message": "deleted CULTURE_GROUP"}

          401 - not authorized
          500 - otherwise
        """
        collection = db.cultures
        result = collection.delete_one({"name": culture_group})
        if result.deleted_count == 0:
            abort(500)

        return {"message": f"deleted {culture_group}"}

    @app.route("/v1/register", methods=["POST"])
    def register() -> Tuple[Dict[str, str], int]:
        """
        Register a new administrator

        Parameters:

          POST Body:

          {
            "name": "name",
            "email": "email",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "token"
           }

        Returns:
          200 - New admin created

          {"message": "successfully created admin NAME <EMAIL>"}

          400 - Malformed body
          401 - unauthorized
          500 - otherwise
        """
        body = request.get_json()

        if not body["oauth"]:
            return {"message": "missing field `oauth`"}, 400

        token = body["oauth"]
        del body["oauth"]

        if body["password"] != body["password_confirmation"]:
            return (
                {"message": "`password` and `password_confirmation` don't match"},
                401,
            )
        del body["password_confirmation"]

        # Encrypt password prior to storing

        collection = db.admins
        result = collection.insert_one(body)
        if not result.acknowledged:
            abort(500)

        return (
            {
                "message": f"successfully created admin {body['name']} <{body['email']}>"
            },
            200,
        )

    @app.route("/v1/admins")
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
    def invite_admin() -> Dict[str, str]:
        """
        Invite admin via Email

        Parameters:

          POST Body:

          {
            "email": "email",
            "oauth": "token"
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
            "oauth": "token"
          }

        Returns:
          200 - admin successfully updated

          {"message": "successfully updated admin <EMAIL>"}

          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()
        if not body["oauth"]:
            return {"message": "missing field `oauth`"}, 400

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

    return app
