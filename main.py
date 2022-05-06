from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests

header = {
    'Accept': 'text/html, /; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,ja;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'info.hansung.ac.kr',
    'Referer': 'https://info.hansung.ac.kr/jsp/sugang/h_sugang_sincheong_main.jsp',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

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
    ans = session.get("https://info.hansung.ac.kr/jsp_21/student/grade/total_grade.jsp?viewMode=oc", headers=header).text

    if "parent.location = '/index.jsp';" in ans:
        print("로그인 에러")
    else:
        print(ans)

    return account