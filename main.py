from functools import lru_cache
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

import requests

import config
from util import *

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


@lru_cache()
def get_settings():
    if os.getenv("DEBUG") == "true":
        return config.Settings(_env_file=".env.dev")

    return config.Settings()


@app.post("/api/grade")
async def getGrade(account: Account, settings: config.Settings=Depends(get_settings)):
    username = account.username
    passwd = account.password

    data = {
        "id": username,
        "passwd": passwd,
        "changePass": "",
        "return_url": "null"
    }

    session = requests.Session()
    session.post(settings.LOGIN_URL, data=data)

    return parseGrade(session, settings.GRADE_URL)


@app.post("/api/nowgrade")
async def getNowGrade(account: Account, settings: config.Settings=Depends(get_settings)):
    username = account.username
    passwd = account.password

    data = {
        "id": username,
        "passwd": passwd,
        "changePass": "",
        "return_url": "null"
    }

    session = requests.Session()
    session.post(settings.LOGIN_URL, data=data)

    return parseNowGrade(session, settings.NOW_SEMESTER_GRADE_URL)


@app.post("/api/info")
async def getInfo(account: Account, settings: config.Settings=Depends(get_settings)):
    username = account.username
    passwd = account.password

    data = {
        "id": username,
        "passwd": passwd,
        "changePass": "",
        "return_url": "null"
    }

    session = requests.Session()
    session.post(settings.LOGIN_URL, data=data)

    return parseInfo(session, settings.INFO_URL)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=443)), log_level="info")
