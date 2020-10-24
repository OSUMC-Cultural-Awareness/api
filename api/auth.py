from typing import Any, Dict, List, Tuple, Optional

from flask import Flask, request

from flask_bcrypt import Bcrypt  # type: ignore
from flask_jwt_extended import (  # type: ignore
    JWTManager,
    jwt_required,
    create_access_token,
)

from pymongo import MongoClient  # type: ignore


def auth(app: Flask, db: MongoClient, bcrypt: Bcrypt) -> None:
    """
    Setup JWT Authentication via flask_jwt_extended and Login and Register route

    Docs: https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage/

    Parameters:
        app: Flask app

        db: MongoDB client

        bcrypt: Bcrypt handle

    Returns:

        JWTManager instance
    """
    jwt = JWTManager(app)

    @app.route("/v1/login", methods=["POST"])
    def login() -> Tuple[Dict[str, str], int]:
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
        if not request.is_json:
            return {"message": "Request body must be JSON"}, 400

        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return {"message": "Request body must have 'email'"}, 400

        if not password:
            return {"message": "Request body must have 'password'"}, 400

        collection = db.admins
        admin = collection.find_one({"email": email})

        if not admin:
            return {"message": "Invalid username or password"}, 401

        if not bcrypt.check_password_hash(admin["password"], password):
            return {"message": "Invalid username or password"}, 401

        return {"token": create_access_token(identity=email)}, 200

    @app.route("/v1/register", methods=["POST"])
    @jwt_required
    def register() -> Tuple[Dict[str, str], int]:
        """
        Register a new administrator

        JWT is passed via

        Parameters:

          POST Body:

          {
            "name": "name",
            "email": "email",
            "password": "password",
            "password_confirmation": "password",
           }

        Returns:
          200 - New admin created

          {"message": "successfully created admin NAME <EMAIL>"}

          400 - Malformed body
          401 - unauthorized
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
        if collection.find_one({"email": body["email"]}) is not None:
            return (
                {
                    "message": f"failed to create admin with email <{body['email']}>: duplicate"
                },
                409,
            )

        body["password"] = bcrypt.generate_password_hash(body["password"])

        result = collection.insert_one(body)
        if not result.acknowledged:
            return {"message": "internal error"}, 500

        return {"token": create_access_token(identity=body["email"])}, 201
