from fastapi import Form
from pydantic import BaseModel


class FollowingForm(BaseModel):
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
                workEmail: str = Form(..., regex=r'^[a-zA-Z0-9](-?[a-zA-Z0-9_])+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*$'),
                message: str = Form(...),
                copy_: bool = Form(False)  # cause 'copy' is base attribute of base model
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
