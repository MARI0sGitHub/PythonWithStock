from datetime import datetime
import json
import requests
import os
import pandas as pd
from pynotifier import Notification
import setGongSiExcel

now = datetime.now()

def init(bookList):
    recentData = dict()
    today = now.strftime('%Y-%m-%d')
    os.makedirs('userData/gongSi/' + today, exist_ok=True)
    for key, _ in bookList.items():
        try:
            f = open(f'userData/gongSi/{today}/{key}.txt', 'r')
            lines = f.readlines()
            temp = dict()
            for line in lines:
                temp[line[:-1]] = True
            recentData[key] = temp
        except:
            f = open(f'userData/gongsi/{today}/{key}.txt', 'w')
            f.close()
            recentData[key] = dict()
    return recentData

def lookFor(Data, key, corp):
    start = now.strftime('%Y%m%d')
    end = now.strftime('%Y%m%d')
    url = "https://opendart.fss.or.kr/api/list.json?"
    crtfc_key = key
    for key, val in Data.items():
        corp_code = corp[key]
        response = requests.get(f'{url}crtfc_key={crtfc_key}&corp_code={corp_code}&bgn_de={start}&end_de={end}')
        item = json.loads(response.text)
        if item.get('message') == '정상':
            arr = item.get('list')
            news = []
            for i in range(0, len(arr)):
                new = arr[i].get('rcept_no')
                if new in val:
                    continue
                else:
                    news.append(i)
                    Data[key][new] = True

            if len(news) > 0:
                print(key)
                today = now.strftime('%Y-%m-%d')
                df = pd.DataFrame(index=range(0, 0),
                                  columns=['법인구분', '종목명', '보고서명', '접수번호', '공시 제출인명', '접수일자', '비고', '공시 링크'])
                f = open(f'userData/gongsi/{today}/{key}.txt', 'a')
                row = 0
                for idx in news:
                    f.write(arr[idx].get('rcept_no') + '\n')
                    df.loc[row] = [
                        arr[idx].get('corp_cls'),
                        arr[idx].get('corp_name'),
                        arr[idx].get('report_nm'),
                        arr[idx].get('rcept_no'),
                        arr[idx].get('flr_nm'),
                        arr[idx].get('rcept_dt'),
                        arr[idx].get('rm'),
                        'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + arr[idx].get('rcept_no')
                    ]
                    row += 1
                f.close()
                os.makedirs('autoGongSi/' + today, exist_ok=True)
                fileName = 'autoGongSi/' + today + '/' + key + '[' + start + ']' + '.xlsx'
                df.to_excel(fileName)
                setGongSiExcel.set(fileName)
                Notification(
                    title='새로운 정보를 발견!',
                    description=f'****{key}의 공시 정보가 업데이트됨****',
                    duration=100
                ).send()
                print(f'****{key}의 공시 정보가 업데이트됨****')