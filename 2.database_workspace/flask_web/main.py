from flask import Flask, render_template, request, redirect, session
from database import MyDB
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

#.env로드
load_dotenv()

#Flask class 생성
# 생성자 함수에는 파일의 이름
app = Flask(__name__)

# 세션을 사용하기 위해 secret_key를 설정
app.secret_key = os.getenv('secret_key')


# DB server에 웹에서 사용할 table이 존재하나?
# 존재한다면 아무 행동도 안 함
# 존재하지 않으면 테이블 생성
# 유저 테이블 생성
create_table = '''
    CREATE TABLE 
    IF NOT EXISTS
    `user_list`
    (
        id varchar(32) primary key,
        password varchar(64) not null,
        name varchar(32)
    )
'''
# MyDB를 이용하여 서버에 접속, 쿼리 전송
web_db = MyDB()

# create_table 쿼리 실행
web_db.execute_query(create_table)

# 유저와 서버간의 데이터를 주고 받는 부분 생성
# api 생성

# localhost:5000/요청
@app.route('/')
def index():
    #로그인 화면을 보여준다.
    
    return render_template('signin.html')

# 로그인 화면에서 id password를 받아주는 주소를 생성
# /login, post 방식으로 데이터
@app.route('/login', methods =['post'])
def login():
    # post 방식으로 데이터를 보낸 데이터는 request 안에 form에 존재(dict 형태)
    # {user_id : xxxx, user_pass : xxxx}
    # 유저가 보낸 아이디값을 변수에 저장
    input_id = request.form['user_id']
    input_pass = request.form['user_password']
    #유저가 보낸 데이터를 확인
    print(f'[post]/login:{input_id}, {input_pass}')
    
    # 로그인의 로직
    # user_list라는 테이블에서 유저가 보낸 id, password를 모두 존재하는 인덱스가 있나?
    # sql 쿼리문을 통해 
    login_query = '''
        SELECT 
        *
        FROM
        `user_list`
        WHERE id = %s AND password = %s
    '''
    # execute_query()함수는 select문 넣었을 때 돌려주는 데이터 타입은 : dataframe
    # 데이터 프레임의 길이가 0이면 -> 로그인 실패
    # 길이가 1이라면 -> 로그인이 성공
    res_sql = web_db.execute_query(login_query,input_id,input_pass)
    
    if len(res_sql):
        # 로그인이 성공했다면 특정 페이지 보여줌. (render_template)
        # 특정 주소로 이동 ( redirect(주소값) )
        # main.html와 같이 로그인 한 유저의 이름 보내기
        # 이름만 출력
        # res_sql.loc[0,'name'], res_sql.iloc[0,2]
        # res_sql['name'][0]
        logined_name = res_sql.loc[0,'name']
        # return 로그인 성공
        # render_template('파일 이름',key= value, key = value, ... )
        # session에 로그인 정보 저장gkrh
        # session에 데이터를 대입
        session['login_info'] = request.form
        #database에 있는 sales records table 로드
        select_query = '''
            SELECT
            *
            FROM
            `sales records`
            LIMIT 10
        '''
        sales_data = web_db.execute_query(select_query)
        # dataframe을 list 안에 dictionary 형태로 변경
        list_data = sales_data.to_dict(orient = 'records')
        # html table에서 필요한 데이터를 컬럼의 이름들을 변수에 따로 저장
        # list_data에서 key 추출
        cols = list_data[0].keys()
        
        # sales_data -> 'Sales Channel' 컬럼을 기준으로 그룹화
        # total_prifit을 그룹화 연산을 통해 합계 구하기
        # index의 값을 리스트로 생성
        # value의 값을 리스트로 생성
        group_query = '''
            SELECT `Sales Channel`, sum(`Total Profit`) as `sum of profit`
            FROM `sales records`
            GROUP BY `Sales Channel`;
        '''
        group_data = web_db.execute_query(group_query)
        glist_data = group_data.to_dict(orient='records')
        gcols = glist_data[0].keys()
        
        # print(glist_data)
        # print(gcols)
        
        
        return render_template('main.html',
                               name = logined_name,
                               columns = cols,
                               td_data = list_data,
                               gcolumns = gcols,
                               g_data = glist_data)
    else:
        # 로그인이 실패했다면 로그인 주소로 이동('/')

        return redirect('/')
    
@app.route('/signup')
def signup():
    # 로그인이 되어 있는 상태라면 해당 페이지를 보여주지 않음
    # 로그인이 되어있는 상태 : session에서 login_info 키가 존재하는가 ?
    # dict데이터에서 val1, val2, val3 = dict --> val1, val2, val3에는 키값 들어감
    # dict 데이터에서 in 비교연산자 -> 키값에 존재 유무
    if 'login_info' in session:
        return render_template('home.html')
    else:
        return render_template('signup.html')

@app.route('/signup2',methods=['post'])
def signup2():
    input_id = request.form['user_id']
    input_pass = request.form['user_pass']
    input_name = request.form['user_name']
    print(f'[POST] / signup2 유저입력 아이디 : {input_id}, 유저입력 비번 : {input_pass}, 유저입력 이름 : {input_name}')
    
    insert_query = '''
        INSERT INTO `user_list` (`id`, `password`, `name`) 
        VALUES (%s, %s, %s);
    '''
    

    try:
        web_db.execute_query(insert_query,input_id,input_pass,input_name,inplace=True)
        return redirect('/')
    # except Exception as e:
    #     print(e)
    except:
        select_query ='''
            SELECT id
            FROM `user_list`
        '''
        sql_res= web_db.execute_query(select_query)
        # print(input_id in sql_res['id'].to_list())
        
        if input_id in sql_res['id'].to_list():
            print('[error]중복된 아이디가 존재합니다.다른 아이디를 이용해주세요')
        return redirect('/signup')
            

@app.route('/graph',methods=['get'])
def graph():
    # select 쿼리 이용 -> sales records 전체 데이터 로드
    select_query = '''
        SELECT *
        FROM `sales records`
    '''
    # 해당 결과는 dataframe 에서
    df = web_db.execute_query(select_query)
    # print(df)
    # Order Date컬럼의 데이터를 시계열 데이터로 변경하고 저장
    OD = df['Order Date']
    df['Order Date'] = pd.to_datetime(OD,format='%m/%d/%Y')
    # print(type(df['Order Date'][1]))
    # 새로운 파생변수 Order Year 생성, Order Date에서 4글자의 년도를 추출
    df['Order Year'] = df['Order Date'].dt.strftime('%Y')
    print(df['Order Year'])
    # Sales Cannel과 Order Year를 기준으로 그룹화 -> Total_profit의 합계
    group_data = df.groupby(['Sales Channel','Order Year'])['Total Profit'].sum()
    # online 데이터를 따로 추출
    online_data = group_data['Online']
    # offline 데이터 따로 추출
    offline_data = group_data['Offline']
    # online 데이터를 추출한 곳에서 index의 값을 리스트로 생성
    data_list = list(online_data.index)
    # online 데이터의 value를 리스트로 생성
    online_value = online_data.values.tolist()
    # offline 데이터의 value를 리스트로 생성
    offline_value = offline_data.values.tolist()
    print(online_value)
    # graph.html 파일에 online, offline 막대그래프 생성까지
    return render_template('graph.html',
                           x_data=data_list,
                           on_data=online_value,
                           off_data=offline_value)

@app.route('/jquery')
def jquery():
    return render_template('jquery.html')




# 웹서버 실행
app.run(debug=True)