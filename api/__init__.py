"""Flask API for interacting with OSUMC-Cultural Awareness App.

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask
from pymongo import MongoClient  # type:ignore


def create_app() -> Flask:
    """Construct Flask App with all Endpoints.

    Returns:
      Flask app
    """
    app = Flask(__name__)

    @app.route("/")
    def index() -> Dict[str, List[Dict[str, Any]]]:
        """Index that informs user about routes.

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
        """Health route."""
        return {"msg": "healthy"}

    return app
