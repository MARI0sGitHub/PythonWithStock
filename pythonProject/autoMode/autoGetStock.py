import requests
from io import BytesIO
import zipfile
import json
import xmltodict
import getStock
from pynotifier import Notification

def get_shcodelist(DART_KEY):
    print('종목 코드 정보를 불러 오는 중....')
    api = 'https://opendart.fss.or.kr/api/corpCode.xml'
    res = requests.get(api, params={ 'crtfc_key': DART_KEY })
    data_xml = zipfile.ZipFile(BytesIO(res.content))
    data_xml = data_xml.read('CORPCODE.xml').decode('utf-8')

    data_odict = xmltodict.parse(data_xml)
    data_dict = json.loads(json.dumps(data_odict))
    data = data_dict.get('result', {}).get('list')

    length = 0
    for i in range(len(data)):
        if data[i]['stock_code'] is not None:
            length = length + 1
    shcodelist = dict()

    count = 0
    for i in range(len(data)):
        if data[i]['stock_code'] is not None:
            shcodelist[data[i]['corp_name']] = data[i]['stock_code']
            count = count + 1
    return shcodelist

def load(bookList):
    recentData = dict()
    for key, _ in bookList.items():
        try:
            f = open(f'userData/stock/{key}.txt', 'r')
            lines = f.readlines()
            temp = []
            for line in lines:
                temp.append(line[:-1])
            recentData[key] = temp
        except:
            f = open(f'userData/stock/{key}.txt', 'w')
            f.write('0\n')
            f.close()
            recentData[key] = ['0']
    return recentData

def lookFor(recData, Codes, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET):
    for key, val in recData.items():
        old = val[0]
        s = key
        stock_code = ''
        if s in Codes:
            stock_code = Codes[s]
        else:
            continue
        new = getStock.get(s, stock_code, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET)
        if old != new:
            recData[key][0] = new
            Notification(
                title='새로운 정보를 발견!',
                description=f'****{s}의 주가가 {recData[key][0]}원 으로 업데이트됨****',
                duration=9999
            ).send()
            print(f'****{s}의 주가가 {recData[key][0]}원 으로 업데이트됨****')
            f = open(f'userData/stock/{key}.txt', 'w')
            f.write(new + '\n')
            f.close()