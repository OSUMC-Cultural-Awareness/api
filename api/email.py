import smtplib, os
from email.message import EmailMessage

EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


def send_admin_invite_email(email_address):
    msg = EmailMessage()
    msg["Subject"] = "Activate your account"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = [email_address]
    msg.set_content("plain text")

    msg.add_alternative(
        """\
    <!DOCTYPE html>
    <html>
      <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
      </body>
    </html>	
    """,
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
