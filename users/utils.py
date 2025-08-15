import logging 
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail


logger=logging.getLogger(__name__)


def send_email_with_html_body(subject: str, receivers: list, template: str, context=dict):
    """This function helps to send a customize email to a specific user or set of users"""
    try:
        message=render_to_string(template, context)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=True,
            html_message=message,
            recipient_list=receivers
        )
        return True
        
    except Exception as e:
        logger.error(e)
    
    return False


def send_email_with_html_body_to_school_for_connexion_key(subject: str, receivers: list, template: str, context=dict):
    """This function helps to send a customize email to a specific user or set of users"""
    try:
        message=render_to_string(template, context)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=True,
            html_message=message,
            recipient_list=receivers
        )
        return True
        
    except Exception as e:
        logger.error(e)
    
    return False
