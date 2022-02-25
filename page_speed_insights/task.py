"""
    Import needed things
"""

from django.template import loader
from django.core.mail import send_mail
from scrapper.settings import (
    DEFAULT_FROM_EMAIL
)


def send_report_status(email):
    """
        Email sent after report done
    """
    try:
        email_subject = "Report Status"
        templates = loader.get_template("email_templates/report_status.html")
        message = {"Message": "Report Done"}
        email_body = templates.render(message)

        from_email = DEFAULT_FROM_EMAIL
        to_email = email.email

        send_mail(
            email_subject,
            email_body,
            from_email,
            [to_email],
            html_message=email_body,
        )
    except Exception as exc:
        print(str(exc))
    return
