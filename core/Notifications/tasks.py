from __future__ import unicode_literals

from celery_run import app
from django.core.mail import EmailMultiAlternatives


@app.task(ignore_result=True)
def send_email(subject, message, message_html, from_email, to_email):
    email_msg = EmailMultiAlternatives(subject,
                                       message,
                                       from_email, to_email)

    email_msg.mixed_subtype = 'related'
    email_msg.attach_alternative(message_html, "text/html")
    email_msg.send()
