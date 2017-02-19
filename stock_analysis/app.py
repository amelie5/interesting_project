from flask import Flask, render_template, jsonify
import tushare as ts
from mysql import *

# from form import MyForm


def transfer(x):
    ntype = ''
    if x >= 9.0:
        ntype = '10'
    elif x >= 5:
        ntype = '5-10'
    elif x >= 1:
        ntype = '1-5'
    elif x >= -1:
        ntype = '-1-1'
    elif x >= -5:
        ntype = '-5- -1'
    elif x > -9.0:
        ntype = '-10- -5'
    else:
        ntype = '-10'
    return ntype


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']='bendawang'


@app.route('/')
def index():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('index.html', values=values, labels=labels)


@app.route('/c')
def c():
    df = ts.get_tick_data('600848', date='2017-02-17').sort(columns='time')
    list_time=df['time'].values.tolist()
    list_price=df['price'].values.tolist()
    start_price=df['price'].head(1).values
    #list_price = df.apply(lambda x: x['changepercent']-start_price, axis=1).values.tolist()
    return render_template('c.html',code='600848',date='2017-02-17',start_price=start_price,list_time=list_time,list_price=list_price)


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
    df['c'] = df.apply(lambda x: transfer(x['changepercent']), axis=1)
    cnt = df.groupby(df['c']).size().rename('counts')
    labels = list(cnt.index)
    values = list(cnt)
    return render_template('e1.html', values=values, labels=labels)


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
