from django.core.mail import send_mail


def dhis2_send_email(subject, content, sender, receiver):
    send_mail(subject, content, sender, receiver, fail_silently=False)