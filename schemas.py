from fastapi import Form, File, UploadFile
from fastapi_mail import ConnectionConfig
from pydantic import BaseModel
from pathlib import Path
import os

# regex for checking valid email address
VALID_EMAIL_VALUE = r'^[a-zA-Z0-9](-?[a-zA-Z0-9_])+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*$'


# schema for sales web form
class SalesForm(BaseModel):
    snrs: bool
    dmarc: bool
    emailsecurity: bool
    aws: bool
    dns: bool
    services: bool
    firstName: str
    lastName: str
    phone: str
    org: str
    workEmail: str
    message: str
    copy_: bool

    @classmethod
    def as_form(cls,
                snrs: bool = Form(False),
                dmarc: bool = Form(False),
                emailsecurity: bool = Form(False),
                aws: bool = Form(False),
                dns: bool = Form(False),
                services: bool = Form(False),
                firstName: str = Form(...),
                lastName: str = Form(...),
                phone: str = Form(...),
                org: str = Form(...),
                workEmail: str = Form(..., regex=VALID_EMAIL_VALUE),  # check for valid value
                message: str = Form(...),
                copy_: bool = Form(False)  # Field name "copy" shadows a BaseModel attribute
                ):
        return cls(
            snrs=snrs,
            dmarc=dmarc,
            emailsecurity=emailsecurity,
            aws=aws,
            dns=dns,
            services=services,
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            org=org,
            workEmail=workEmail,
            message=message,
            copy_=copy_
        )


# schemas for sending email
class EmailSchema(BaseModel):
    to: str
    workEmail: str
    message: str
    files: UploadFile

    @classmethod
    def as_form(cls, to: str = Form(...), workEmail: str = Form(..., regex=VALID_EMAIL_VALUE),  # check for valid value
                message: str = Form(...), file: UploadFile = File(None)):
        return cls(to=to, workEmail=workEmail, message=message, file=file)


# get custom connection config for sending mail
def get_custom_connection_config(mail_from) -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=f"{os.getenv('MAIL_USERNAME')}",
        MAIL_PASSWORD=f"{os.getenv('MAIL_PASSWD')}",
        MAIL_FROM=f"{mail_from}",
        MAIL_PORT=f"{os.getenv('MAIL_PORT')}",
        MAIL_SERVER=f"{os.getenv('MAIL_SERVER')}",
        MAIL_FROM_NAME=F"{os.getenv('MAIL_FROM_NAME')}",
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
    )
