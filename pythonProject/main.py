import getAuth
import getHash
import getCorpXml
import makeCorpDict
import getGongSi
import setGongSiExcel
from autoMode import initAutoMode
from autoMode import autoGetStock
from autoMode import autoGetGongSi
import getNews
from autoMode import asyncCoroutine
import asyncio
from autoMode import autoGetNews

APP_KEY = "api key"
APP_SECRET = "secret key"
URL_BASE = "https://openapivts.koreainvestment.com:29443"

#보안 인증키 발급
ACCESS_TOKEN = getAuth.Auth(APP_KEY, APP_SECRET, URL_BASE)

#해쉬 키 발급
#해쉬키(Hashkey)는 보안을 위한 요소로 사용자가 보낸 요청 값을 중간에 탈취하여 변조하지 못하도록 하는데 사용
HASH_KEY = getHash.hashkey(APP_KEY, APP_SECRET, URL_BASE)

DART_KEY = "api key"
#Dart api를 통해 고유번호 xml파일 다운
getCorpXml.getCode(DART_KEY)


CORP_INFO = makeCorpDict.makeCodeInfo() #key:기업이름, val:고유 번호

print('1. 자동 탐색 모드, 2. 유저 탐색 모드 (이외의 입력은 종료):', end='')
mode = input()

if mode == '1':
    stockCodes = autoGetStock.get_shcodelist(DART_KEY)
    print('종목 코드 로딩 완료!')
    bookList = initAutoMode.load()
    bookList = initAutoMode.addBookMarkMode(bookList, stockCodes)
    bookList = initAutoMode.deleteBookMarkMode(bookList)
    initAutoMode.save(bookList)

    recentData = autoGetStock.load(bookList)
    gongsiData = autoGetGongSi.init(bookList)
    newsDict = autoGetNews.init(bookList)

    asyncio.run(asyncCoroutine.main(newsDict, recentData, stockCodes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET, gongsiData, DART_KEY, CORP_INFO))

elif mode == '2':
    while True:
        print()
        print('===================================================')
        print()
        print('종목 이름 입력: (exit입력시 종료)', end=' ')
        s = input()
        #프로그램 종료
        if s.lower() == 'exit':
            break
        #해당 기업에 대한 고유번호가 있는 경우 진행
        if s in CORP_INFO:
            print('고유 번호:' + CORP_INFO[s])
            #사작일_종료일 (공시 정보를 가져올 기간)
            fileName = getGongSi.getList(DART_KEY, CORP_INFO[s], s, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET)
            #공시 엑셀 파일의 열 너비를 보기 쉽게 조절
            if fileName != '':
                setGongSiExcel.set(fileName)
            print('공시 정보 파일 생성 완료!')
            newsFiles = getNews.get(s)
            for file in newsFiles:
                getNews.editExcel(file)
            print('뉴스 관련 자료 생성 완료!')
            break
        else:
            print('해당 하는 종목 없음!')
            continue