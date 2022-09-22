from fastapi import FastAPI, Depends, Form
from schemas import SalesForm
from dotenv import load_dotenv
import os
import boto3

load_dotenv('.env')
app = FastAPI()
# connecting to db
dynamo_client = boto3.resource(
    service_name=os.getenv('SERVICE_NAME'),
    region_name=os.getenv('REGION_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
# creating table
form_data_table = dynamo_client.Table('form_data_table')


# handling post sales form
@app.post('/sales')
async def post_sale_form(form_data: SalesForm = Depends(SalesForm.as_form)):
    if dict(form_data)['copy_'] == True:
        # CC the email to workEmail address
        pass
    else:
        # send email only to sales@domain.com
        pass
    form_data_table.put_item(Item=dict(form_data))  # Put everything we got into DynamoDB.


@app.post('/security')
async def post_security_form(to: str = Form(...)):
    pass