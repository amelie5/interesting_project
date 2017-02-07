from flask import Flask,request,render_template
from parse import *

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    table = '<table border="1">'
    for k in sorted(res_list, key=lambda x: x[3], reverse=True)[:10]:
        table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%k
    table +='</table>'
    return table

if __name__ == '__main__':
    app.run()