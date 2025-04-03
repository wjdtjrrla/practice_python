from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/second')
def second():
    return render_template('second.html')

@app.route('/item_info')
def item_info():
    #선택한 상품
    user_select = request.args['item']
    return render_template('item_info.html',
                           selected = user_select)
    
@app.route('/shop')
def shop():
    # 물건의 수량
    item_cnt = request.args['cnt']
    # 물건의 가격
    item_price = request.args['price']
    return render_template('shop.html',
                           price = item_cnt * item_price)
    
app.run(debug=True)