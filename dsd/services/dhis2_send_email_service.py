from django.core.mail import send_mail


def dhis2_send_email(subject, content, sender, receivers):
    send_mail(subject, content, sender, receivers, fail_silently=False)