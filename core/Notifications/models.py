import mongoengine
from mongoengine import fields
from django.db import models
from django.utils import timezone
from django.conf import settings

from django.template import Context, Template
from django.template.loader import render_to_string
from premailer import transform

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin
from .tasks import send_email


class Notification(CrmMixin, SlugifyMixin):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    message = models.TextField()
    message_html = models.TextField()
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_slug(cls, slug):
        return cls.objects.get(slug=slug)

    def prepare_message(self, context):
        ctx = Context(context)
        return Template(self.message).render(ctx)

    def prepare_message_html(self, context):
        ctx = Context(context)
        base_template = 'Notification/base_email_template.html'
        _text = Template(self.message_html).render(ctx)
        _context = context.copy()
        _context.update({'text': _text})
        _template = render_to_string(base_template, _context)
        return transform(_template, base_url=settings.EMAIL_BASE_SITE)

    def prepare_subject(self, context):
        ctx = Context(context)
        return Template(self.subject).render(ctx)

    def create_message(self, recipient, context, slug):
        msg = NotificationMessage()
        msg.recipient = recipient
        msg.message = self.prepare_message(context)
        msg.message_html = self.prepare_message_html(context)
        msg.subject = self.prepare_subject(context)
        msg.context = context
        msg.notification_slug = slug
        msg.save()
        return msg

    def send(self, recipient, context):
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [recipient.notify_by_email]
        msg = self.create_message(recipient.notify_by_email, context, slug='email')

        send_email.apply_async(args=[msg.subject, msg.message, msg.message_html,
                                     from_email, to_email])
        return msg

    def send_fridge(self, recipient, context):
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [recipient.notify_by_email]
        msg = self.create_message(recipient.notify_by_email, context, slug='email')
        send_email.apply_async(args=[msg.subject, msg.message, msg.message_html,
                                     from_email, to_email])

        self.create_message(recipient.notify_by_email, context, slug='fridge')
        return msg


class NotificationMessage(mongoengine.DynamicDocument):
    stamp = fields.DateTimeField(default=timezone.now)

    recipient = fields.StringField()
    subject = fields.StringField(null=True)
    message = fields.StringField()
    message_html = fields.StringField(null=True)
    context = fields.DictField(null=True)
    notification_slug = fields.StringField(null=True)
    is_read = fields.BooleanField(default=False)

    meta = {
        'db_alias': 'notification',
        'allow_inheritance': False,
        'collection': 'notification_message',
    }
