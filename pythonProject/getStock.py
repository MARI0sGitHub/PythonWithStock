import requests
#3. 주식 시세 가져오기

def get(s, stock_code, URL_BASE, ACCESS_TOKEN, APP_KEY, APP_SECRET):
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"

    #주식현재가 시세의 tr_id는 "FHKST01010100"
    headers = {"Content-Type":"application/json",
               "authorization": f"Bearer {ACCESS_TOKEN}",
               "appKey":APP_KEY,
               "appSecret":APP_SECRET,
               "tr_id":"FHKST01010100"
    }
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code
    }
    res = requests.get(URL, headers=headers, params=params)
    cur = res.json()['output']['stck_prpr']
    return cur