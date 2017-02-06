from flask import Flask, render_template,jsonify
from mysql import *

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('index.html', values=values, labels=labels)

@app.route('/charts')
def e2():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('charts.html', values=values, labels=labels)

@app.route('/code/<code>')
def e1(code=None):
    return render_template('real_time.html', code=code)

@app.route('/line', methods=["POST"])
def line():
    s1 = select([test])  # 查询全表
    r1 = conn.execute(s1)
    res = r1.fetchall()
    return jsonify(time = [x[0] for x in res],
                   data = [x[1] for x in res])

if __name__ == "__main__":
    app.run()
