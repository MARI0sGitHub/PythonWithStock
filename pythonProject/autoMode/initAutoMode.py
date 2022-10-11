import time

#자동 모드 수행전 북마크 데이터 셋
def load():
    bookList = dict()
    f = open('userData/bookMark.txt', 'r')
    lines = f.readlines()
    print('관심 종목 불러오기 완료')
    for line in lines:
        line = line[:-1]
        print(line)
        bookList[line] = True
    f.close()
    return bookList

def addBookMarkMode(bookList, stockCodes):
    print('===================================================')
    while True:
        print('추가할 관심 종목명 입력(0 입력시 건너뜀):', end = '')
        s = input()
        if s == '0':
            break
        elif s in stockCodes:
            if s in bookList:
                print('이미 등록된 관심 종목')
                continue
            print(f'관심 종목{s}가 추가됨!')
            bookList[s] = True
        else:
            print('현재 상장 되어 있지 않는 종목')
    return bookList

def deleteBookMarkMode(bookList):
    print('===================================================')
    while True:
        print('*관심 종목 리스트*')
        for key, val in bookList.items():
            print(key)
        print('삭제할 관심 종목 입력(0입력시 건너 뜀):', end='')
        s = input()
        if s == '0':
            break
        elif s in bookList:
            print(f'{s}를 관심 기업 리스트에서 제거 완료')
            del bookList[s]
        else:
            print('존재하지 않는 항목!')
    return bookList

def save(bookList):
    f = open('userData/bookMark.txt', 'w')
    for key, _ in bookList.items():
        f.write(key + '\n')
    f.close()
