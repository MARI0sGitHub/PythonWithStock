import json
import requests

def hashkey(APP_KEY, APP_SECRET, URL_BASE):
    datas = {
        "CANO": '00000000',
        "ACNT_PRDT_CD": "01",
        "OVRS_EXCG_CD": "SHAA",
        "PDNO": "00001",
        "ORD_QTY": "500",
        "OVRS_ORD_UNPR": "52.65",
        "ORD_SVR_DVSN_CD": "0"
    }

    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
        'content-Type' : 'application/json',
        'appKey' : APP_KEY,
        'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]

    return hashkey