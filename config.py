from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
class FormSettings(BaseSettings):

    # set up mail
    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    mail_port: int
    mail_from_name: str
    mail_subject_line: str
    mail_tls: bool = True
    mail_ssl: bool = False
    use_credentials: bool = True
    validate_credentials: bool = True

    # set up s3
    region_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    table_name: str
    bucket_name: str

settings = FormSettings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)

