"""Contains functions that send emails."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message  # type: ignore
from jinja2 import Template

load_dotenv()

FRONTEND_IP = os.getenv("FRONTEND_IP")


def send_invite_email(app: Flask, token: str, email: str) -> None:
    """Prepare the admin invite email and send it.

    Arguments:
      app: the flask app
      token: token created for the email
      email: address the email is being sent to
    """
    mail = Mail(app)
    with open("api/mailer/templates/invite.html", "r") as f:
        template = Template(f.read())

    msg = Message("Account Activation", sender="App Admin", recipients=[f"{email}"],)

    msg.html = template.render(url=f"http://{FRONTEND_IP}/Register?token={token}")

    mail.send(msg)
