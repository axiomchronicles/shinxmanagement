from aquilify.core import mail
from aquilify.core.mail import BadHeaderError
from aquilify import shortcuts
from aquilify.settings import settings

def send_email(subject: str, message:str, recipient: str, context: dict, template_name: str ):
    try:
        
        subject = subject
        message = message
        from_email = settings.DEFAULT_FROM_EMAIL
        from_name = f"Shinx Team"
        from_email_with_name = f'"{from_name}" <{from_email}>'
        recipient_list = [recipient]
        html_message = shortcuts.render_from_string(
                template_name = template_name, context = context if context else None
            )
        
        mail.send_mail(
            subject,
            message,
            from_email_with_name,
            recipient_list,
            html_message=html_message
        )
        return True
    except (BadHeaderError, Exception) as e:
        print(f"Error sending email: {e}")
        return False  # Email failed to send