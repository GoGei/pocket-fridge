# Generated by Django 3.2.12 on 2023-09-24 17:53

from django.db import migrations

MESSAGE = """Greetings, {{first_name}} {{last_name}}!\n
Thank you for registering in our system.\n
Please confirm your registration by clicking the link below: {{ url }}"""

MESSAGE_HTML = """Greetings, {{first_name}} {{last_name}}!<br>
Thank you for registering in our system.<br>
Please confirm your registration by clicking the link below: <a href="{{ url }}">Link</a><br>
Or, if the link in not active, just paste it to your browser: {{ url }}"""


def add_registration_activate_email(apps, schema):
    slug = 'registration-activate-email'
    Notification = apps.get_model('Notifications', 'Notification')
    notification, created = Notification.objects.get_or_create(
        slug=slug,
        defaults={
            'name': 'Email for user to register in system',
            'description': 'Email for user to register in system',
            'message': MESSAGE,
            'message_html': MESSAGE_HTML,
            'subject': 'Confirm registration',
        }
    )
    if created:
        print(f'Notification {slug} created')
    else:
        print(f'Notification {slug} already exists')


class Migration(migrations.Migration):
    dependencies = [
        ('Notifications', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_registration_activate_email)
    ]
