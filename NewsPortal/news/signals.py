from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import *
from ..NewsPortal import settings


def send_notifications(preview, pk, title, subs):
    html_context = render_to_string(
        'post_created_email.html',
        {'text': preview,
         'link': f'{settings.SITE_URL}/news/{pk}',
         }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subs,

    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Post)
def notify_created_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_save':
        subscriptions = instance.postTopics.all()
        subs: list[str] = []
        for t in subscriptions:
            subs += t.subs.all()

        subs = [s.email for s in subs]

        send_notifications(instance.preview(), instance.pk, instance.title, subs)


