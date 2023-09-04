from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
import random


def generate_otp_code():
    print("Generating OTP Code...")
    otp_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    print(f'Generated OTP Code: {otp_code}')
    return otp_code


@shared_task
def send_otp_email(email):
    try:
        otp_code = generate_otp_code()
        print(f'Email: {email}')
        print(f'Generated OTP Code: {otp_code}')

        subject = 'Your OTP Code'
        message = f'Your OTP code is: {otp_code}'
        from_email = 'gurkin22@yandex.ru'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        cache.set(f'otp_code_{email}', otp_code, 300)
        return "OTP code sent successfully"
    except Exception as e:
        return f"Task failed with error: {str(e)}"
