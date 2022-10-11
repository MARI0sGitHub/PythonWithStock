import json
import requests
import os
from datetime import datetime
import pandas as pd
import getStock
#공시정보 파일을 받아 공시정보를 배열에 담아 반환

def check(s):
    if len(s) != 8:
        return False
    if s.isdigit():
        return True
    return False

def getList(key, corp, s, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET):
    url = "https://opendart.fss.or.kr/api/list.json?"
    crtfc_key = key
    corp_code = corp
    start = ""
    end = ""
    while True:
        print('공시정보 시작일(반드시 \'YYYYMMDD\'형식으로 입력해 주세요!):', end='')
        start = input()
        if check(start):
            break
    while True:
        print('공시정보 종료일(반드시 \'YYYYMMDD\'형식으로 입력해 주세요!), (0입력시 현재 날짜로 설정):', end='')
        end = input()
        if end == '0':
            end = ""
            break
        if check(end):
            break

    if end == "":
        now = datetime.now()
        end = now.strftime('%Y%m%d')
    response = requests.get(f'{url}crtfc_key={crtfc_key}&corp_code={corp_code}&bgn_de={start}&end_de={end}')
    item = json.loads(response.text)
    if item.get('message') == '정상':
        arr = item.get('list')
        # 기업의 공시정보를 저장하는 과정...
        df = pd.DataFrame(index=range(0, 0), columns=['법인구분', '종목명', '보고서명', '접수번호', '공시 제출인명', '접수일자', '비고', '공시 링크'])
        row = 0
        # 종목코드
        stock_code = ""
        for data in arr:
            if stock_code == "":
                stock_code = data.get('stock_code')
            df.loc[row] = [
                data.get('corp_cls'),
                data.get('corp_name'),
                data.get('report_nm'),
                data.get('rcept_no'),
                data.get('flr_nm'),
                data.get('rcept_dt'),
                data.get('rm'),
                'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + data.get('rcept_no')
            ]
            row += 1
        now = datetime.now()
        dt = now.strftime('%Y-%m-%d')
        # 공시 정보 저장 완료, gongsi 폴더 -> 현재 날짜 폴더 -> 공시정보 엑셀 파일
        os.makedirs('gongSi/' + dt, exist_ok=True)
        fileName = 'gongSi/' + dt + '/' + s + '[' + start + '-' + end + ']' + '.xlsx'
        df.to_excel(fileName)

        stock = getStock.get(s, stock_code, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET)
        if stock_code != '':
            print('종목코드:', stock_code)
            print('현재 주가:', stock)
        else:
            print('현재 상장 되어 있지 않은 종목')
        return fileName
    elif item.get('message') == '조회된 데이타가 없습니다.':
        print('데이터를 찾을 수 없습니다')
        return ""
    else:
        print('날짜 형식이 잘못되었습니다 다시 확인 하시고 시도 하여 주세요')
        return ""