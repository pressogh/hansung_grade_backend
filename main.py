from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import requests
from util import parse

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Account(BaseModel):
    username: str
    password: str

@app.post("/api/grade")
async def get_grade(account: Account):
    id = account.username
    passwd = account.password

    data = {
        "id": id,
        "passwd": passwd,
        "changePass": "",
        "return_url": "null"
    }
    
    session = requests.Session()
    session.post("https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl", data=data)

    return parse(session, "https://info.hansung.ac.kr/jsp_21/student/grade/total_grade.jsp?viewMode=oc")