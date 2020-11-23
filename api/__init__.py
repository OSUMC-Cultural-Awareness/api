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

    @app.route("/health")
    def health():
        """Health route."""
        return {"msg": "healthy"}

    return app
