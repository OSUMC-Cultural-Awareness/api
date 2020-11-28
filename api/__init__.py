"""Flask API for interacting with OSUMC-Cultural Awareness App.

Routes Specified:
  https://docs.google.com/spreadsheets/d/19zLqvcoFI7Jm_y6nPPgcRmaBuPEkDKtgeiyozekbMoU/edit?usp=sharing
"""
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, request
from pymongo import MongoClient  # type:ignore

from .mailer import send_feedback
from .request_schemas import FeedbackSchema, validate_request_body


def create_app() -> Flask:
    """Construct Flask App with all Endpoints.

    Returns:
      Flask app
    """
    app = Flask(__name__)

    @app.route("/health")
    def health() -> Tuple[Dict[str, str], int]:
        """Health route."""
        return {"msg": "healthy"}, 200

    @app.route("/api/v1/feedback", methods=["POST"])
    def feedback() -> Tuple[Dict[str, str], int]:
        """Send feedback to $GMAIL_USERNAME.

        Arguments:
          POST Body:

          {
            "feedback": "...",
          }

        Returns:
          200 - feedback sent

          {"msg": "feedback sent"}

          400 - malformed request
          500 - otherwise

        """
        body = validate_request_body(FeedbackSchema, request.json)
        if isinstance(body, str):
            return {"msg": body}, 400

        feedback = body["feedback"]

        send_feedback(app, feedback)

        return {"msg": "feedback sent"}, 200

    return app
