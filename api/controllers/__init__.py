"""
Flask API for interacting with OSUMC-Cultural Awareness App

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
from typing import Any, List, Dict
from flask import request, Flask
from ../ import db_connection
db = db_connection.connect()


def create_app() -> Flask:
    """
    Construct Flask App with all Endpoints

    Returns:

      Flask app
    """
    app = Flask(__name__)

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
        Fetch a list of all culture groups

        Returns:

          200 - list of the all the names of culture groups
          {
            "cultures": [culture1, culture2, ...]
          }

          500 - otherwise
        """
        return {"cultures": []}

    @app.route("/v1/<group_name>")
    def culture_snapshot(group_name: str) -> Any:
        """
        Fetch a snapshot of information about a specific Culture Group

        Parameters:

          group_name: name of Culture Group

        Returns:
          200 - all general insights for a group
          500 - otherwise
        """
        pass

    @app.route("/v1/<group_name>/all")
    def culture_detailed(group_name: str) -> Any:
        """
        Fetch all information about a specific Culture Group

        Parameters:

          group_name: name of Culture Group

        Returns:
          200 - all insights for a group
          500 - otherwise
        """
        pass

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

            {"oauth": "token"}

            400 - malformed request body
            401 - wrong password
            500 - otherwise
        """
        body = request.get_json()
        return {"oauth": body["password"]}

    @app.route("/v1/culture_groups", methods=["POST"])
    def create_culture() -> Dict[str, str]:
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

          {"message": "successfully created CULTURE_NAME"}

          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()
        return {"message": f"succesfully created {body['name']}"}

    @app.route("/v1/<culture_group>", methods=["PUT"])
    def update_culture(culture_group: str) -> Dict[str, str]:
        """
        Update an existing Culture

        Parameters:

          POST Body:

          {
            "name": "culture-name",
            "general_insights": [],
            "specialized_insights": [],
            "oauth": "token"
           }

        Returns:
          200 - group successfully updated

          {"message": "successfully updated CULTURE_GROUP"}

          401 - bad auth token
          500 - otherwise
        """
        body = request.get_json()
        return {"message": f"succesfully updated {culture_group}"}

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
        return {"message": f"deleted {culture_group}"}

    @app.route("/v1/register", methods=["POST"])
    def register() -> Dict[str, str]:
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

          {"message": "successfully created user NAME <EMAIL>"}

          400 - Malformed body
          401 - unauthorized
          500 - otherwise
        """
        body = request.get_json()
        return {
            "message":
            f"successfully created user {body['name']} <{body['email']}>"
        }

    @app.route("/v1/admins")
    def admins() -> List[Any]:
        """
        List all admins

        Returns:

          200 - list of admins returned

          {"admins": ["admin1", "admin2", ...]}

          401 - bad auth token
          500 - otherwise
        """
        return {"admins": []}

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
        return {"message": f"email sent to {body['email']}"}

    @app.route("/v1/admin/<email>", methods=["PUT"])
    def update_admin(email: str) -> Dict[str, str]:
        """
        Update Admin

        Parameters:

          email: email of Admin

          POST Body:

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
        return {"message": f"successfully updated admin <{email}>"}

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
        return {"message": "successfully deleted admin <{email}>"}

    return app
