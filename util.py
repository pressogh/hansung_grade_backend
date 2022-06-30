from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bs4 import BeautifulSoup as bs4
import re
import json

from data import HEADER

header = HEADER

gradeWeight = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F0": 0.0,
    "P": 1.0,
    "N": 0.0
}


def parseGrade(session, address):
    grade_page = session.get(address, headers=header).text

    if len(grade_page) < 1000:
        raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못되었습니다.")

    soup = bs4(grade_page[40000:], 'lxml')
    data = soup.select('div.row > div[class="col-12 col-lg-6 col-print-6"]')

    credits_string = ["register_credits", "earned_credits", "total_score", "average_credits", "percentile"]
    subject_string = ["classification", "name", "code", "credits", "grade", "track"]

    resList = []
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
            subject_item = htmlToText(sub)
            subject_dict[subject_string[len(subject_dict)]] = subject_item

            if len(subject_dict) >= 6:
                subject_2dlist.append(subject_dict)
                subject_dict = {}
        res["subject"] = subject_2dlist
        resList.append(res)

    # res_json = jsonable_encoder(json.dumps(res_list, indent="\t", ensure_ascii=False))
    return JSONResponse(content=resList)


def parseNowGrade(session, address):
    now_semester_grade_page = session.get(address, headers=header).text

    if len(now_semester_grade_page) < 1000:
        raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못되었습니다.")

    soup = bs4(now_semester_grade_page, 'lxml')

    semester = htmlToText(soup.select('table')[1].select('tr > td')[2])[:11]
    data = soup.select('table')[3].select('tr')[1:]

    res = {}
    subject_list = []
    dataTitle = {
        "1": "code",
        "2": "name",
        "4": "classification",
        "5": "credits",
        "9": "grade"
    }

    total_credits, register_credits, earned_credits, total_score = 0, 0, 0, 0
    needIndex = [1, 2, 4, 5, 9]
    for item in data:
        itemList = item.select('td')

        itemDict = {}
        index, lastCredits = 0, ""
        for p in itemList:
            p = htmlToText(p)

            if index in needIndex:
                itemDict[dataTitle[str(index)]] = p

                if index == 5:
                    register_credits += int(p)
                    lastCredits = p
                if index == 9:
                    total_credits += gradeWeight[p]
                    if p != "F0" and p != "N":
                        earned_credits += int(lastCredits)

                    total_score += gradeWeight[p] * int(lastCredits)

            index += 1

        subject_list.append(itemDict)

    # 학점 : 성적의 총 합 / 수강 학점의 총 합
    res["average_credits"] = str(total_credits / len(subject_list))[:4]
    # 얻은 학점 : 수강 학점의 총 합 - f나 np를 받은 과목 학점의 총 합
    res["register_credits"] = register_credits
    res["earned_credits"] = earned_credits
    res["semester"] = semester
    res["subject"] = subject_list
    res["total_score"] = total_score

    return JSONResponse(content=res)


def parseInfo(session, address):
    info_page = session.get(address, headers=header).text

    if len(info_page) < 1000:
        raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못되었습니다.")

    soup = bs4(info_page[4000:], 'lxml')

    data = soup.select('table[class="table table-condensed"] > tr > td')

    res = {}
    res["pic"] = "https://info.hansung.ac.kr/tonicsoft/jik/register/" + data[0].select('img[name="sajin"]')[0].attrs["src"]

    needData = ["성명", "제1트랙", "제2트랙", "학년", "상태", "입학일자"]
    dataTitle = ["name", "track1", "track2", "grade", "status", "admission_date"]

    index = 0
    flag = False
    for item in data:
        p = htmlToText(item)

        if flag:
            res[dataTitle[index]] = p
            index += 1
            flag = False

            if index >= len(needData):
                break

        elif p.find(needData[index]) != -1:
            flag = True

    # res_json = jsonable_encoder(json.dumps(res, indent="\t", ensure_ascii=False))
    return JSONResponse(content=res)


def htmlToText(html):
    return re.sub(pattern="<[^>]*>", repl="", string=html.text.strip()).replace(" ", "")