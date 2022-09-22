from fastapi import FastAPI, Depends, UploadFile, File
from starlette.responses import JSONResponse
from schemas import SalesForm, EmailSchema
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
import boto3
from pathlib import Path

load_dotenv('.env')
app = FastAPI()

# creating session
session = boto3.Session(
    region_name=os.getenv('REGION_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))


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


# upload file to s3
def s3_upload(file_obj: UploadFile = File(...)):
    # Creating S3 Resource From the Session
    pass


# handling post sales form
@app.post('/sales')
async def post_sale_form(form_data: SalesForm = Depends(SalesForm.as_form)) -> JSONResponse:
    conf = get_custom_connection_config('your_email_from@domain.com')

    if dict(form_data)['copy_'] == True:  # CC the email to workEmail address
        message = MessageSchema(
            subject='subject line',
            recepients=[dict(form_data)['workEmail']],
            body=dict(form_data)['message'],
        )
    else:  # send email only to sales@domain.com
        message = MessageSchema(
            subject='subject line',
            recepients=['sales@domain.com'],
            body=dict(form_data)['message'],
        )

    # connecting to db
    dynamo_client = session.resource(service_name='dynamodb')
    # creating table
    form_data_table = dynamo_client.Table('form_data_table')
    # insert values from ford_data to table
    form_data_table.put_item(Item=dict(form_data))  # Put everything we got into DynamoDB.

    fm = FastMail(config=conf)
    await fm.send_message(message, template_name="email_template.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent, data from form inserted success"})


# handling post security from and send mail with async
@app.post('/security')
async def post_security_form(email: EmailSchema = Depends(EmailSchema.as_form)) -> JSONResponse:
    # getting connect configuration
    conf = get_custom_connection_config(email.workEmail)

    if dict(email)['file']:  # if attachments is not empty
        message = MessageSchema(
            subject='subject line',
            recepients=[email.to],
            body=email.message,
            attachments=[dict(email)['file']]
        )
    else:  # if attachments is empty
        message = MessageSchema(
            subject='subject line',
            recepients=[email.to],
            body=email.message,
        )
    s3_upload(dict(email)['file'])
    fm = FastMail(config=conf)
    await fm.send_message(message, template_name="email_template.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
