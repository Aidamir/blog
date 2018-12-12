from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_mass_mail_template(template, users, subject, context={}):
    plaintext = get_template(template + '.txt')
    html = get_template(template + '.html')
    messages = list()

    for u in users:
        if not u.email:
            continue
        context['user'] = u
        from_email, to = settings.DEFAULT_FROM_EMAIL, u.email
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        messages.append(msg)

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()