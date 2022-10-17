from typing import List

from fastapi import FastAPI, Form, UploadFile, File
from pydantic import EmailStr
from starlette.responses import JSONResponse

from config import settings
from services import get_custom_connect_config, get_boto3_client, send_mail, upload_files_to_s3

app = FastAPI()


@app.post('/sales')
async def post_sales(

        snrs: bool = Form(False),
        dmarc: bool = Form(False),
        emailsecurity: bool = Form(False),
        aws: bool = Form(False),
        dns: bool = Form(False),
        services: bool = Form(False),

        firstName: str = Form(),
        lastName: str = Form(),
        phone: str = Form(),
        org: str = Form(),
        workEmail: EmailStr = Form(),
        message: str = Form(),
        copy: bool = Form(False)

) -> JSONResponse:

    conf = get_custom_connect_config(settings.mail_from)
    client_dynamo = get_boto3_client('dynamodb')
    # connect to table, which already exists and have a columns(param of function)
    form_data_table = client_dynamo.Table(settings.table_name)

    if copy: # CC the email to workEmail address
        await send_mail(config=conf, email=[workEmail], message=message)

    else:
        await send_mail(config=conf, email=['sales@domain.com'], message=message)

    form_data_table.put_item(Item={
        'snrs': snrs,
        'dmarc': dmarc,
        'emailsecurity': emailsecurity,
        'aws': aws,
        'dns': dns,
        'services': services,
        # Put everything we got into DynamoDB.
        'firstName': firstName,
        'lastName': lastName,
        'phone': phone,
        'org': org,
        'workEmail': workEmail,
        'message':  message,
        'copy': copy
    })


    return JSONResponse(
        status_code=200,
        content={"message": "email has been sent, data from form inserted success"}
    )

@app.post('/security')
async def post_security(
        to: EmailStr = Form(),
        workEmail: EmailStr = Form(),
        message: str = Form(),
        files: list[UploadFile] = File(None)
) -> JSONResponse:
    conf = get_custom_connect_config(mail_from=workEmail)

    if files is not None:
        await send_mail(config=conf, email=[to], message=message, attachments=files)
        await upload_files_to_s3(files)
        return JSONResponse(status_code=200, content={"message": "email has been sent, all files uploaded to s3"})

    await send_mail(config=conf, email=[to], message=message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


