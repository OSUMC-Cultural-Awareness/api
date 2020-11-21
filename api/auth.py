"""
Module for Authentication and Authorization Routes
"""
from datetime import timedelta
from json import dumps
from typing import Dict, Tuple

from flask import Flask, request
from flask_bcrypt import Bcrypt  # type: ignore
from flask_jwt_extended import JWTManager  # type: ignore
from flask_jwt_extended import create_access_token, jwt_required
from pymongo import MongoClient  # type: ignore

from .request_schemas import (AdminLoginSchema, AdminRegisterSchema,
                              validate_request_body)


def auth_routes(app: Flask, db: MongoClient, bcrypt: Bcrypt) -> None:
    """
    Setup JWT Authentication via flask_jwt_extended and Login and Register route

    Docs: https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage/

    Parameters:
        app: Flask app

        db: MongoDB client

        bcrypt: Bcrypt handle
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

            {"token": JWT}

            400 - malformed request body
            401 - wrong password
            500 - otherwise
        """
        body = validate_request_body(AdminLoginSchema, request.json)
        if isinstance(body, str):
            return {"msg": "Login unsuccessful"}, 400

        email = body["email"]
        password = body["password"]

        admin = db.admins.find_one({"email": email})

        if not admin:
            return {"msg": "Invalid username or password"}, 401

        if not bcrypt.check_password_hash(admin["password"], password):
            return {"msg": "Invalid username or password"}, 401

        return (
            {
                "token": create_access_token(
                    identity=email, expires_delta=timedelta(days=1)
                )
            },
            200,
        )

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

          {"token": JWT}

          400 - Malformed body
          401 - unauthorized
          500 - otherwise
        """
        body = validate_request_body(AdminRegisterSchema, request.get_json())
        if isinstance(body, str):
            return {"msg": body}, 400

        if body["password"] != body["password_confirmation"]:
            return (
                {"msg": "`password` and `password_confirmation` don't match"},
                401,
            )
        del body["password_confirmation"]

        if db.admins.find_one({"email": body["email"]}) is not None:
            return (
                {
                    "msg": f"failed to create admin with email <{body['email']}>: duplicate"
                },
                409,
            )

        body["password"] = bcrypt.generate_password_hash(body["password"])
        body["superUser"] = False

        result = db.admins.insert_one(body)
        if not result.acknowledged:
            return {"msg": "internal error"}, 500

        del body["password"]
        body["_id"] = str(body["_id"])

        return (
            {
                "user": dumps(body),
                "token": create_access_token(
                    identity=body["email"], expires_delta=timedelta(days=1)
                ),
            },
            201,
        )
