# flask web server 실행
# 프레임 워크 호출
from flask import Flask, render_template, request, redirect, session
import random
from database import MyDB

# 클래스 생성
app = Flask(__name__)

web_db = MyDB(
    _host = '172.30.1.60',
    _port=3306,
    _user='ubion',
    _password='1234',
    _db = 'ubion'
)

app.secret_key='asdfqwer'

# api 생성, 함수 생성
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    # 세션에 데이터가 존재한다면?
    if 'user_nick' in session:
        return render_template('game.html',
                               nick_name = session['user_nick'])
    else:
        #index.html을 이용하여 보낸 데이터를 변수에 저장
        #get 방식으로 들어온 데이터는 request.args에 존재 ( post인 경우 request.form에 존재 )
        try:
            # 정상적으로 작동하는 경우
            user_nick = request.args['nickname']
            print(f'[get] /game : {user_nick}')
            # 세션에 닉 저장
            session['user_nick'] = user_nick
            return render_template('game.html',
                                   nick_name=user_nick)
        except Exception as e:
            print(e)
            # 에러 발생한다면 첫 페이지로 이동
            return redirect('/')
            
@app.route('/game_result')
def game_result():
    #data : { 'user' : xxxx }
    user_select = int(request.args['user'])
    print(f'[get] /game_result : {user_select}')
    #1:가위, 2:바위, 3:보
    #서버가 선택할 리스트 생성
    _list = [1,2,3]
    server_select = random.choice(_list)
    # 유저가 선택한 값과 서버가 선ㅌ택한 값을 가지고 조건
    if user_select == server_select:
        result = '무승부'
    else:
        #유저가 가위인 경우
        if user_select == 1:
            #서버가 바위를 냈다면?
            if  server_select ==2:
                result = '패배'
            #서버가 보를 냈다면?
            else:
                result = '승리'
        #유저가 바위인 경우
        elif user_select==2:
            if server_select ==1:
                result='승리'
            else:
                result='패배'
        #유저가 보인 경우
        else:
            if server_select == 1:
                result='패배'
            else:
                result='승리'
    #ajax에서 받는 데이터 ㅏ입을 json으로 지정해서 
    return_data = {
        'user':user_select,
        'server' : server_select,
        'result' : result
    }
    print(f'[get_ajax] /game_result : GAME_DATA{return_data}')
    return return_data
            
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/check_id', methods=['POST'])
def check_id():
    #post 방식으로 들어오는 데이터
    user_id = request.form['user_id']
    print(f'[post] /check_id : {user_id}')
    #DB에 해당하는 아이디가 존재하는가?
    select_query = '''
        SELECT *
        FROM `user_list`
        WHERE `id` = %s
    '''
    res_sql = web_db.execute_query(select_query,user_id)
    print(f'[post] /check_id : {res_sql}')
    if len(res_sql) == 0:
        result = True
    else:
        result = False
    return_data = {
        'check_id':result
    }
    return return_data
        
        
@app.route('/signup2', methods=['post'])
def signup2():
    # 회원 가입 페이지에서 유저가 입력한 데이터들을 모두 변수에 저장
    # id, pass1, pass2, name 4개의 부분에서 입력
    # id, pass1, name 공간에는 name 속성 존재
    # pass2는 name 속성이 존재하지 않는다(해당하는 데이터는 받을 수 없다.)
    print(f'[post] /signup2 : {request.form}')
    user_id=request.form['user_id']
    user_pass=request.form['user_pass']
    user_name=request.form['user_name']
    
    
    # 에러가 발생하는 경우?
        # try, except
    # 데이터베이스에 INSERT 작업
    # insert가 정상 작동이라면 -> 로그인 페이지 redirect('/로그인 페이지 주소')
    # 정상 작동 아니면 -> 회원가입 페이지 redirect('/signup)
    insert_query = '''
        INSERT INTO `user_list`(id, password, name)
        values(%s,%s,%s)
    '''
    try:
        web_db.execute_query(insert_query, user_id, user_pass, user_name, inplace=True)
        return redirect('/')
    except Exception as e :
        print(f'[post] /signup2 : ERROR {e}')
        return redirect('signup')
    
    
    
        
        
        
        
    

# 앱실행
app.run(debug=True)