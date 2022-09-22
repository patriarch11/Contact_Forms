from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from schemas import FollowingForm

app = FastAPI()


@app.post('/sales', response_class=HTMLResponse)
def post_following_form(form_data: FollowingForm = Depends(FollowingForm.as_form)):
    return form_data.json()
