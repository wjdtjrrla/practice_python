# 환율 정보 csv 저장 자동화 풀 코드
import pandas as pd
import os

# 저장하고자 하는 파일 이름
file_name = '환율.csv'

# header인자값 정하기, 컬럼을 저장할지 말지 여부 결정
header_bool  = not os.path.exists(file_name)

df = pd.read_html(
    'https://finance.naver.com/marketindex/exchangeList.naver',
    encoding='cp949'
    )[0]

# csv 파일로 저장장
df.to_csv(
    file_name,
    mode='a',   
    index =False,
    header=header_bool
)