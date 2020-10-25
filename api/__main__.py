import os

from flask import Flask

from flask_bcrypt import Bcrypt  # type: ignore

from . import create_app, db_connection
from .auth import auth_routes
from .resource.admin import admin_routes
from .resource.culture import culture_routes


MAIL_USERNAME = os.getenv("GMAIL_ADDRESS")
MAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

db = db_connection.connect()
app = create_app(db)

app.config.update(
    # EMAIL SETTINGS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
)

bcrypt = Bcrypt(app)

# Routes
auth_routes(app, db, bcrypt)
admin_routes(app, db)
culture_routes(app, db)
