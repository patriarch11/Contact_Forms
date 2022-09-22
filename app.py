from fastapi import FastAPI, Depends
# from fastapi.responses import HTMLResponse
from schemas import FollowingForm

app = FastAPI()


@app.post('/sales')
def post_following_form(form_data: FollowingForm = Depends(FollowingForm.as_form)):
    if dict(form_data)['copy_'] == True:
        pass
    #  we need to CC the email to workEmail address
    else:
        pass
    # send email only to sales@domain.com
    return form_data.json()
