import os
import smtplib
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .threading import EmailThread


def generate_token(email):
    dt = datetime.now() + timedelta(days=1)

    token = jwt.encode({
        'email': email,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')
    if (isinstance(token, bytes)):
        return token.decode('utf-8')
    return token


def account_url_metadata(request):
    email = request.data.get('email')
    token = generate_token(email)
    protocol_secure = request.is_secure()
    if protocol_secure:
        protocol = 'https://'
    else:
        protocol = 'http://'
    uid = urlsafe_base64_encode(force_bytes(
        email))
    env = os.getenv('ENVIRONMENT')
    test_and_staging_env = ['local', 'postgres_local', 'test', 'dev']
    host = ''
    if env in test_and_staging_env:
        host = request.get_host()
    if env == 'prod':
        host = 'www.thenewboston.com'
    return (token, host, protocol, uid)


def send_account_email(request, subject, path):
    token, host, protocol, uid = account_url_metadata(request)
    email = request.data.get('email')
    display_name = request.data.get('display_name', '')
    link = protocol + host + path + '/' + uid + '/' + token
    to_email = email
    from_email = os.getenv('DEFAULT_FROM_EMAIL')
    s = smtplib.SMTP()
    s.connect(os.getenv('SMTP_SERVER'), 587)
    s.starttls()
    s.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
    msg = 'From: ' + from_email + '\nTo: ' + to_email + '\nSubject: ' + subject + '\n\nHi' + \
        display_name + '\nThank you for registering an account with thenewboston!\nPlease confirm your'\
        'account by clicking the link below\n\n' + link
    EmailThread(s, from_email, to_email, msg).start()
