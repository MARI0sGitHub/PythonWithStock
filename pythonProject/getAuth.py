import json
import requests
#한국 투자 증권api를 사용하는데 필요한 보안 토큰을 발급하기 위한 코드 입니다#

def Auth(APP_KEY, APP_SECRET, URL_BASE):
    #rest api의 구성
    #권한 인증 등에 활용되는 header
    headers = {"content-type":"application/json"}
    #body는 POST 방식에 활용, GET방식 할 때 query string 사용
    body = {"grant_type":"client_credentials",
            "appkey":APP_KEY,
            "appsecret":APP_SECRET}
    #위치를 나타내는 path
    PATH = "oauth2/tokenP"

    URL = URL_BASE + '/' + PATH

    res = requests.post(URL, headers=headers, data=json.dumps(body))

    # POST 요청을 진행하면 보안인증키 얻어옴
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN