"""
Module for culture routes
"""
from typing import Any, Dict, List, Tuple

from flask import Flask, request
from flask_jwt_extended import jwt_required  # type: ignore

from pymongo import MongoClient  # type:ignore


def culture_routes(app: Flask, db: MongoClient) -> None:
    """
    Adds Culture routes to Flask App

    Parameters:

    app: Flask app

    db: MongoDB client
    """

    @app.route("/v1/culture")
    def cultures() -> Tuple[Dict[str, List[str]], int]:
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
        return {"cultures": cultures}, 200

    @app.route("/v1/culture/<name>")
    def culture_snapshot(name: str) -> Tuple[Dict[str, Any], int]:
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
            return {"msg": "Internal server error"}, 500

        del culture["specialized_insights"]
        culture["_id"] = str(culture["_id"])
        return culture, 200

    @app.route("/v1/culture/<name>/all")
    def culture_detailed(name: str) -> Tuple[Dict[str, Any], int]:
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
            return {"msg": f"unknown culture `{name}`"}, 404

        culture["_id"] = str(culture["_id"])
        return culture, 200

    @app.route("/v1/culture/<name>/download")
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
                {"msg": f"failed to create culture {body['name']}: already exists"},
                409,
            )

        result = collection.insert_one(body)

        if not result.acknowledged:
            return {"msg": f"failed to create culture {body['name']}"}, 500

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
            return {"msg": "Internal server error"}, 500

        return body, 200

    @app.route("/v1/culture/<name>", methods=["DELETE"])
    @jwt_required
    def delete_culture(name: str) -> Tuple[Dict[str, str], int]:
        """
        Delete an existing Culture

        Returns:

          200 - culture deleted

          {"msg": "deleted CULTURE_GROUP"}

          401 - not authorized
          500 - otherwise
        """
        collection = db.cultures
        result = collection.delete_one({"name": name})
        if result.deleted_count == 0:
            return {"msg": "Internal server error"}, 500

        return {"msg": f"deleted {name}"}, 200