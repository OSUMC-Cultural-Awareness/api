"""Contains functions that send emails."""

import os

from flask import Flask
from flask_mail import Mail, Message  # type: ignore
from jinja2 import Template

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

    msg.html = template.render(
        url=f"http://{FRONTEND_IP}/Register?token={token}",
        title="OSUMC Cultural Awareness App Admin Invitation Email",
        link_caption="Click the following link to register for an admin account",
        header="Join our Admin team",
        action="Register",
    )

    mail.send(msg)


def send_recovery_email(app: Flask, token: str, email: str) -> None:
    """Prepare the admin recovery email and send it.

    Arguments:
      app: the flask app
      token: token created for the email
      email: address the email is being sent to
    """
    mail = Mail(app)
    with open("api/mailer/templates/invite.html", "r") as f:
        template = Template(f.read())

    msg = Message("Account Recovery", sender="App Admin", recipients=[email])

    msg.html = template.render(
        url=f"http://{FRONTEND_IP}/Recovery?token={token}&email={email}",
        title="OSUMC Cultural Awareness App Admin Recovery Email",
        link_caption="Click the following link to recover your account",
        header="Recover your Account",
        action="Recover Account",
    )

    mail.send(msg)
