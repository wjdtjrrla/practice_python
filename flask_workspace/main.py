'''
    - 서버를 식당에 비유 -
        식당 오픈 = 서버 생성
        메뉴판 만들기 = api 생성
        서빙 직원 호출 = api 호출
'''
# flask 프레임워크 로드
from flask import Flask, render_template, request
import pandas as pd

# class 생성
# Flask class는 파일의 이름을 인자값으로 대입
# 현재 파일의 이름은 __name__
app = Flask(__name__)
 
# api 생성
# base_url -> localhost // 127.0.0.1
# port : 5000 , 8080은 express
# 웹서버 접속 시에는 -> localhost:5000

# 누군가 내 웹 서버에 요청을 보낸다.
# localhost:5000
@app.route('/')
def index():
    # index()함수는 localhost:5000 / 요청이 왔을 때 호출
    # 문자열 되돌려줄 때
    # return '<h1>Hello</h1>'
    
    # html 문서 되돌려줄 때
    # render_template()함수는 기본 경로가 현재 작업 공간에서 하위 폴더인 templates로 구성
    return render_template('index.html')

# /second 주소로 요청이 들어왔을 때
# second.html을 되돌려준다.
# second 페이지에서는 메인 화면으로 돌아가는 하이퍼링크 생성

#127.0.0.1:5000/second
@app.route('/second')
def second():
    # return '<h1><i>second Page</i></h1>'
    return render_template('second.html')


# get 방식 데이터 전송
@app.route('/login')
def login():
    # request 메시지 확인 -> flask에 request 로드
    print(request.args)
    # 로그인이 성공하는 조건?
    # 유저가 입력한 아이디의 값이 'test'
    # 유저가 입력한 비번의 값이 'asdf1234'
    # 두 조건 모두 만족할 시 로그인 (AND)
    # 둘 중 하나라도 만족 안되면 로그인 실패

    if (request.args['input_id']=='test') & (request.args['input_pass']=='asdf1234'):
        return '로그인 성공'
    else:
        return '로그인 실패'
    
    
# post 방식 데이터 전송  
@app.route('/login_post', methods={'post'})
def login_post():
    print(request.form)
    user= pd.read_csv('./user_info')
    print(user)

    # if request.form['post_id'] in user['id'].values:
    #     if user.loc[user['id'] == request.form['post_id'],'pass'].values[0] == int(request.form['post_pass']):
    #         return '로그인 성공'
    # else:
    #     return '로그인 실패'
    #----------------------------------------------------------------------------------------------
    flag = user['id'] == request.form['post_id']
    flag2 = user['pass'] == int(request.form['post_pass'])
    print(f"user 데이터프레임 결과 : {user.loc[flag&flag2]}")
    if len(user.loc[flag&flag2]):
        user_name = user.loc[flag,'name'].iloc[0]
        print(user_name)
        
        return render_template('main.html',user = user_name)
    else:
        return '로그인 실패'
    #----------------------------------------------------------------------------------------------
    # login_check = False
    # for i in range(len(user)):
    #     if list(user.iloc[i].values) == [request.form['post_id'],int(request.form['post_pass'])]:
    #         login_check=True
    #     if login_check == 1:
    #         return '로그인 성공'
    #     else:
    #         return '로그인 실패'


# 웹 서버 오픈
# host 매개 변수 : 접속할 수 있는 아이피의 목록0
# port 매개변수 : 해당하는 주소의 포트 번호
# debug 매개변수 : 디버그 모드 오픈 여부 
app.run(debug=True)




#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
# 유저가 서버에게 데이터를 보내는 경우
    # html 문서 안에 유저가 입력할 수 있는 공간 생성
        # input 태그 이용
    # 데이터를 보내는 방법은
        # 일반적으로 form 태그 사용
        # 어느 주소로 보낼 것인가? (action)
        # 어떤 방법으로 보낼 것인가? (method)
            #get
                # url 뒤에 ?를 붙여 key = value 형태로 데이터 전송
                # 데이터 노출로 인한 보안상 문제가 발생 가능
                # url은 최대 255자까지제한
                # 보안적으로 노출이 되면 안되는 데이터나 굉장히 긴 데이터는 전송 불가능
                # requests 메시지 안에 args 키 값에 데이터가 dict 형태로 존재
            #post
                # requests 데이터에서 body라는 부분에 데이터를 담아서 보낸다.
                # 데이터의 노출이 없고, 길이의 제한이 없다.
                # get에 비해 상대적으로 느리다. (그치만 빠르다)
                # requests 메시지 안에 form 키 값에 데이터가 딕셔너리 형태로 존재


# 서버가 유저에게 데이터를 보내는 경우
    # html 문서를 제외한 다른 특정 데이터를 보낸다.
    # html과 특정 데이터를 묶어서 하나의 html로 만드는 과정이 필요
    # render_template(파일의 이름, html에서 사용할 변수명 = 데이터)
        # html 문서를 불러온다. 한줄씩 확인
        # 반복 도중 {% %}와 같은 부분을 확인
        # {% python code %} python code로 변환
        # 변수는 그냥 변수 값으로 되돌림
        # if나 for의 경우 들여쓰기를 html이 인식 불가
        # 끝나는 부분은 작성 {%endif%} {%endfor%
        # 전체 데이터를 문자열로 변경하여 유저에게 되돌려주는 형태