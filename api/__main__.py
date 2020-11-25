"""Main entry point for Flask app."""
import os

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt  # type: ignore
from flask_cors import CORS  # type: ignore

from . import create_app, db_connection
from .auth import auth_routes
from .resource.admin import admin_routes
from .resource.culture import culture_routes

load_dotenv()

db = db_connection.connect()
app = create_app()

app.config.update(
    # EMAIL SETTINGS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv("GMAIL_ADDRESS"),
    MAIL_PASSWORD=os.getenv("GMAIL_PASSWORD"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
)

CORS(app)
bcrypt = Bcrypt(app)
auth_routes(app, db, bcrypt)
admin_routes(app, db, bcrypt)
culture_routes(app, db)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
