from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class SendEmail(BaseModel):
    """Un mensaje que se enviará al usuario"""
    message: str = Field(..., description="El mensaje que se enviará al usuario.")

class SendEmailTool(BaseTool):

    name: str = "Enviar una email"
    description: str = (
        "Esta herramienta se utiliza para enviar un email al usuario."
    )
    args_schema: Type[BaseModel] = SendEmail

    def _run(self, message: str) -> str:
        print(f"Email: {message}")
        from_email = os.getenv('MAILGUN_FROM')
        to_email = "Javier <surtich@gmail.com>"
        content = message

        requests.post(
            f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_SANDBOX')}/messages",
            auth=("api", os.getenv('MAILGUN_API_KEY')),
            data={"from": from_email,
                "to": to_email,
                "subject": "Notificación de Stock Picker",
                "html": content})
        return '{"notification": "ok"}'
