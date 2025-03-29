import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver

url = 'https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd='

# input()함수를 이용하여 종목 코드 받는다.
code = []
# 반복문을 이요하여 종목 코드를 여러 개 받는다.
while True:
    input_data = input('종목 코드를 입력하시오')
    # input_data가 빈 문자열이라면 input_data ==''
    # input_data의 길이가 0이거나 len(input_data) ==0
    if input_data == '':
        break
    # input_data의 길이가 6이 아니라면 반복문으로 돌아간다.
    if len(input_data) != 6:
        print('종목코드는 6자리로 입력해주세요.')
        continue
    
    
    
    # input_data code에 추가
    code.append(input_data)
    
# 웹 브라우져 열기
driver = webdriver.Chrome()

# code를 기준으로 반복문 생성
for c in code:
    # 특정 웹사이트 오픈
    driver.get(url+c)
    time.sleep(2)
    # 웹 사이트 html구조 파싱
    soup = bs(driver.page_source,'html.parser')
    

    table_data = soup.find_all(
        'table',
        attrs={
            'class' : 'gHead01 all-width'
        }
    )[-1]
    df = pd.read_html(
        str(table_data)
    )[0]
    #파일의 이름 지정 : 종목 코드 + report + 현재 시간 .csv
    time_data = datetime.now().strftime('%Y-%m-%d')
    df.to_csv(f'{c} report {time_data}.csv',index=False)
    print(f'{c} report {time_data}.csv 파일이 생성')


# 웹 브라우저 종료
driver.close()