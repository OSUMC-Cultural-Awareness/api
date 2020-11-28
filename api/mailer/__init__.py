"""Contains functions that send emails."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message  # type: ignore
from jinja2 import Template

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")


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
        url=f"{FRONTEND_URL}/Register?token={token}",
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
        url=f"{FRONTEND_URL}/Recovery?token={token}&email={email}",
        title="OSUMC Cultural Awareness App Admin Recovery Email",
        link_caption="Click the following link to recover your account",
        header="Recover your Account",
        action="Recover Account",
    )

    mail.send(msg)


def send_feedback(app: Flask, feedback: str) -> None:
    """Send feedback to $MAIL_USERNAME if not provided logs the feedback.

    Arguments:
      app: the flask app
      feedback: feedback from user
    """
    mail = Mail(app)
    try:
        msg = Message(
            "Feedback",
            sender="User",
            recipients=[app.config["MAIL_USERNAME"]],
            body=feedback,
        )
        mail.send(msg)
    except KeyError:
        print("$MAIL_USERNAME not configured")
        print(f'Feedback: "{feedback}"')

