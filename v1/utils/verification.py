import os
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def generate_token(email):
    dt = datetime.now() + timedelta(days=1)

    token = jwt.encode({
        'email': email,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


def account_url_metadata(data, host, protocol_secure):
    email = data.get('email')
    token = generate_token(email)
    if protocol_secure:
        protocol = 'https://'
    else:
        protocol = 'http://'
    uid = urlsafe_base64_encode(force_bytes(
        email))

    return (token, host, protocol, uid)


def send_account_email(data, host, protocol_secure, subject, path, template):
    token, host, protocol, uid = account_url_metadata(data, host, protocol_secure)
    email = data.get('email')
    display_name = data.get('display_name')
    message = render_to_string(
        template, {
            'domain': host,
            'uid': uid,
            'name': display_name,
            'link': protocol + host + path + '?key=' + token
        })

    to_email = email
    from_email = os.getenv('DEFAULT_FROM_EMAIL')

    send_mail(
        subject,
        'thenewboston',
        from_email, [
            to_email,
        ],
        html_message=message,
        fail_silently=False
    )
