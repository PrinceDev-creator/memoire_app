import logging 
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags


logger=logging.getLogger(__name__)

def send_preg_email_with_html_body_to_school(subject: str, receivers: list, template: str, context: dict): #email de pré-inscription
    
    print('email1')
    
    try:
        message = render_to_string(template, context)
        plain_message = strip_tags(message)  # Version texte pour les clients non HTML
        
        send_mail(
            subject=subject,
            message=plain_message,  # Version texte
            from_email=settings.DEFAULT_FROM_EMAIL,  # Préférez ceci à EMAIL_HOST_USER
            recipient_list=receivers,
            fail_silently=False,  # Mettez à False pour voir les erreurs
            html_message=message,  # Version HTML
        )
        return True
    except Exception as e:
        logger.error(f"Erreur d'envoi d'email: {str(e)}", exc_info=True)
        return False
    
def send_preg_email_with_html_body_to_app_team(subject: str, receivers: list, template: str, context: dict):
    
    print('email2')
    
    try:
        message = render_to_string(template, context)
        plain_message = strip_tags(message)  # Version texte pour les clients non HTML
        
        send_mail(
            subject=subject,
            message=plain_message,  # Version texte
            from_email=settings.DEFAULT_FROM_EMAIL,  # Préférez ceci à EMAIL_HOST_USER
            recipient_list=receivers,
            fail_silently=False,  # Mettez à False pour voir les erreurs
            html_message=message,  # Version HTML
        )
        return True
    except Exception as e:
        logger.error(f"Erreur d'envoi d'email: {str(e)}", exc_info=True)
        return False