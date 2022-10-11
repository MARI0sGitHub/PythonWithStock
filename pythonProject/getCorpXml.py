from io import BytesIO
from zipfile import ZipFile
import urllib.request
#고유번호 파일을 받아오기 위한 코드입니다#

def getCode(DART_KEY):
    url = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=' + DART_KEY
    with urllib.request.urlopen(url) as zipresponse:
        with ZipFile(BytesIO(zipresponse.read())) as zipfile:
            zipfile.extractall('corpCode')