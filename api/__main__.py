import os

from flask import Flask

from flask_bcrypt import Bcrypt  # type: ignore

from . import create_app, db_connection
from .auth import auth.auth


MAIL_USERNAME = os.getenv("GMAIL_ADDRESS")
MAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

app = Flask(__name__)
app.config.update(
    # EMAIL SETTINGS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
)

db = db_connection.connect()
bcrypt = Bcrypt(app)

auth(app, db, bcrypt)  # type: ignore
create_app(app, db)
