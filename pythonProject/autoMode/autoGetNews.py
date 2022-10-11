from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
from datetime import datetime
import getNews
from pynotifier import Notification

def init(bookList):
    recNewsDict = {}
    for key, _ in bookList.items():
        try:
            f = open(f'userData/news/{key}.txt', 'r')
            line = f.readline()[:-1]
            recNewsDict[key] = line
            f.close()
        except:
            f = open(f'userData/news/{key}.txt', 'w')
            f.close()
            recNewsDict[key] = ''
    return recNewsDict

def get(newsDict):
    for key, val in newsDict.items():
        dfOrderByTime = pd.DataFrame(index=range(0, 0), columns=['언론', '제목', '링크'])
        flag = False
        titleText = []
        pressText = []
        links = []
        for page in range(1, 31):
            page = (10 * (page - 1)) + 1
            url = f'https://search.naver.com/search.naver?where=news&query={key}&sm=tab_opt&sort={1}&start={page}'
            html = requests.get(url)
            soup = bs(html.text, 'html.parser')

            data = soup.find('div', {'class': 'group_news'})

            titles = data.find_all('a', {'class': 'news_tit'})
            presses = data.find_all('a', {'class': 'info press'})

            for i in range(len(titles)):
                if titles[i].text == val:
                    flag = True
                    break
                titleText.append(titles[i].text)
                pressText.append(presses[i].text.strip('언론사 선정'))
                links.append(titles[i]['href'])
            if flag:
                break

        for row in range(0, len(titleText)):
            dfOrderByTime.loc[row] = [pressText[row], titleText[row], links[row]]
            row += 1

        if len(titleText) > 0:
            f = open(f'userData/news/{key}.txt', 'w')
            f.write(titleText[0] + '\n')
            f.close()

            now = datetime.now()
            dt = now.strftime('%y%m%d %H:%M:%S')
            os.makedirs('autoNews/' + key, exist_ok=True)

            file = f'autoNews/{key}/[{dt}]{key}.xlsx'
            dfOrderByTime.to_excel(file)
            getNews.editExcel(file)
            Notification(
                title='새로운 정보를 발견!',
                description=f'****{key}의 뉴스 정보가 업데이트됨****',
                duration=100
            ).send()
            print(f'****{key}의 뉴스 정보가 업데이트됨****')