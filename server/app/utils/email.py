from typing import Any, Dict, Mapping, Optional

import emails
from emails.template import JinjaTemplate
from pydantic import EmailStr

from app.core.config import get_app_settings
from app.exceptions.custom import InvalidStateException


def send_email(
    email_to: EmailStr,
    subject_template: str = "",
    html_template: str = "",
    environment: Mapping[str, Any] = {},
    email_from_email: Optional[str] = None,
    email_from_name: Optional[str] = None,
) -> Optional[Dict[str, str]]:
    settings = get_app_settings()
    if not settings.EMAILS_ENABLED:
        raise InvalidStateException("no provided configuration for email variables")

    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(
            email_from_name or settings.EMAILS_FROM_NAME,
            email_from_email or settings.EMAILS_FROM_EMAIL,
        ),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    try:
        response = message.send(to=email_to, render=environment, smtp=smtp_options)
        print(f"Send email result: {response}")
        return {
            "id": response.status_text.decode("utf8").split("queued as ")[1],
            "status": ("SUCCESS" if response.success else "FAILED"),
        }

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return None
