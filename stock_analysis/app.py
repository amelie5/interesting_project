from flask import Flask, render_template,jsonify

from mysql import *

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('index.html', values=values, labels=labels)

@app.route('/c')
def c():
    return render_template('c.html')

@app.route('/charts')
def e2():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('charts.html', values=values, labels=labels)

@app.route('/e1')
def e1():
    labels = ['January', 'February', 'March', 'April', 'May']
    values = [10, 9, 8, 7, 6]
    return render_template('e1.html', code=values, values=values, labels=labels)

@app.route('/e1e', methods=["POST"])
def e1e():
    labels = ["January", "February", "March", "April", "May"]
    values = [10, 9, 8, 7, 6]
    return  jsonify(values=values, labels=labels)


@app.route('/code/<code>')
def code(code=None):
    return render_template('real_time.html', code=code)

@app.route('/line', methods=["POST"])
def line():
    s1 = 'select ctime,data from price'  # 查询全表
    r1 = conn.execute(s1)
    res = r1.fetchall()
    print(x[0] for x in res)
    return jsonify(time = [x[0] for x in res],
                   data = [x[1] for x in res])

if __name__ == "__main__":
    app.run()
