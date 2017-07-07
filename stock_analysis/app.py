from flask import Flask, render_template, jsonify
import tushare as ts
from mysql import *
from flask_socketio import SocketIO, emit
import json





def transfer(x):
    ntype = ''
    if x >= 9.9:
        ntype = 'zhangting!!!!'
    elif x >= 5:
        ntype = '5-10'
    elif x >= 0:
        ntype = '0-5'
    elif x >= -5:
        ntype = '-5- 0'
    elif x > -9.9:
        ntype = '-10- -5'
    else:
        ntype = '-10'
    return ntype


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']='bendawang'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/zs_table')
def zs_table():
    df=get_zs()
    return render_template('zs_table.html', values=df)


@app.route('/c/<code>/<date>')
def c(code=None,date=None):
    df = ts.get_tick_data(code, date=date).sort(columns='time')
    list_time=df['time'].values.tolist()
    list_price=df['price'].values.tolist()
    start_price=df['price'].head(1).values
    #list_price = df.apply(lambda x: x['changepercent']-start_price, axis=1).values.tolist()
    return render_template('c.html',code=code,date=date,start_price=start_price,list_time=list_time,list_price=list_price)


# @app.route('/form', methods=['GET', 'POST'])
# def form():
#     form = MyForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         print(name)
#     return render_template('form.html', form=form)


@app.route('/charts')
def e2():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('charts.html', values=values, labels=labels)


@app.route('/e1')
def e1():
    df = ts.get_today_all()
    df = df[['changepercent', 'trade', 'volume']]
    str=df.describe().to_string()
    df['c'] = df.apply(lambda x: transfer(x['changepercent']), axis=1)
    cnt = df.groupby(df['c']).size().astype(float)
    labels = list(cnt.index)
    values = list(cnt)
    j = {'labels': labels, 'values': values,'str':str}
    return render_template('e1.html',j=j)

@socketio.on('e1_event')
def client_msg(msg):
    print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    df = ts.get_today_all()
    df = df[['changepercent', 'trade', 'volume']]
    str = df.describe().to_string()
    df['c'] = df.apply(lambda x: transfer(x['changepercent']), axis=1)
    cnt = df.groupby(df['c']).size().astype(float)
    labels = list(cnt.index)
    values = list(cnt)
    j = {'labels': labels, 'values': values,'str':str}
    emit('e1_response',j)


@app.route('/code/<code>')
def code(code=None):
    return render_template('real_time.html', code=code)


@app.route('/line', methods=["POST"])
def line():
    s1 = 'select ctime,data from price'  # 查询全表
    r1 = conn.execute(s1)
    res = r1.fetchall()
    print(x[0] for x in res)
    return jsonify(time=[x[0] for x in res],
                   data=[x[1] for x in res])


if __name__ == "__main__":
    app.run()
