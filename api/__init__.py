"""
Flask API for interacting with OSUMC-Cultural Awareness App

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
from typing import Any, Dict, List, Tuple, Optional

from flask import Flask

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


def create_app(db: MongoClient) -> Flask:
    """
    Construct Flask App with all Endpoints

    Returns:

      Flask app
    """
    app = Flask(__name__)
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
        """
        Health route
        """
        return {"message": "healthy"}

    return app
