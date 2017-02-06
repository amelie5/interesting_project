from flask import Flask, render_template


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('index.html', values=values, labels=labels)

@app.route('/e2')
def e2():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('charts.html', values=values, labels=labels)

@app.route('/e1/<code>')
def e1(code=None):
    return render_template('c.html', code=code)

if __name__ == "__main__":
    app.run()
