from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_to_email(emails: list, first_name: str):
    send_mail('Royhatdan otish', F'Tabriklimiz {first_name} royhatdan otdiz', EMAIL_HOST_USER, emails)
    return {'success': True}


@shared_task
def custom_task():
    # time.sleep(30)
    return {'msg': 'task bajarildi'}


@shared_task
def send_new_product_notification(users_emails, product_name: str, url: str):
    # from apps.models import User
    # users_emails = User.objects.values_list('email', flat=True)
    send_mail(f'Yangi mahsulot {product_name}', F'Saytimizga kirib koring {url}', EMAIL_HOST_USER, users_emails)

