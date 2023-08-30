from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import *
from django.conf import settings


def send_notifications(preview, pk, title, subs):
    html_content = render_to_string(
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

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Topics)
def notify_created_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        topics = instance.postTopics.all()
        subs: list[str] = []
        print(f'{subs = }')
        for t in topics:
            subs += t.subs.all()

        subs = [s.email for s in subs]
        print(f'{subs = }')

        send_notifications(instance.preview(), instance.pk, instance.title, subs)




# Есть такое вариант на основе проекта интернет-магазина. Но какой из них корректнее?
# По условиям итогового задания нужно использовать post_save, но в вебинарах разбирают другой вариант


    # @receiver(post_save, sender=Post)
    # def product_created(instance, created, **kwargs,):
    #     if not created:
    #         return
    #
    #     emails = User.objects.filter(
    #         user_subscriptions=instance.postTopic.subs
    #     ).values_list('email', flat=True)
    #
    #     html_content = render_to_string(
    #         'post_created_email.html',
    #         {'link': f'{settings.SITE_URL}/news/{instance.get_absolute_url()}'}
    #     )
    #     for email in emails:
    #         msg = EmailMultiAlternatives(None, [email])
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send()
