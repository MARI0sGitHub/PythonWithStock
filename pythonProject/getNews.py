from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook

def editExcel(fileName):
    wb = load_workbook(fileName)
    ws = wb.active
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 100
    ws.column_dimensions['D'].width = 80
    wb.save(fileName)

def get(query):
    mode = ''
    print()
    print('=============뉴스 가져오기=================')
    while True:
        print('모드 입력(0 정확도 순, 1 최신 순):', end = '')
        s = input()
        if s != '0' and s != '1':
            print('!!잘못된 입력!!')
            continue
        mode = s
        break

    start = 0
    end = 0

    while True:
        print('탐색할 범위 시작(1이상):', end = '')
        s = input()
        if s.isdigit() == False:
            print('!!숫자 형식이 아님!!')
            continue
        elif int(s) < 1:
            print('!!0보다 큰 수를 입력!!')
            continue
        start = int(s)
        break

    while True:
        print(f'탐색할 범위 끝({s}이상):', end = '')
        s = input()
        if s.isdigit() == False:
            print('!!숫자 형식이 아님!!')
            continue
        elif int(s) < start:
            print(f'!!{start}이상의 수를 입력!!')
            continue
        end = int(s)
        break

    rowTime = 0
    rowPress = 0
    dfOrderByTime = pd.DataFrame(index=range(0, 0), columns=['언론', '제목', '링크'])
    dfOrderByPress = pd.DataFrame(index=range(0, 0), columns=['언론', '제목', '링크'])
    dictionary = dict()

    for page in range(start, end + 1):
        page = (10 * (page - 1)) + 1
        url = f'https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort={mode}&start={page}'
        html = requests.get(url)
        soup = bs(html.text, 'html.parser')

        data = soup.find('div', {'class' : 'group_news'})

        titles = data.find_all('a', {'class' : 'news_tit'})
        presses = data.find_all('a', {'class' : 'info press'})

        titleText = []
        pressText = []
        links = []


        for i in range(len(titles)):
            titleText.append(titles[i].text)
            pressText.append(presses[i].text.strip('언론사 선정'))
            links.append(titles[i]['href'])

            if (presses[i].text.strip('언론사 선정') in dictionary) == False:
                temp = [ [ titles[i].text, titles[i]['href'] ] ]
                dictionary[presses[i].text.strip('언론사 선정')] = temp
            else:
                dictionary[presses[i].text.strip('언론사 선정')].append([titles[i].text, titles[i]['href']])

        now = datetime.now()
        dt = now.strftime('%Y-%m-%d')
        os.makedirs('news/' + dt, exist_ok=True)

        for row in range(0, len(titleText)):
            dfOrderByTime.loc[rowTime] = [pressText[row], titleText[row], links[row]]
            rowTime += 1

    if mode == '0':
        mode = '정확도순'
    else:
        mode = '최신순'
    # 엑셀 파일에서 윗행일 수록 최신 기사
    dfOrderByTime.to_excel(f'news/{dt}/[{start} - {end}]{query}[{mode}, 시간 기준 정렬].xlsx')

    for key, val in dictionary.items():
        for data in val:
            title = data[0]
            link = data[1]
            dfOrderByPress.loc[rowPress] = [key, title, link]
            rowPress += 1
    dfOrderByPress.to_excel(f'news/{dt}/[{start} - {end}]{query}[{mode}, 언론사 기준 정렬].xlsx')

    return [
        f'news/{dt}/[{start} - {end}]{query}[{mode}, 시간 기준 정렬].xlsx',
        f'news/{dt}/[{start} - {end}]{query}[{mode}, 언론사 기준 정렬].xlsx'
    ]