from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bs4 import BeautifulSoup as bs4
import re
import json

from data import HEADER

header = HEADER


def parse(session, address):
    grade_page = session.get(address, headers=header).text

    if len(grade_page) < 1000:
        return HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못되었습니다.")

    soup = bs4(grade_page[40000:], 'lxml')
    data = soup.select('div.row > div[class="col-12 col-lg-6 col-print-6"]')

    credits_string = ["register_credits", "earned_credits", "total_score", "average_credits", "percentile"]
    subject_string = ["classification", "name", "code", "credits", "grade", "track"]

    res_list = []
    for item in data:
        res = {}
        semester = re.sub(pattern="<[^>]*>", repl="",
                          string=item.select('span[class="objHeading_h3 text-white"]')[0].text).strip()
        res["semester"] = semester

        credits = item.select('div[class="div_sub_subdiv card card-info"] > div[class="card-body"]')
        credits_list = []
        for cre in credits:
            credits_item = re.sub(pattern="<[^>]*>", repl="", string=cre.text).strip()
            credits_list.append(credits_item)
        for cre_str, cre in zip(credits_string, credits_list):
            res[cre_str] = cre

        subject = item.select('table[class="table_1"] > tbody > tr > td')
        subject_2dlist = []
        subject_dict = {}
        for sub in subject:
            subject_item = re.sub(pattern="<[^>]*>", repl="", string=sub.text).strip()
            subject_dict[subject_string[len(subject_dict)]] = subject_item

            if len(subject_dict) >= 6:
                subject_2dlist.append(subject_dict)
                subject_dict = {}
        res["subject"] = subject_2dlist
        res_list.append(res)

    res_json = jsonable_encoder(json.dumps(res_list, indent="\t", ensure_ascii=False))
    return JSONResponse(content=res_json)
