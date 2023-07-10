from celery import shared_task
from django.core.mail import send_mail
from apps.authentication.models import User
from django.utils import timezone
from django.conf import settings

@shared_task
def wish_birthday() -> None:
    users = User.objects.filter(
        date_of_birth = timezone.now()
    )
    
    for user in users:
        print(f'Happy {user.first_name}')
        
        subject = f"Happy Birthday {user.first_name} {user.last_name} !"
        message = f"Happy Birthday {user.first_name} {user.last_name} !!! Have a great year ahead !"
        
        send_mail(
            subject,
            message,
            settings['EMAIL_HOST_USER'],
            [f'{user.email}'],
            fail_silently = True
        )