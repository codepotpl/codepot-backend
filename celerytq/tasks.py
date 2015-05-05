from celery import shared_task
from django.core.mail import send_mail as d_send_mail

from codepot.logging import logger


@shared_task
def send_mail(to, title, message):
    logger.info('Sending email to: {}, title: {}, message: {}'.format(to, title, message))
    return d_send_mail(title, message, 'donotreply@codepot.pl', [to])


@shared_task
def add(x, y):
    return x + y