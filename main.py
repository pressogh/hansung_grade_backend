from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=443)), log_level="info")