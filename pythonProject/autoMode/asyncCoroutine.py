import asyncio
import time
from autoMode import autoGetStock
from autoMode import autoGetGongSi
from autoMode import autoGetNews

async def test():
    print('뉴스는 최대 30페이지 까지만 가져옴')
    print('**********탐색 모드 시작***********')
    await asyncio.sleep(10)
    print('*')


async def search(newsDict, recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET, gongsiData, DART_KEY, CORP_INFO):
    print('자동 모드를 유지 하고 싶은 시간을 입력(분단위):', end='')
    t = int(input())
    endTime = time.time() + (60 * t)
    print('==========================탐색중========================')
    print(f'{t}분뒤에 종료됨')
    autoGetStock.lookFor(recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET)
    autoGetGongSi.lookFor(gongsiData, DART_KEY, CORP_INFO)
    while True:
        if int(time.time()) % 100 == 0:
            print(f'자동 탐색 종료{int(endTime - time.time()) // 60}분 남음')
            autoGetStock.lookFor(recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET)
            autoGetGongSi.lookFor(gongsiData, DART_KEY, CORP_INFO)
        if time.time() > endTime:
            print('탐색 종료')
            break
    autoGetNews.get(newsDict)

async def main(newsDict, recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET, gongsiData, DART_KEY, CORP_INFO):
    c1 = test()
    c2 = search(newsDict, recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET, gongsiData, DART_KEY, CORP_INFO)
    await asyncio.gather(c1, c2)
