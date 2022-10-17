from pathlib import Path
from typing import List

import boto3
from fastapi import UploadFile
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from pydantic import EmailStr, BaseModel

from config import settings

class EmailSchema(BaseModel):
    email: List[EmailStr]


def get_custom_connect_config(mail_from: EmailStr) -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_FROM_NAME=settings.mail_from_name,
        MAIL_TLS=settings.mail_tls,
        MAIL_SSL=settings.mail_ssl,
        USE_CREDENTIALS=settings.use_credentials,
        VALIDATE_CERTS=settings.validate_credentials,
        TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
    )
# getting boto3 client like database or aws storage
def get_boto3_client(service_name: str):
    return  boto3.resource(
        service_name=service_name,
        region_name=settings.region_name,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

async def send_mail(
        config: ConnectionConfig,
        email: EmailSchema,
        message: str,
        attachments: list[UploadFile] = None
) -> None:
    if attachments is not None:
        message_schema = MessageSchema(
            subject_line=settings.mail_subject_line,
            recipients=email,
            body=message,
            attachments=attachments
        )
    else:
        message_schema = MessageSchema(
            subject_line=settings.mail_subject_line,
            recipients=email,
            body=message,
        )

    fm = FastMail(config=config)
    await fm.send_message(message_schema, template_name="email_template.html")

async def upload_files_to_s3(files: list[UploadFile]):

    client_s3 = get_boto3_client(service_name='s3')

    for file in files:
        client_s3.Bucket(
            settings.bucket_name
        ).upload_fileobj(file.file, file.filename)
