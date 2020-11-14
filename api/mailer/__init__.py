"""
  This module is used for sending emails
"""

import os
from flask_mail import Mail, Message  # type: ignore
from jinja2 import Template

FRONTEND_IP = os.getenv("FRONTEND_IP")


def send_invite_email(app: any, token: str, email: str) -> None:
    """
    Prepare the admin invite email and send it

    Parameters:

      app: the flask app
      token: token created for the email
      email: address the email is being sent to

      Returns:
        None
    """

    mail = Mail(app)
    with open("api/mailer/templates/invite_template.txt", "r") as f:
        template = Template(f.read())

    msg = Message(
        "Account Activation",
        sender="App Admin",
        recipients=[f"{email}"],
    )

    msg.html = template.render(url=f"http://{FRONTEND_IP}/Register?token={token}")

    mail.send(msg)
