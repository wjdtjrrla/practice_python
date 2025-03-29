# 기본적인 웹 서버 코드
from flask import Flask, request,redirect,render_template,url_for
from database import MyDB
import pandas as pd
import os

#Flask 클래스 생성
app = Flask(__name__)

# MyDB Class 생성
web_db = MyDB()

#127.0.0.1:5000/ url 생성
@app.route('/')
def index():
    return render_template('index.html')


# dashboard를 보는 url 생성
@app.route('/dashboard')
def dashboard():
    # 유저가 보내주는 데이터 : ticker
    ticker = request.args['ticker']
    # ticker에 따라 다른 csv파일을 로드해줌
    print(f'[get] / /dasdhboard : {ticker}')
    
    # 상대경로 사용해서 불러오기
    df = pd.read_csv(f"./data/{ticker}.csv")
    
    # 절대 경로 사용해서 불러오기
    # df = pd.read_csv(f"/home/jeongseok/mysite/data/{ticker}.csv")
    
    # os 사용
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir,'data',f'{ticker}.csv')
    df = pd.read_csv(csv_path)
    
    # 데이터프레임 하위 50개 추출
    df = df.tail(50)
    # Date 컬럼에 데이터를 리스트로 생성 -> X축 데이터
    date_list = df['Date'].to_list()
    # Adj Close 컬럼의 데이터를 리스트로 생성 -> y축 데이터
    close_list = df['Adj Close'].to_list()
    # 전체 데이터프레임을 dict 형태로 변환
    dict_data = df.to_dict(orient='records')
    # dict 에서 첫번째 원소의 값들 = 키값들을 리스트로 생성
    cols_list = list(dict_data[0].keys())
    #대시보드에 date 컬럼의 리스트와 adj close 리스트, dict, keys들을 모두 보낸다.
    
    volume_list = df['Volume'].to_list()

    
    
    
    
    
    
    
    
    
    
    
    
    
    return render_template('dashboard.html',
                           x_data = date_list,
                           y_data = close_list,
                           table_data = dict_data,
                           table_cols = cols_list,
                           y_data2 = volume_list)


#웹서버 실행
app.run(debug=True)