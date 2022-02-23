from django.template import loader
from django.core.mail import send_mail
from scrapper.settings import (
    DEFAULT_FROM_EMAIL,
    DOMAIN_URL
)


def send_report_status(Email):
    try:
        email_subject = "Report Status"
        t = loader.get_template("email_templates/report_status.html")
        c = {"Message": "Report Done"}
        email_body = t.render(c)

        from_email = DEFAULT_FROM_EMAIL
        to_email = Email.email

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
